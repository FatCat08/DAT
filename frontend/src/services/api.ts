const BASE_URL = '/api';

export const checkHealth = async () => {
    try {
        const res = await fetch(`${BASE_URL}/health`);
        const data = await res.json();
        return data;
    } catch (error) {
        console.error("Health check failed:", error);
        return { status: "error" };
    }
};

export const fetchSessions = async () => {
    const res = await fetch(`${BASE_URL}/sessions`);
    if (!res.ok) throw new Error('Failed to fetch sessions');
    return res.json();
};

export const createSession = async (title = 'New Chat') => {
    const res = await fetch(`${BASE_URL}/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title })
    });
    if (!res.ok) throw new Error('Failed to create session');
    return res.json();
};

export const deleteSession = async (sessionId: string) => {
    const res = await fetch(`${BASE_URL}/sessions/${sessionId}`, {
        method: 'DELETE'
    });
    if (!res.ok) throw new Error('Failed to delete session');
    return res.json();
};

export const fetchSessionDetail = async (sessionId: string) => {
    const res = await fetch(`${BASE_URL}/sessions/${sessionId}`);
    if (!res.ok) throw new Error('Failed to fetch session detail');
    return res.json();
};

export const fetchDatabaseSchema = async () => {
    const res = await fetch(`${BASE_URL}/db/tables`);
    if (!res.ok) throw new Error('Failed to fetch DB schema');
    return res.json();
};
