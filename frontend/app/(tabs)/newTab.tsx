import React, { useEffect, useState } from 'react';
import { View, Text } from 'react-native';
import socket from '@/utilities/socketConnection';

export default function NewTabScreen() {
  const [message, setMessage] = useState<string>('');

  useEffect(() => {
    // Handle custom socket events
    const handleClientData = (data: any) => {
      console.log('Received data:', data);
      setMessage(JSON.stringify(data));
    };

    socket.on('client data', handleClientData);

    // Clean up the listeners on unmount
    return () => {
      socket.off('client data', handleClientData);
    };
  }, []);

  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text>New Tab screen</Text>
      <Text>{message ? `Data: ${message}` : 'Waiting for data...'}</Text>
    </View>
  );
}