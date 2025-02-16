import { useEffect, useState } from 'react';
import socket from '@/utilities/socketConnection';

const useWebSocket = () => {
    const [message, setMessage] = useState(null);
    const [connectionStatus, setConnectionStatus] = useState({ isConnected: false, lastError: null });

    useEffect(() => {
        // Update connection status
        setConnectionStatus({ isConnected: socket.connected, lastError: null });
        // Listen for messages from the server
        socket.on('client data', (data) => {
            setMessage(data);
        });

        // Update connection status on connect and disconnect
        socket.on('connect', () => {
            setConnectionStatus({ isConnected: true, lastError: null });
        });
        
        socket.on('disconnect', () => {
            setConnectionStatus({ isConnected: false, lastError: null });
        });

        // Handle errors
        socket.on('error', (error) => {
            setConnectionStatus({ isConnected: false, lastError: error.message });
        });

        // Cleanup on unmount
        return () => {
            socket.off('client data');
            socket.off('connect');
            socket.off('disconnect');
            socket.off('error');
        };
    }, []);

    return { message, connectionStatus };
};

export default useWebSocket;