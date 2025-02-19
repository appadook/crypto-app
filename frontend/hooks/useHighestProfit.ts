import { useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { ArbitrageData } from '../app/types/arbitrage';

const STORAGE_KEY = 'highest_profit_data';

export interface HighestProfitData {
  profit: number;
  timestamp: Date;
  details: ArbitrageData;
}

export function useHighestProfit(currentArbitrageData: ArbitrageData | null) {
  const [highestProfit, setHighestProfit] = useState<HighestProfitData | null>(null);

  // Load saved highest profit on mount
  useEffect(() => {
    const loadSavedProfit = async () => {
      try {
        const savedData = await AsyncStorage.getItem(STORAGE_KEY);
        if (savedData) {
          const parsed = JSON.parse(savedData);
          parsed.timestamp = new Date(parsed.timestamp); // Convert timestamp back to Date
          setHighestProfit(parsed);
        }
      } catch (error: unknown) {
        console.error('Error loading highest profit:', error);
      }
    };
    loadSavedProfit();
  }, []);

  useEffect(() => {
    if (
      currentArbitrageData?.status === 'success' && 
      currentArbitrageData.arbitrage_after_fees && 
      (
        !highestProfit || 
        currentArbitrageData.arbitrage_after_fees > highestProfit.profit
      )
    ) {
      const newHighestProfit = {
        profit: currentArbitrageData.arbitrage_after_fees,
        timestamp: new Date(),
        details: { ...currentArbitrageData }
      };
      
      setHighestProfit(newHighestProfit);
      
      // Save to AsyncStorage
      AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(newHighestProfit))
        .catch((error: unknown) => console.error('Error saving highest profit:', error));
    }
  }, [currentArbitrageData, highestProfit]);

  return highestProfit;
}