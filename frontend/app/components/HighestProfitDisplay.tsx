import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { ArbitrageOpportunityData } from '@/types/arbitrage';

interface HighestProfitData {
  profit: number;
  timestamp: Date;
  details: ArbitrageOpportunityData;
}

interface HighestProfitDisplayProps {
  highestProfit: HighestProfitData | null;
}

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value);
};

export default function HighestProfitDisplay({ highestProfit }: HighestProfitDisplayProps) {
  if (!highestProfit) return null;

  return (
    <View style={styles.highestProfitContainer}>
      <Text style={styles.highestProfitText}>Highest Profit: {formatCurrency(highestProfit.profit)}</Text>
      <Text style={styles.highestProfitTimestamp}>
        Recorded at: {highestProfit.timestamp.toLocaleTimeString()}
      </Text>
      <Text style={styles.exchangeInfo}>
        {highestProfit.details.crypto}: {highestProfit.details.lowest_price_exchange} ({highestProfit.details.buy_currency}) → {highestProfit.details.highest_price_exchange} ({highestProfit.details.sell_currency})
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  highestProfitContainer: {
    backgroundColor: '#1c1c1c',
    padding: 16,
    borderRadius: 8,
    marginBottom: 16,
  },
  highestProfitText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#00ff00',
    marginBottom: 8,
  },
  highestProfitTimestamp: {
    fontSize: 14,
    color: '#888',
    marginBottom: 4,
  },
  exchangeInfo: {
    fontSize: 16,
    color: '#fff',
  },
});