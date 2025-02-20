import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface ConnectionStatusProps {
  isConnected: boolean;
  isDataFresh: boolean;
  lastUpdate: Date | null;
}

export default function ConnectionStatus({ isConnected, isDataFresh, lastUpdate }: ConnectionStatusProps) {
  return (
    <View style={styles.statusBar}>
      <View style={styles.statusContainer}>
        <View style={[
          styles.statusIndicator,
          { backgroundColor: isConnected ? '#4CAF50' : '#F44336' }
        ]} />
        <Text style={styles.statusText}>
          {isConnected ? 'Connected' : 'Disconnected'}
        </Text>
        {!isDataFresh && isConnected && (
          <Text style={styles.staleDataText}> (Stale Data)</Text>
        )}
      </View>
      {lastUpdate && (
        <Text style={[
          styles.lastUpdateText,
          !isDataFresh && styles.staleLastUpdateText
        ]}>
          Last Update: {lastUpdate.toLocaleTimeString()}
        </Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  statusBar: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
    padding: 8,
    backgroundColor: '#1c1c1c',
    borderRadius: 8,
    elevation: 2,
    shadowColor: '#fff',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
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
    color: '#ffffff',
  },
  lastUpdateText: {
    fontSize: 12,
    color: '#cccccc',
  },
  staleDataText: {
    color: '#ffaa00',
    marginLeft: 8,
    fontSize: 14,
  },
  staleLastUpdateText: {
    color: '#ffaa00',
  },
});