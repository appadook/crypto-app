import React, { useEffect, useState } from 'react';
import { View, ScrollView, Text, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { LinearGradient } from 'expo-linear-gradient';
import useWebSocket from '@/hooks/useWebSocket';
import { useHighestProfit } from '@/hooks/useHighestProfit';
import HighestProfitDisplay from '@/app/components/HighestProfitDisplay';
import ConnectionStatus from '@/app/components/ConnectionStatus';
import HelloMessage from '@/app/components/HelloMessage';
import ArbitrageOpportunity from '@/app/components/ArbitrageOpportunity';
import LoadingState from '@/app/components/LoadingState';
import StatusMessage from '@/app/components/StatusMessage';

export default function LiveArbitrageScreen() {
  const { arbitrageData, helloMessage, connectionStatus, lastUpdate, isDataFresh } = useWebSocket();
  const [lastHelloMessage, setLastHelloMessage] = useState<string | null>(null);
  const highestProfit = useHighestProfit(arbitrageData);

  useEffect(() => {
    if (helloMessage?.message) {
      setLastHelloMessage(helloMessage.message);
      console.log('[NewTab] Received new hello message:', helloMessage.message);
    }
  }, [helloMessage]);

  useEffect(() => {
    if (arbitrageData) {
      console.log('[LiveArbitrage] Arbitrage data updated:', {
        status: arbitrageData.status,
        timestamp: lastUpdate?.toISOString()
      });
    }
  }, [arbitrageData, lastUpdate]);

  const renderArbitrageContent = () => {
    if (!connectionStatus.isConnected) {
      return <LoadingState type="connection" />;
    }

    if (!arbitrageData) {
      return <LoadingState type="data" />;
    }

    if (arbitrageData.status === 'waiting' || arbitrageData.status === 'error' || arbitrageData.status === 'no_arbitrage') {
      return <StatusMessage type={arbitrageData.status} message={arbitrageData.message} />;
    }

    return <ArbitrageOpportunity data={arbitrageData} />;
  };

  return (
    <SafeAreaView style={styles.safeArea} edges={['top']}>
      <LinearGradient
        colors={['#000000', '#1A1A1A']}
        style={styles.container}
      >
        <View style={styles.header}>
          <Text style={styles.screenTitle}>Live Arbitrage</Text>
          <ConnectionStatus 
            isConnected={connectionStatus.isConnected}
            isDataFresh={isDataFresh}
            lastUpdate={lastUpdate}
          />
        </View>

        <HighestProfitDisplay highestProfit={highestProfit} />

        {connectionStatus.lastError && (
          <Text style={styles.errorText}>{connectionStatus.lastError}</Text>
        )}

        {helloMessage && (
          <HelloMessage 
            message={helloMessage.message}
            timestamp={helloMessage.timestamp}
          />
        )}

        {renderArbitrageContent()}
      </LinearGradient>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#000000',
  },
  container: {
    flex: 1,
    padding: 16,
    paddingTop: 8,
  },
  header: {
    marginBottom: 8,
  },
  screenTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#00FF9D',
    marginBottom: 8,
  },
  errorText: {
    color: '#ff4c4c',
    marginBottom: 12,
    padding: 12,
    backgroundColor: 'rgba(255, 76, 76, 0.1)',
    borderRadius: 8,
    overflow: 'hidden',
    borderLeftWidth: 4,
    borderLeftColor: '#ff4c4c',
  },
});