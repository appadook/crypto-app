import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, StyleSheet, ActivityIndicator } from 'react-native';
import useWebSocket from '@/hooks/useWebSocket';

export default function NewTabScreen() {
  const { message, connectionStatus } = useWebSocket(); // Use the hook to get message and connection status
  const [messages, setMessages] = useState<any[]>([]);

  // Update messages based on the message received from the WebSocket
  useEffect(() => {
    if (message) {
      setMessages((prevMessages: any) => [message, ...prevMessages].slice(0, 50)); // Keep last 50 messages
    }
  }, [message]);

  return (
    <View style={styles.container}>
      {/* Connection Status */}
      <View style={styles.statusContainer}>
        <View style={[
          styles.statusIndicator,
          { backgroundColor: connectionStatus.isConnected ? '#4CAF50' : '#F44336' }
        ]} />
        <Text style={styles.statusText}>
          {connectionStatus.isConnected ? 'Connected' : 'Disconnected'}
        </Text>
      </View>

      {/* Error Message */}
      {connectionStatus.lastError && (
        <Text style={styles.errorText}>Error: {connectionStatus.lastError}</Text>
      )}

      {/* Data Display */}
      <ScrollView style={styles.scrollView}>
        {messages.length > 0 ? (
          messages.map((msg, index) => (
            <View key={index} style={styles.messageContainer}>
              <Text style={styles.messageText}>
                {JSON.stringify(msg, null, 2)}
              </Text>
              <Text style={styles.timestamp}>
                {new Date().toLocaleTimeString()}
              </Text>
            </View>
          ))
        ) : (
          <View style={styles.waitingContainer}>
            <ActivityIndicator size="large" color="#0000ff" />
            <Text style={styles.waitingText}>Waiting for updates...</Text>
          </View>
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#f5f5f5',
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
    padding: 8,
    backgroundColor: '#fff',
    borderRadius: 8,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  statusIndicator: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 8,
  },
  statusText: {
    fontSize: 16,
    fontWeight: '600',
  },
  errorText: {
    color: '#F44336',
    marginBottom: 16,
    padding: 8,
    backgroundColor: '#FFEBEE',
    borderRadius: 4,
  },
  scrollView: {
    flex: 1,
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 8,
  },
  messageContainer: {
    padding: 12,
    marginBottom: 8,
    backgroundColor: '#E3F2FD',
    borderRadius: 4,
    borderLeftWidth: 4,
    borderLeftColor: '#2196F3',
  },
  messageText: {
    fontSize: 14,
    fontFamily: 'monospace',
  },
  timestamp: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  waitingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  waitingText: {
    marginTop: 12,
    fontSize: 16,
    color: '#666',
  },
});