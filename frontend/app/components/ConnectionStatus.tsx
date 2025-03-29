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
                    {!isDataFresh && isConnected && (
                        <Text style={styles.staleDataText}> (Stale)</Text>
                    )}
                </Text>
            </View>
            {lastUpdate && (
                <Text style={[
                    styles.lastUpdateText,
                    !isDataFresh && styles.staleLastUpdateText
                ]}>
                    Updated: {lastUpdate.toLocaleTimeString()}
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
        marginBottom: 8,
        padding: 6,
        backgroundColor: '#1c1c1c',
        borderRadius: 6,
        elevation: 2,
        shadowColor: '#fff',
        shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.1,
        shadowRadius: 2,
    },
    statusContainer: {
        flexDirection: 'row',
        alignItems: 'center',
    },
    statusIndicator: {
        width: 8,
        height: 8,
        borderRadius: 4,
        marginRight: 6,
    },
    statusText: {
        fontSize: 14,
        fontWeight: '500',
        color: '#ffffff',
    },
    lastUpdateText: {
        fontSize: 12,
        color: '#cccccc',
    },
    staleDataText: {
        color: '#ffaa00',
        fontSize: 14,
    },
    staleLastUpdateText: {
        color: '#ffaa00',
    },
});