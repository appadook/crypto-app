import { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, RefreshControl, Pressable } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import axios from 'axios';

type FiatPair = {
  fiat: string;
  price1: number;
  price2: number;
  spread: number;
};

type ArbitrageOpportunity = {
  id: string;
  cryptoSymbol: string;
  cryptoName: string;
  exchange1: string;
  exchange2: string;
  pairs: FiatPair[];
  bestSpread: number;
};

export default function ArbitrageScreen() {
  const [opportunities, setOpportunities] = useState<ArbitrageOpportunity[]>([]);
  const [refreshing, setRefreshing] = useState(false);
  const [expandedCard, setExpandedCard] = useState<string | null>(null);

  const fetchArbitrageOpportunities = async () => {
    try {
      // Simulated data - in production, you would fetch from real exchanges
      const mockData: ArbitrageOpportunity[] = [
        {
          id: '1',
          cryptoSymbol: 'BTC',
          cryptoName: 'Bitcoin',
          exchange1: 'Binance',
          exchange2: 'Coinbase',
          pairs: [
            { fiat: 'USD', price1: 43250.45, price2: 43350.78, spread: 0.23 },
            { fiat: 'EUR', price1: 39875.30, price2: 40012.45, spread: 0.34 },
            { fiat: 'GBP', price1: 34123.78, price2: 34278.90, spread: 0.45 }
          ],
          bestSpread: 0.45
        },
        {
          id: '2',
          cryptoSymbol: 'ETH',
          cryptoName: 'Ethereum',
          exchange1: 'Kraken',
          exchange2: 'Binance',
          pairs: [
            { fiat: 'USD', price1: 2250.34, price2: 2265.89, spread: 0.69 },
            { fiat: 'EUR', price1: 2075.45, price2: 2089.23, spread: 0.66 },
            { fiat: 'GBP', price1: 1789.56, price2: 1801.34, spread: 0.65 }
          ],
          bestSpread: 0.69
        },
        {
          id: '3',
          cryptoSymbol: 'SOL',
          cryptoName: 'Solana',
          exchange1: 'Binance',
          exchange2: 'Huobi',
          pairs: [
            { fiat: 'USD', price1: 98.45, price2: 99.12, spread: 0.68 },
            { fiat: 'EUR', price1: 90.78, price2: 91.45, spread: 0.73 },
            { fiat: 'GBP', price1: 77.89, price2: 78.56, spread: 0.86 }
          ],
          bestSpread: 0.86
        },
      ];
      setOpportunities(mockData);
    } catch (error) {
      console.error('Error fetching arbitrage opportunities:', error);
    }
  };

  useEffect(() => {
    fetchArbitrageOpportunities();
    const interval = setInterval(fetchArbitrageOpportunities, 30000);
    return () => clearInterval(interval);
  }, []);

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchArbitrageOpportunities();
    setRefreshing(false);
  };

  const toggleExpand = (id: string) => {
    setExpandedCard(expandedCard === id ? null : id);
  };

  const renderPairRow = (pair: FiatPair, item: ArbitrageOpportunity) => (
    <View style={styles.pairRow} key={pair.fiat}>
      <View style={styles.pairHeader}>
        <Text style={styles.fiatSymbol}>{pair.fiat}</Text>
        <Text style={[styles.pairSpread, { color: pair.spread >= 0.5 ? '#00FF9D' : '#FF6B6B' }]}>
          {pair.spread.toFixed(2)}% Spread
        </Text>
      </View>
      
      <View style={styles.tradingActions}>
        <View style={styles.actionCard}>
          <Text style={styles.actionTitle}>BUY {item.cryptoSymbol}</Text>
          <Text style={styles.exchangeName}>{item.exchange1}</Text>
          <Text style={styles.price}>{pair.fiat} {pair.price1.toFixed(2)}</Text>
        </View>
        
        <View style={styles.arrowContainer}>
          <Ionicons name="arrow-forward" size={20} color="#666" />
        </View>
        
        <View style={styles.actionCard}>
          <Text style={styles.actionTitle}>SELL {item.cryptoSymbol}</Text>
          <Text style={styles.exchangeName}>{item.exchange2}</Text>
          <Text style={styles.price}>{pair.fiat} {pair.price2.toFixed(2)}</Text>
        </View>
      </View>
    </View>
  );

  const renderOpportunity = ({ item }: { item: ArbitrageOpportunity }) => (
    <Pressable style={styles.card} onPress={() => toggleExpand(item.id)}>
      <View style={styles.cardHeader}>
        <View style={styles.cryptoInfo}>
          <Text style={styles.symbol}>{item.cryptoSymbol}</Text>
          <Text style={styles.cryptoName}>{item.cryptoName}</Text>
        </View>
        <Text style={[styles.spread, { color: item.bestSpread >= 0.5 ? '#00FF9D' : '#FF6B6B' }]}>
          Best: {item.bestSpread.toFixed(2)}%
        </Text>
      </View>

      {expandedCard === item.id && (
        <View style={styles.pairsContainer}>
          {item.pairs.map(pair => renderPairRow(pair, item))}
        </View>
      )}
      
      <View style={styles.expandButton}>
        <Ionicons 
          name={expandedCard === item.id ? "chevron-up" : "chevron-down"} 
          size={20} 
          color="#666" 
        />
      </View>
    </Pressable>
  );

  return (
    <View style={styles.container}>
      <FlatList
        data={opportunities}
        renderItem={renderOpportunity}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.list}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            tintColor="#00FF9D"
          />
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#121212',
  },
  list: {
    padding: 16,
  },
  card: {
    backgroundColor: '#1E1E1E',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#333',
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  cryptoInfo: {
    flex: 1,
  },
  symbol: {
    fontSize: 20,
    fontWeight: '600',
    color: '#FFF',
  },
  cryptoName: {
    fontSize: 14,
    color: '#888',
    marginTop: 2,
  },
  spread: {
    fontSize: 16,
    fontWeight: '600',
  },
  pairsContainer: {
    marginTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#333',
    paddingTop: 12,
  },
  pairRow: {
    marginBottom: 16,
  },
  pairHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  fiatSymbol: {
    fontSize: 16,
    color: '#FFF',
    fontWeight: '500',
  },
  pairSpread: {
    fontSize: 14,
    fontWeight: '500',
  },
  tradingActions: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  actionCard: {
    flex: 1,
    backgroundColor: '#252525',
    borderRadius: 8,
    padding: 12,
    borderWidth: 1,
    borderColor: '#333',
  },
  actionTitle: {
    fontSize: 12,
    color: '#888',
    marginBottom: 4,
  },
  exchangeName: {
    fontSize: 14,
    color: '#FFF',
    fontWeight: '500',
    marginBottom: 4,
  },
  price: {
    fontSize: 16,
    color: '#00FF9D',
    fontWeight: '600',
  },
  arrowContainer: {
    paddingHorizontal: 12,
  },
  expandButton: {
    alignItems: 'center',
    marginTop: 8,
  },
});