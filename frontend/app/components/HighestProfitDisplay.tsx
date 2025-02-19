import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { HighestProfitData } from '@/hooks/useHighestProfit';

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

export function HighestProfitDisplay({ highestProfit }: HighestProfitDisplayProps) {
  if (!highestProfit) return null;

  return (
    <View style={styles.highestProfitContainer}>
      <Text style={styles.highestProfitText}>Highest Profit: {formatCurrency(highestProfit.profit)}</Text>
      <Text style={styles.highestProfitTimestamp}>
        Recorded at: {highestProfit.timestamp.toLocaleTimeString()}
      </Text>
      <Text style={styles.exchangeInfo}>
        {highestProfit.details.crypto}: {highestProfit.details.lowest_price_exchange} → {highestProfit.details.highest_price_exchange}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  highestProfitContainer: {
    padding: 16,
    backgroundColor: '#004d00',
    borderRadius: 8,
    marginBottom: 16,
  },
  highestProfitText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  highestProfitTimestamp: {
    fontSize: 12,
    color: '#cccccc',
    marginTop: 4,
  },
  exchangeInfo: {
    fontSize: 12,
    color: '#aaaaaa',
    marginTop: 4,
  }
});