import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface StatusMessageProps {
  type: 'waiting' | 'error' | 'no_arbitrage';
  message?: string;
}

export function StatusMessage({ type, message }: StatusMessageProps) {
  const getContent = () => {
    switch (type) {
      case 'waiting':
        return {
          containerStyle: styles.messageContainer,
          text: message || 'Waiting for data...',
          textStyle: styles.messageText
        };
      case 'error':
        return {
          containerStyle: [styles.messageContainer, styles.errorContainer],
          text: message || 'Error calculating arbitrage',
          textStyle: styles.errorText
        };
      case 'no_arbitrage':
        return {
          containerStyle: [styles.messageContainer, styles.warningContainer],
          text: 'No profitable arbitrage opportunities found',
          textStyle: styles.warningText
        };
    }
  };

  const content = getContent();

  return (
    <View style={content.containerStyle}>
      <Text style={content.textStyle}>{content.text}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  messageContainer: {
    padding: 16,
    marginBottom: 16,
    backgroundColor: '#002244',
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#0044ff',
  },
  messageText: {
    fontSize: 16,
    color: '#66aaff',
  },
  errorContainer: {
    backgroundColor: '#330000',
    borderLeftColor: '#ff4c4c',
  },
  errorText: {
    fontSize: 16,
    color: '#ff4c4c',
  },
  warningContainer: {
    backgroundColor: '#332200',
    borderLeftColor: '#ffaa00',
  },
  warningText: {
    fontSize: 16,
    color: '#ffaa00',
  },
});