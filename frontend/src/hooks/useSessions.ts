import { useState, useEffect } from 'react';
import { fetchSessions, createSession, deleteSession } from '../services/api';

export function useSessions() {
    const [sessions, setSessions] = useState([]);
    const [loading, setLoading] = useState(true);

    const loadSessions = async () => {
        try {
            setLoading(true);
            const data = await fetchSessions();
            setSessions(data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadSessions();
    }, []);

    const handleCreateSession = async () => {
        try {
            const newSession = await createSession();
            setSessions(prev => [newSession, ...prev]);
            return newSession.id;
        } catch (error) {
            console.error(error);
        }
    };

    const handleDeleteSession = async (id: string) => {
        try {
            await deleteSession(id);
            setSessions(prev => prev.filter(s => s.id !== id));
        } catch (error) {
            console.error(error);
        }
    };

    return {
        sessions,
        loading,
        createSession: handleCreateSession,
        deleteSession: handleDeleteSession,
        refreshSessions: loadSessions
    };
}
