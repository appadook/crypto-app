import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { ArbitrageData } from '@/app/types/arbitrage';

interface ArbitrageOpportunityProps {
  data: ArbitrageData;
}

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value);
};

export function ArbitrageOpportunity({ data }: ArbitrageOpportunityProps) {
  const profitColor = (data.arbitrage_after_fees ?? 0) > 0 ? '#00ff00' : '#ff4c4c';

  return (
    <View style={styles.arbitrageContainer}>
      <Text style={styles.arbitrageTitle}>Arbitrage Opportunity Found</Text>
      <Text style={styles.cryptoName}>{data.crypto}</Text>
      
      <View style={styles.opportunityContainer}>
        <View style={styles.buySection}>
          <Text style={styles.sectionTitle}>Buy At</Text>
          <Text style={styles.exchangeName}>{data.lowest_price_exchange}</Text>
          <Text style={styles.price}>{formatCurrency(data.lowest_price || 0)}</Text>
          <Text style={styles.currency}>{data.buy_currency}</Text>
        </View>
        
        <View style={styles.sellSection}>
          <Text style={styles.sectionTitle}>Sell At</Text>
          <Text style={styles.exchangeName}>{data.highest_price_exchange}</Text>
          <Text style={styles.price}>{formatCurrency(data.highest_price || 0)}</Text>
          <Text style={styles.currency}>{data.sell_currency}</Text>
        </View>
      </View>

      <View style={styles.profitSection}>
        <Text style={styles.feesText}>Total Fees: {formatCurrency(data.total_fees || 0)}</Text>
        <Text style={[styles.profitText, { color: profitColor }]}>
          Profit after Fees: {formatCurrency(data.arbitrage_after_fees || 0)}
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
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
  },
});