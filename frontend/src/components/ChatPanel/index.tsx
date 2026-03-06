import { Send, Sparkles, Square } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { useState, useRef, useEffect } from 'react';
import './style.css';

interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    metadata?: any;
}

interface ChatPanelProps {
    status: string;
    messages: Message[];
    onSendMessage: (msg: string) => void;
    isStreaming: boolean;
    onStopStreaming: () => void;
}

export default function ChatPanel({ status, messages, onSendMessage, isStreaming, onStopStreaming }: ChatPanelProps) {
    const [inputValue, setInputValue] = useState("");
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = () => {
        if (inputValue.trim() && !isStreaming) {
            onSendMessage(inputValue);
            setInputValue("");
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="chat-container">
            {/* Top Header */}
            <header className="chat-header">
                <div className="header-info">
                    <h2>Current Session</h2>
                    <span className="session-status">
                        <span className={`status-dot ${status === 'Connected & Ready' ? 'online' : 'offline'}`}></span>
                        {status}
                    </span>
                </div>
            </header>

            {/* Messages Area */}
            <div className="chat-history">
                {messages.length === 0 ? (
                    <div className="empty-state">
                        <Sparkles size={32} className="empty-icon" />
                        <h3>How can I help you today?</h3>
                        <p>Try asking about your data schema or metrics.</p>
                    </div>
                ) : (
                    messages.map((msg) => (
                        <div key={msg.id} className={`message ${msg.role === 'assistant' ? 'bot-message' : 'user-message'}`}>
                            {msg.role === 'assistant' && (
                                <div className="avatar bot-avatar">
                                    <Sparkles size={16} />
                                </div>
                            )}
                            <div className="message-bubble">
                                {msg.role === 'user' ? (
                                    <div className="whitespace-pre-wrap">{msg.content}</div>
                                ) : (
                                    <>
                                        {msg.metadata?.sql && (
                                            <div className="text-xs text-gray-400 font-mono bg-gray-900 bg-opacity-50 p-2 rounded mb-2">
                                                Generated SQL Query
                                            </div>
                                        )}
                                        <ReactMarkdown>{msg.content}</ReactMarkdown>
                                        {isStreaming && msg === messages[messages.length - 1] && !msg.content && (
                                            <span className="typing-indicator">...</span>
                                        )}
                                    </>
                                )}
                            </div>
                            {msg.role === 'user' && (
                                <div className="avatar user-avatar">
                                    U
                                </div>
                            )}
                        </div>
                    ))
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="input-container">
                <div className="input-wrapper">
                    <textarea
                        className="chat-input"
                        placeholder="Ask a question about your data..."
                        rows={1}
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyDown={handleKeyDown}
                        disabled={isStreaming}
                    />
                    {isStreaming ? (
                        <button className="send-btn stop-btn" onClick={onStopStreaming} title="Stop replying">
                            <Square size={14} className="fill-current" />
                        </button>
                    ) : (
                        <button className="send-btn" onClick={handleSend} disabled={!inputValue.trim()}>
                            <Send size={18} />
                        </button>
                    )}
                </div>
                <p className="input-footer">AI assistants can make mistakes. Please verify important data.</p>
            </div>
        </div>
    );
}
