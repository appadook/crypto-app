import { useState, useEffect } from 'react';
import { ArbitrageData } from '../app/types/arbitrage';

interface HighestProfitData {
  profit: number;
  timestamp: Date;
  details: ArbitrageData;
}

export function useHighestProfit(currentArbitrageData: ArbitrageData | null) {
  const [highestProfit, setHighestProfit] = useState<HighestProfitData | null>(null);

  useEffect(() => {
    if (
      currentArbitrageData?.status === 'success' && 
      currentArbitrageData.arbitrage_after_fees && 
      (
        !highestProfit || 
        currentArbitrageData.arbitrage_after_fees > highestProfit.profit
      )
    ) {
      setHighestProfit({
        profit: currentArbitrageData.arbitrage_after_fees,
        timestamp: new Date(),
        details: { ...currentArbitrageData }
      });
    }
  }, [currentArbitrageData, highestProfit]);

  return highestProfit;
}