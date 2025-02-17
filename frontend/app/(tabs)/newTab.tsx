import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, StyleSheet, ActivityIndicator } from 'react-native';
import useWebSocket from '@/hooks/useWebSocket';

export default function NewTabScreen() {
  const { arbitrageData, helloMessage, connectionStatus, lastUpdate, isDataFresh } = useWebSocket();
  const [lastHelloMessage, setLastHelloMessage] = useState<string | null>(null);

  // Update lastHelloMessage when helloMessage changes
  useEffect(() => {
    if (helloMessage?.message) {
      setLastHelloMessage(helloMessage.message);
      console.log('[NewTab] Received new hello message:', helloMessage.message);
    }
  }, [helloMessage]);

  // Log when arbitrage data changes
  useEffect(() => {
    if (arbitrageData) {
      console.log('[NewTab] Arbitrage data updated:', {
        status: arbitrageData.status,
        timestamp: lastUpdate?.toISOString()
      });
    }
  }, [arbitrageData, lastUpdate]);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(value);
  };

  const renderArbitrageContent = () => {
    if (!connectionStatus.isConnected) {
      return (
        <View style={styles.waitingContainer}>
          <ActivityIndicator size="large" color="#F44336" />
          <Text style={[styles.waitingText, { color: '#F44336' }]}>
            Waiting for connection...
          </Text>
        </View>
      );
    }

    if (!arbitrageData) {
      return (
        <View style={styles.waitingContainer}>
          <ActivityIndicator size="large" color="#2196F3" />
          <Text style={styles.waitingText}>
            Waiting for arbitrage data...
          </Text>
        </View>
      );
    }

    if (arbitrageData.status === 'waiting') {
      return (
        <View style={styles.messageContainer}>
          <Text style={styles.messageText}>{arbitrageData.message || 'Waiting for data...'}</Text>
        </View>
      );
    }

    if (arbitrageData.status === 'error') {
      return (
        <View style={[styles.messageContainer, styles.errorContainer]}>
          <Text style={styles.errorText}>{arbitrageData.message || 'Error calculating arbitrage'}</Text>
        </View>
      );
    }

    if (arbitrageData.status === 'no_arbitrage') {
      return (
        <View style={[styles.messageContainer, styles.warningContainer]}>
          <Text style={styles.warningText}>No profitable arbitrage opportunities found</Text>
        </View>
      );
    }

    return (
      <View style={styles.arbitrageContainer}>
        <Text style={styles.arbitrageTitle}>Arbitrage Opportunity Found</Text>
        <Text style={styles.cryptoName}>{arbitrageData.crypto}</Text>
        
        <View style={styles.opportunityContainer}>
          <View style={styles.buySection}>
            <Text style={styles.sectionTitle}>Buy At</Text>
            <Text style={styles.exchangeName}>{arbitrageData.lowest_price_exchange}</Text>
            <Text style={styles.price}>{formatCurrency(arbitrageData.lowest_price || 0)}</Text>
            <Text style={styles.currency}>{arbitrageData.buy_currency}</Text>
          </View>
          
          <View style={styles.sellSection}>
            <Text style={styles.sectionTitle}>Sell At</Text>
            <Text style={styles.exchangeName}>{arbitrageData.highest_price_exchange}</Text>
            <Text style={styles.price}>{formatCurrency(arbitrageData.highest_price || 0)}</Text>
            <Text style={styles.currency}>{arbitrageData.sell_currency}</Text>
          </View>
        </View>

        <View style={styles.profitSection}>
          <Text style={styles.feesText}>Total Fees: {formatCurrency(arbitrageData.total_fees || 0)}</Text>
          <Text style={styles.profitText}>
            Profit after Fees: {formatCurrency(arbitrageData.arbitrage_after_fees || 0)}
          </Text>
        </View>
      </View>
    );
  };

  return (
    <View style={styles.container}>
      {/* Connection Status */}
      <View style={styles.statusBar}>
        <View style={styles.statusContainer}>
          <View style={[
            styles.statusIndicator,
            { backgroundColor: connectionStatus.isConnected ? '#4CAF50' : '#F44336' }
          ]} />
          <Text style={styles.statusText}>
            {connectionStatus.isConnected ? 'Connected' : 'Disconnected'}
          </Text>
          {!isDataFresh && connectionStatus.isConnected && (
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

      {/* Error Message */}
      {connectionStatus.lastError && (
        <Text style={styles.errorText}>Error: {connectionStatus.lastError}</Text>
      )}

      {/* Hello Message */}
      {helloMessage && (
        <View style={styles.helloContainer}>
          <Text style={styles.helloText}>{helloMessage.message}</Text>
          <Text style={styles.helloTimestamp}>
            Received at: {new Date(helloMessage.timestamp).toLocaleTimeString()}
          </Text>
        </View>
      )}

      {/* Arbitrage Data */}
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
    backgroundColor: '#f5f5f5',
  },
  statusBar: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
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
  lastUpdateText: {
    fontSize: 12,
    color: '#666',
  },
  errorText: {
    color: '#F44336',
    marginBottom: 16,
    padding: 8,
    backgroundColor: '#FFEBEE',
    borderRadius: 4,
  },
  helloContainer: {
    padding: 16,
    marginBottom: 16,
    backgroundColor: '#E8F5E9',
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#4CAF50',
  },
  helloText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 8,
  },
  helloTimestamp: {
    fontSize: 12,
    color: '#666',
  },
  scrollView: {
    flex: 1,
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 8,
  },
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
    color: '#666',
  },
  messageContainer: {
    padding: 16,
    marginBottom: 16,
    backgroundColor: '#E3F2FD',
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#2196F3',
  },
  messageText: {
    fontSize: 16,
    color: '#1976D2',
  },
  errorContainer: {
    backgroundColor: '#FFEBEE',
    borderLeftColor: '#F44336',
  },
  warningContainer: {
    backgroundColor: '#FFF3E0',
    borderLeftColor: '#FF9800',
  },
  warningText: {
    fontSize: 16,
    color: '#F57C00',
  },
  arbitrageContainer: {
    padding: 16,
    backgroundColor: '#E8F5E9',
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#4CAF50',
  },
  arbitrageTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 8,
  },
  cryptoName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1976D2',
    marginBottom: 16,
  },
  opportunityContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  buySection: {
    flex: 1,
    padding: 12,
    backgroundColor: '#E3F2FD',
    borderRadius: 8,
    marginRight: 8,
  },
  sellSection: {
    flex: 1,
    padding: 12,
    backgroundColor: '#E8EAF6',
    borderRadius: 8,
    marginLeft: 8,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#666',
    marginBottom: 4,
  },
  exchangeName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1976D2',
    marginBottom: 4,
  },
  price: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 4,
  },
  currency: {
    fontSize: 14,
    color: '#666',
  },
  profitSection: {
    padding: 12,
    backgroundColor: '#F5F5F5',
    borderRadius: 8,
  },
  feesText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 4,
  },
  profitText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2E7D32',
  },
  staleDataText: {
    color: '#FFA000',
    marginLeft: 8,
    fontSize: 14,
  },
  staleLastUpdateText: {
    color: '#FFA000',
  },
});