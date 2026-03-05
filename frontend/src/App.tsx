import { useEffect, useState } from 'react';
import { checkHealth } from './services/api';
import './App.css';

import Sidebar from './components/Sidebar';
import ChatPanel from './components/ChatPanel';
import ChartPanel from './components/ChartPanel';

function App() {
  const [health, setHealth] = useState<string>('Checking...');

  useEffect(() => {
    checkHealth().then((data) => {
      if (data?.status === 'ok') {
        setHealth('Connected & Ready');
      } else {
        setHealth('Offline');
      }
    });
  }, []);

  return (
    <div className="app-container">
      <Sidebar />
      <ChatPanel status={health} />
      <ChartPanel />
    </div>
  );
}

export default App;
