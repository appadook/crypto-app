import { useEffect, useState, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';
import { ArbitrageData, ArbitrageOpportunityData } from '@/types/arbitrage';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:5001';

interface RawArbitrageData {
    status: 'success' | 'waiting' | 'no_arbitrage' | 'error';
    message?: string;
    crypto?: string;
    lowest_price?: number;
    lowest_price_exchange?: string;
    highest_price?: number;
    highest_price_exchange?: string;
    buy_currency?: string;
    sell_currency?: string;
    total_fees?: number;
    arbitrage_after_fees?: number;
    spread_percentage?: number;
    profit_percentage?: number;
}

interface HelloMessage {
    message: string;
    timestamp: string;
}

interface ConnectionStatus {
    isConnected: boolean;
    lastError: string | null;
}

const transformArbitrageData = (rawData: RawArbitrageData): ArbitrageData => {
    if (rawData.status !== 'success') {
        return {
            status: rawData.status,
            message: rawData.message,
            opportunities: []
        };
    }

    const opportunity: ArbitrageOpportunityData = {
        crypto: rawData.crypto!,
        lowest_price: rawData.lowest_price!,
        lowest_price_exchange: rawData.lowest_price_exchange!,
        highest_price: rawData.highest_price!,
        highest_price_exchange: rawData.highest_price_exchange!,
        buy_currency: rawData.buy_currency!,
        sell_currency: rawData.sell_currency!,
        spread_percentage: rawData.spread_percentage || 0,
        total_fees: rawData.total_fees!,
        arbitrage_after_fees: rawData.arbitrage_after_fees!,
        profit_percentage: rawData.profit_percentage || 0
    };

    return {
        status: 'success',
        opportunities: [opportunity]
    };
};

const useWebSocket = () => {
    const [socket, setSocket] = useState<Socket | null>(null);
    const [arbitrageData, setArbitrageData] = useState<ArbitrageData | null>(null);
    const [helloMessage, setHelloMessage] = useState<HelloMessage | null>(null);
    const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>({ 
        isConnected: false, 
        lastError: null 
    });
    const [lastUpdate, setLastUpdate] = useState<Date | null>(null);

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

        newSocket.on('connect', () => {
            console.log('[WebSocket] Connected with ID:', newSocket.id);
            setConnectionStatus({ isConnected: true, lastError: null });
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

        newSocket.on('hello', (data: HelloMessage) => {
            console.log('[WebSocket] Hello message received:', data);
            setHelloMessage(data);
            setLastUpdate(new Date());
        });

        newSocket.on('client_data', (data: { type: string; data: RawArbitrageData; timestamp: string }) => {
            console.log('[WebSocket] Raw client data received:', JSON.stringify(data, null, 2));
            
            if (data.type === 'arbitrage_update') {
                console.log('[WebSocket] Processing arbitrage update...');
                const transformedData = transformArbitrageData(data.data);
                setArbitrageData(transformedData);
                setLastUpdate(new Date(data.timestamp));
                
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

        setSocket(newSocket);

        return () => {
            console.log('[WebSocket] Cleaning up connection');
            newSocket.disconnect();
        };
    }, []);

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