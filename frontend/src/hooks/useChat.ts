import { useState, useEffect, useRef } from 'react';
import { fetchSessionDetail } from '../services/api';

export function useChat(sessionId: string | null) {
    const [messages, setMessages] = useState<any[]>([]);
    const [isStreaming, setIsStreaming] = useState(false);
    const [currentChart, setCurrentChart] = useState<any>(null);
    const [currentData, setCurrentData] = useState<any>(null);
    const [loadingHistory, setLoadingHistory] = useState(false);

    // Keep track of the active SSE connection to abort if needed
    const abortControllerRef = useRef<AbortController | null>(null);

    useEffect(() => {
        if (!sessionId) {
            setMessages([]);
            setCurrentChart(null);
            setCurrentData(null);
            return;
        }

        const loadHistory = async () => {
            setLoadingHistory(true);
            try {
                const detail = await fetchSessionDetail(sessionId);
                setMessages(detail.messages || []);

                // If the last message from assistant has chart metadata, render it
                if (detail.messages && detail.messages.length > 0) {
                    let foundData = false;
                    for (let i = detail.messages.length - 1; i >= 0; i--) {
                        const msg = detail.messages[i];
                        if (msg.role === 'assistant' && msg.metadata?.chart && msg.metadata?.data) {
                            setCurrentChart(msg.metadata.chart);
                            setCurrentData(msg.metadata.data);
                            foundData = true;
                            break;
                        }
                    }
                    if (!foundData) {
                        setCurrentChart(null);
                        setCurrentData(null);
                    }
                }
            } catch (error) {
                console.error("Error loading chat history:", error);
                setMessages([]);
            } finally {
                setLoadingHistory(false);
            }
        };

        loadHistory();

        // Cleanup function
        return () => {
            if (abortControllerRef.current) {
                abortControllerRef.current.abort();
            }
        };
    }, [sessionId]);

    const sendMessage = async (content: string) => {
        if (!content.trim() || !sessionId || isStreaming) return;

        // 1. Instantly add user message to UI
        const userMsg = { id: Date.now().toString(), role: 'user', content };
        setMessages(prev => [...prev, userMsg]);

        // 2. Add an empty assistant message to stream into
        const botMsgId = (Date.now() + 1).toString();
        const initialBotMsg = { id: botMsgId, role: 'assistant', content: '', metadata: {} };
        setMessages(prev => [...prev, initialBotMsg]);
        setIsStreaming(true);
        setCurrentChart(null);

        abortControllerRef.current = new AbortController();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: sessionId, message: content }),
                signal: abortControllerRef.current.signal
            });

            if (!response.body) throw new Error("ReadableStream not yet supported in this browser.");

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let aiText = '';
            let metadata: Record<string, any> = {};

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                const lines = chunk.split('\n');

                let currentEvent = null;

                for (let i = 0; i < lines.length; i++) {
                    const line = lines[i].trim();
                    if (!line) continue;

                    if (line.startsWith('event: ')) {
                        currentEvent = line.substring(7).trim();
                    } else if (line.startsWith('data: ')) {
                        const dataStr = line.substring(6).trim();
                        if (!dataStr) continue;

                        try {
                            const dataObj = JSON.parse(dataStr);

                            if (currentEvent === 'text_delta') {
                                aiText += dataObj.content || '';
                                setMessages(prev => prev.map(m =>
                                    m.id === botMsgId ? { ...m, content: aiText, metadata } : m
                                ));
                            } else if (currentEvent === 'sql') {
                                metadata.sql = dataObj.sql;
                                setMessages(prev => prev.map(m =>
                                    m.id === botMsgId ? { ...m, metadata: { ...m.metadata, ...metadata } } : m
                                ));
                            } else if (currentEvent === 'data') {
                                metadata.data = dataObj;
                                setCurrentData(dataObj);
                                setMessages(prev => prev.map(m =>
                                    m.id === botMsgId ? { ...m, metadata: { ...m.metadata, ...metadata } } : m
                                ));
                            } else if (currentEvent === 'chart') {
                                metadata.chart = dataObj;
                                setCurrentChart(dataObj);
                                setMessages(prev => prev.map(m =>
                                    m.id === botMsgId ? { ...m, metadata: { ...m.metadata, ...metadata } } : m
                                ));
                            } else if (currentEvent === 'done') {
                                // Finalize the message ID with the DB's actual ID
                                setMessages(prev => prev.map(m =>
                                    m.id === botMsgId ? { ...m, id: dataObj.message_id } : m
                                ));
                            }
                        } catch (e) {
                            console.error("Error parsing SSE JSON:", e, dataStr);
                        }
                    }
                }
            }
        } catch (error: any) {
            if (error.name === 'AbortError') {
                console.log('Stream aborted');
            } else {
                console.error("Error in chat stream:", error);
                setMessages(prev => [...prev, {
                    id: Date.now().toString(),
                    role: 'assistant',
                    content: 'An error occurred while connecting to the server.'
                }]);
            }
        } finally {
            setIsStreaming(false);
            abortControllerRef.current = null;
        }
    };

    const stopStreaming = () => {
        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
            setIsStreaming(false);
        }
    };

    return {
        messages,
        isStreaming,
        currentChart,
        currentData,
        loadingHistory,
        sendMessage,
        stopStreaming
    };
}
