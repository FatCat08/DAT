import { useEffect, useState } from 'react'
import { checkHealth } from './services/api'
import './App.css'

function App() {
    const [health, setHealth] = useState('Checking...');

    useEffect(() => {
        checkHealth().then(data => {
            setHealth(data.status === 'ok' ? 'Connected to Backend ✅' : 'Backend Disconnected ❌');
        });
    }, []);

    return (
        <div className="app-container">
            <div className="sidebar">
                <h2>Sidebar</h2>
                <p>Sessions will go here</p>
            </div>
            <div className="chat-panel">
                <h2>Chat Panel</h2>
                <p>System Status: {health}</p>
                <div className="input-area">
                    <input type="text" placeholder="Type your query here..." disabled />
                </div>
            </div>
            <div className="chart-panel">
                <h2>Chart Panel</h2>
                <p>Charts will render here</p>
            </div>
        </div>
    )
}

export default App
