import { useEffect, useState, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';
import { ArbitrageData, ArbitrageOpportunityData } from '../app/types/arbitrage';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:5001';

interface HelloMessage {
    message: string;
    timestamp: string;
}

interface ConnectionStatus {
    isConnected: boolean;
    lastError: string | null;
}

const useWebSocket = () => {
    // State
    const [socket, setSocket] = useState<Socket | null>(null);
    const [arbitrageData, setArbitrageData] = useState<ArbitrageData | null>(null);
    const [helloMessage, setHelloMessage] = useState<HelloMessage | null>(null);
    const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>({ 
        isConnected: false, 
        lastError: null 
    });
    const [lastUpdate, setLastUpdate] = useState<Date | null>(null);

    // Initialize socket connection
    useEffect(() => {
        console.log('[WebSocket] Initializing connection to:', BACKEND_URL);
        
        const newSocket = io(BACKEND_URL, {
            transports: ['websocket', 'polling'],
            autoConnect: true,
            reconnection: true,
            reconnectionAttempts: Infinity,
            reconnectionDelay: 1000,
            reconnectionDelayMax: 5000,
            timeout: 20000
        });

        // Connection handlers
        newSocket.on('connect', () => {
            console.log('[WebSocket] Connected with ID:', newSocket.id);
            setConnectionStatus({ isConnected: true, lastError: null });
            
            // Request initial data
            newSocket.emit('request_hello');
        });

        newSocket.on('disconnect', (reason) => {
            console.log('[WebSocket] Disconnected:', reason);
            setConnectionStatus({ isConnected: false, lastError: null });
            setHelloMessage(null);
            setArbitrageData(null);
        });

        newSocket.on('connect_error', (error) => {
            console.error('[WebSocket] Connection error:', error.message);
            setConnectionStatus({ 
                isConnected: false, 
                lastError: `Connection error: ${error.message}` 
            });
        });

        // Message handlers
        newSocket.on('hello', (data: HelloMessage) => {
            console.log('[WebSocket] Hello message received:', data);
            setHelloMessage(data);
            setLastUpdate(new Date());
        });

        newSocket.on('client_data', (data: { type: string; data: ArbitrageData; timestamp: string }) => {
            console.log('[WebSocket] Raw client data received:', JSON.stringify(data, null, 2));
            
            if (data.type === 'arbitrage_update') {
                console.log('[WebSocket] Processing arbitrage update...');
                setArbitrageData(data.data);
                setLastUpdate(new Date(data.timestamp));
                
                // Log detailed arbitrage information
                if (data.data.status === 'success') {
                    console.log('[WebSocket] Arbitrage opportunity found:', {
                        crypto: data.data.crypto,
                        buy: `${data.data.lowest_price_exchange} at ${data.data.lowest_price} ${data.data.buy_currency}`,
                        sell: `${data.data.highest_price_exchange} at ${data.data.highest_price} ${data.data.sell_currency}`,
                        profit: data.data.arbitrage_after_fees,
                        timestamp: data.timestamp
                    });
                } else {
                    console.log('[WebSocket] Non-success arbitrage status:', {
                        status: data.data.status,
                        message: data.data.message,
                        timestamp: data.timestamp
                    });
                }
            } else {
                console.log('[WebSocket] Unknown data type received:', data.type);
            }
        });

        // Store socket instance
        setSocket(newSocket);

        // Cleanup on unmount
        return () => {
            console.log('[WebSocket] Cleaning up connection');
            newSocket.disconnect();
        };
    }, []); // Empty dependency array - only run once on mount

    // Helper function to check if data is fresh (within last 30 seconds)
    const isDataFresh = lastUpdate ? (new Date().getTime() - lastUpdate.getTime()) < 3000 : false;

    return {
        arbitrageData,
        helloMessage,
        connectionStatus,
        lastUpdate,
        isDataFresh,
        socket
    };
};

export default useWebSocket;