import { Send, Sparkles } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import './style.css';

interface ChatPanelProps {
    status: string;
}

export default function ChatPanel({ status }: ChatPanelProps) {
    return (
        <div className="chat-container">
            {/* Top Header */}
            <header className="chat-header">
                <div className="header-info">
                    <h2>Current Session</h2>
                    <span className="session-status">
                        <span className="status-dot online"></span>
                        {status}
                    </span>
                </div>
            </header>

            {/* Messages Area */}
            <div className="chat-history">
                {/* Mock Bot Message */}
                <div className="message bot-message">
                    <div className="avatar bot-avatar">
                        <Sparkles size={16} />
                    </div>
                    <div className="message-bubble">
                        <ReactMarkdown>
                            Hello! I'm your Data Assistant. You can ask me to analyze database metrics, like:
                            * *Show me the Q4 sales numbers*
                            * *What is the daily active user count this week?*
                        </ReactMarkdown>
                    </div>
                </div>

                {/* Mock User Message */}
                <div className="message user-message">
                    <div className="message-bubble">
                        Show me the Q4 sales numbers, broken down by month.
                    </div>
                    <div className="avatar user-avatar">
                        U
                    </div>
                </div>

                {/* Mock Bot Message 2 */}
                <div className="message bot-message">
                    <div className="avatar bot-avatar">
                        <Sparkles size={16} />
                    </div>
                    <div className="message-bubble">
                        <ReactMarkdown>
                            Certainly. I have analyzed the sales data for Q4. The monthly breakdown is now rendering on your chart panel.

                            **Key Insights:**
                            - December had a 24% spike due to holiday sales.
                            - Overall revenue hit target goals smoothly.
                        </ReactMarkdown>
                    </div>
                </div>
            </div>

            {/* Input Area */}
            <div className="input-container">
                <div className="input-wrapper">
                    <textarea
                        className="chat-input"
                        placeholder="Ask a question about your data..."
                        rows={1}
                    />
                    <button className="send-btn">
                        <Send size={18} />
                    </button>
                </div>
                <p className="input-footer">AI assistants can make mistakes. Please verify important data.</p>
            </div>
        </div>
    );
}
