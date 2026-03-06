import { Plus, MessageSquare, Menu, Settings, Trash2 } from 'lucide-react';
import './style.css';

interface SidebarProps {
    sessions: any[];
    currentSessionId: string | null;
    onSelectSession: (id: string) => void;
    onNewSession: () => void;
    onDeleteSession: (id: string) => void;
}

export default function Sidebar({ sessions, currentSessionId, onSelectSession, onNewSession, onDeleteSession }: SidebarProps) {
    return (
        <aside className="sidebar-container">
            {/* Brand Header */}
            <div className="sidebar-brand">
                <div className="brand-logo">
                    <div className="logo-shape"></div>
                </div>
                <span className="brand-text">Data Agent</span>
                <button className="icon-btn" title="Toggle Menu">
                    <Menu size={18} />
                </button>
            </div>

            {/* New Chat Button */}
            <div className="p-4">
                <button className="new-chat-btn" onClick={onNewSession}>
                    <Plus size={18} />
                    <span>New Analysis</span>
                </button>
            </div>

            {/* History List */}
            <div className="history-section">
                <h3 className="section-title">Recent Sessions</h3>
                <div className="history-list">
                    {sessions.map(session => (
                        <div
                            key={session.id}
                            className={`history-item-wrapper ${currentSessionId === session.id ? 'active' : ''}`}
                        >
                            <button
                                className="history-item"
                                onClick={() => onSelectSession(session.id)}
                            >
                                <MessageSquare size={16} className="item-icon" />
                                <span className="item-text">{session.title}</span>
                            </button>
                            <button
                                className="delete-btn"
                                onClick={() => onDeleteSession(session.id)}
                                title="Delete session"
                            >
                                <Trash2 size={14} />
                            </button>
                        </div>
                    ))}
                </div>
            </div>

            {/* Footer Settings */}
            <div className="sidebar-footer">
                <button className="settings-btn">
                    <Settings size={18} />
                    <span>Settings</span>
                </button>
            </div>
        </aside>
    );
}
