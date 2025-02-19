import React from 'react';
import { View, Text, ActivityIndicator, StyleSheet } from 'react-native';

interface LoadingStateProps {
  type: 'connection' | 'data';
}

export function LoadingState({ type }: LoadingStateProps) {
  const isConnection = type === 'connection';
  
  return (
    <View style={styles.waitingContainer}>
      <ActivityIndicator size="large" color={isConnection ? "#F44336" : "#2196F3"} />
      <Text style={[styles.waitingText, isConnection && { color: '#F44336' }]}>
        {isConnection ? 'Waiting for connection...' : 'Waiting for arbitrage data...'}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  waitingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    minHeight: 200,
  },
  waitingText: {
    marginTop: 12,
    fontSize: 16,
    color: '#cccccc',
  },
});