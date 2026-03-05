export const checkHealth = async () => {
    try {
        const res = await fetch('/api/health');
        const data = await res.json();
        return data;
    } catch (error) {
        console.error("Health check failed:", error);
        return { status: "error" };
    }
};
