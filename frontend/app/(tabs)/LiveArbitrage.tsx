import React, { useEffect, useState } from 'react';
import { View, ScrollView, Text, StyleSheet } from 'react-native';
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
    <View style={styles.container}>
      <HighestProfitDisplay highestProfit={highestProfit} />
      
      <ConnectionStatus 
        isConnected={connectionStatus.isConnected}
        isDataFresh={isDataFresh}
        lastUpdate={lastUpdate}
      />

      {connectionStatus.lastError && (
        <Text style={styles.errorText}>{connectionStatus.lastError}</Text>
      )}

      {helloMessage && (
        <HelloMessage 
          message={helloMessage.message}
          timestamp={helloMessage.timestamp}
        />
      )}

      <ScrollView style={styles.scrollView}>
        {renderArbitrageContent()}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#000000',
  },
  scrollView: {
    flex: 1,
    backgroundColor: '#1c1c1c',
    borderRadius: 8,
    padding: 8,
  },
  errorText: {
    color: '#ff4c4c',
    marginBottom: 16,
    padding: 8,
    backgroundColor: '#330000',
    borderRadius: 4,
  },
});