import { useState } from 'react';
import { View, Text, StyleSheet, Switch, Pressable } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

type Exchange = {
  id: string;
  name: string;
  enabled: boolean;
};

export default function SettingsScreen() {
  const [exchanges, setExchanges] = useState<Exchange[]>([
    { id: '1', name: 'Binance', enabled: true },
    { id: '2', name: 'Coinbase', enabled: true },
    { id: '3', name: 'Kraken', enabled: true },
    { id: '4', name: 'Huobi', enabled: false },
    { id: '5', name: 'KuCoin', enabled: false },
  ]);
  
  const [notifications, setNotifications] = useState({
    priceAlerts: true,
    arbitrageAlerts: true,
    newsAlerts: false,
  });

  const toggleExchange = (id: string) => {
    setExchanges(prev =>
      prev.map(exchange =>
        exchange.id === id
          ? { ...exchange, enabled: !exchange.enabled }
          : exchange
      )
    );
  };

  const renderSection = (title: string) => (
    <Text style={styles.sectionTitle}>{title}</Text>
  );

  const renderSettingItem = (
    title: string,
    value: boolean,
    onToggle: () => void,
    icon: string
  ) => (
    <View style={styles.settingItem}>
      <View style={styles.settingLeft}>
        <Ionicons name={icon as any} size={24} color="#00FF9D" style={styles.settingIcon} />
        <Text style={styles.settingText}>{title}</Text>
      </View>
      <Switch
        value={value}
        onValueChange={onToggle}
        trackColor={{ false: '#333', true: '#00FF9D' }}
        thumbColor="#FFF"
      />
    </View>
  );

  return (
    <View style={styles.container}>
      {renderSection('Exchanges')}
      {exchanges.map(exchange => (
        <Pressable
          key={exchange.id}
          style={styles.settingItem}
          onPress={() => toggleExchange(exchange.id)}>
          <View style={styles.settingLeft}>
            <Ionicons
              name="business-outline"
              size={24}
              color="#00FF9D"
              style={styles.settingIcon}
            />
            <Text style={styles.settingText}>{exchange.name}</Text>
          </View>
          <Switch
            value={exchange.enabled}
            onValueChange={() => toggleExchange(exchange.id)}
            trackColor={{ false: '#333', true: '#00FF9D' }}
            thumbColor="#FFF"
          />
        </Pressable>
      ))}

      {renderSection('Notifications')}
      {renderSettingItem(
        'Price Alerts',
        notifications.priceAlerts,
        () => setNotifications(prev => ({ ...prev, priceAlerts: !prev.priceAlerts })),
        'notifications-outline'
      )}
      {renderSettingItem(
        'Arbitrage Alerts',
        notifications.arbitrageAlerts,
        () => setNotifications(prev => ({ ...prev, arbitrageAlerts: !prev.arbitrageAlerts })),
        'trending-up'
      )}
      {renderSettingItem(
        'News Alerts',
        notifications.newsAlerts,
        () => setNotifications(prev => ({ ...prev, newsAlerts: !prev.newsAlerts })),
        'newspaper-outline'
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#121212',
    padding: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#FFF',
    marginTop: 24,
    marginBottom: 16,
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#1E1E1E',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#333',
  },
  settingLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  settingIcon: {
    marginRight: 12,
  },
  settingText: {
    fontSize: 16,
    color: '#FFF',
  },
});