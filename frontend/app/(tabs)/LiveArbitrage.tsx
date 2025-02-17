import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, StyleSheet, ActivityIndicator } from 'react-native';
import useWebSocket from '@/hooks/useWebSocket';

export default function LiveArbitrageScreen() {
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

  const profitColor = arbitrageData && typeof arbitrageData.arbitrage_after_fees === 'number' && arbitrageData.arbitrage_after_fees > 0 ? '#00ff00' : '#ff4c4c';

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
          <Text style={[styles.profitText, { color: profitColor }]}>Profit after Fees: {formatCurrency(arbitrageData.arbitrage_after_fees || 0)}</Text>
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
    backgroundColor: '#000000',
  },
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
  errorText: {
    color: '#ff4c4c',
    marginBottom: 16,
    padding: 8,
    backgroundColor: '#330000',
    borderRadius: 4,
  },
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
  scrollView: {
    flex: 1,
    backgroundColor: '#1c1c1c',
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
    color: '#cccccc',
  },
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
  warningContainer: {
    backgroundColor: '#332200',
    borderLeftColor: '#ffaa00',
  },
  warningText: {
    fontSize: 16,
    color: '#ffaa00',
  },
  arbitrageContainer: {
    padding: 16,
    backgroundColor: '#1c1c1c',
    borderRadius: 8,
    marginBottom: 16,
    shadowColor: '#fff',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  arbitrageTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 8,
  },
  cryptoName: {
    fontSize: 18,
    color: '#cccccc',
    marginBottom: 8,
  },
  opportunityContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  buySection: {
    flex: 1,
    padding: 8,
    backgroundColor: '#003300',
    borderRadius: 8,
    marginRight: 8,
  },
  sellSection: {
    flex: 1,
    padding: 8,
    backgroundColor: '#330000',
    borderRadius: 8,
    marginLeft: 8,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 4,
  },
  exchangeName: {
    fontSize: 14,
    color: '#aaaaaa',
    marginBottom: 4,
  },
  price: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  currency: {
    fontSize: 14,
    color: '#999999',
  },
  profitSection: {
    padding: 8,
    backgroundColor: '#332200',
    borderRadius: 8,
  },
  feesText: {
    fontSize: 14,
    color: '#ffaa00',
    marginBottom: 4,
  },
  profitText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#00ff00',
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