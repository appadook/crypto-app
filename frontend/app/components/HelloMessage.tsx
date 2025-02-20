import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface HelloMessageProps {
  message: string;
  timestamp: string | number | Date;
}

export default function HelloMessage({ message, timestamp }: HelloMessageProps) {
  return (
    <View style={styles.helloContainer}>
      <Text style={styles.helloText}>{message}</Text>
      <Text style={styles.helloTimestamp}>
        Received at: {new Date(timestamp).toLocaleTimeString()}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  helloContainer: {
    padding: 16,
    marginBottom: 16,
    backgroundColor: '#003300',
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#00ff00',
  },
  helloText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#00ff00',
    marginBottom: 8,
  },
  helloTimestamp: {
    fontSize: 12,
    color: '#999999',
  },
});