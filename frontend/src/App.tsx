import { useEffect, useState } from 'react';
import { checkHealth } from './services/api';
import './App.css';

import Sidebar from './components/Sidebar';
import ChatPanel from './components/ChatPanel';
import ChartPanel from './components/ChartPanel';

import { useSessions } from './hooks/useSessions';
import { useChat } from './hooks/useChat';

function App() {
  const [health, setHealth] = useState<string>('Checking...');
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);

  const { sessions, createSession, deleteSession } = useSessions();
  const { messages, isStreaming, currentChart, currentData, sendMessage, stopStreaming } = useChat(currentSessionId);

  useEffect(() => {
    checkHealth().then((data: any) => {
      if (data?.status === 'ok') {
        setHealth('Connected & Ready');
      } else {
        setHealth('Offline');
      }
    });
  }, []);

  const handleCreateNew = async () => {
    const newId = await createSession();
    if (newId) setCurrentSessionId(newId);
  };

  return (
    <div className="app-container">
      <Sidebar
        sessions={sessions}
        currentSessionId={currentSessionId}
        onSelectSession={setCurrentSessionId}
        onNewSession={handleCreateNew}
        onDeleteSession={deleteSession}
      />
      <ChatPanel
        status={health}
        messages={messages}
        onSendMessage={sendMessage}
        isStreaming={isStreaming}
        onStopStreaming={stopStreaming}
      />
      <ChartPanel chartConfig={currentChart} chartData={currentData} />
    </div>
  );
}

export default App;
