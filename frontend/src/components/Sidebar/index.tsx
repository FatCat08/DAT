import { Plus, MessageSquare, Menu, Settings } from 'lucide-react';
import './style.css';

export default function Sidebar() {
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
                <button className="new-chat-btn">
                    <Plus size={18} />
                    <span>New Analysis</span>
                </button>
            </div>

            {/* History List */}
            <div className="history-section">
                <h3 className="section-title">Recent Sessions</h3>
                <div className="history-list">
                    {/* Mock Item */}
                    <button className="history-item active">
                        <MessageSquare size={16} className="item-icon" />
                        <span className="item-text">Q4 Sales Overview</span>
                    </button>

                    <button className="history-item">
                        <MessageSquare size={16} className="item-icon" />
                        <span className="item-text">User Growth 2025</span>
                    </button>

                    <button className="history-item">
                        <MessageSquare size={16} className="item-icon" />
                        <span className="item-text">Retention Analysis</span>
                    </button>
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
