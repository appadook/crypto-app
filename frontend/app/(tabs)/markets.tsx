import { useState } from 'react';
import { View, Text, StyleSheet, FlatList, TextInput, Pressable } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const CRYPTOCURRENCIES = [
  { id: '1', symbol: 'BTC', name: 'Bitcoin', price: 43250.45, change24h: 2.5 },
  { id: '2', symbol: 'ETH', name: 'Ethereum', price: 2250.34, change24h: -1.2 },
  { id: '3', symbol: 'SOL', name: 'Solana', price: 98.45, change24h: 5.7 },
  { id: '4', symbol: 'BNB', name: 'Binance Coin', price: 305.67, change24h: 0.8 },
  { id: '5', symbol: 'ADA', name: 'Cardano', price: 0.45, change24h: -2.3 },
];

export default function MarketsScreen() {
  const [searchQuery, setSearchQuery] = useState('');
  const [favorites, setFavorites] = useState<string[]>([]);

  const filteredCryptos = CRYPTOCURRENCIES.filter(
    crypto =>
      crypto.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      crypto.symbol.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const toggleFavorite = (id: string) => {
    setFavorites(prev =>
      prev.includes(id) ? prev.filter(fid => fid !== id) : [...prev, id]
    );
  };

  const renderCrypto = ({ item }: { item: typeof CRYPTOCURRENCIES[0] }) => (
    <Pressable style={styles.cryptoCard}>
      <View style={styles.cryptoInfo}>
        <Text style={styles.symbol}>{item.symbol}</Text>
        <Text style={styles.name}>{item.name}</Text>
      </View>
      
      <View style={styles.priceInfo}>
        <Text style={styles.price}>${item.price.toFixed(2)}</Text>
        <Text
          style={[
            styles.change,
            { color: item.change24h >= 0 ? '#00FF9D' : '#FF6B6B' },
          ]}>
          {item.change24h >= 0 ? '+' : ''}{item.change24h}%
        </Text>
      </View>
      
      <Pressable
        onPress={() => toggleFavorite(item.id)}
        style={styles.favoriteButton}>
        <Ionicons
          name={favorites.includes(item.id) ? 'star' : 'star-outline'}
          size={24}
          color={favorites.includes(item.id) ? '#FFD700' : '#666'}
        />
      </Pressable>
    </Pressable>
  );

  return (
    <View style={styles.container}>
      <View style={styles.searchContainer}>
        <Ionicons name="search" size={20} color="#666" style={styles.searchIcon} />
        <TextInput
          style={styles.searchInput}
          placeholder="Search cryptocurrencies..."
          placeholderTextColor="#666"
          value={searchQuery}
          onChangeText={setSearchQuery}
        />
      </View>
      
      <FlatList
        data={filteredCryptos}
        renderItem={renderCrypto}
        keyExtractor={item => item.id}
        contentContainerStyle={styles.list}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#121212',
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1E1E1E',
    margin: 16,
    borderRadius: 8,
    paddingHorizontal: 12,
  },
  searchIcon: {
    marginRight: 8,
  },
  searchInput: {
    flex: 1,
    color: '#FFF',
    paddingVertical: 12,
    fontSize: 16,
  },
  list: {
    padding: 16,
    paddingTop: 0,
  },
  cryptoCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1E1E1E',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#333',
  },
  cryptoInfo: {
    flex: 1,
  },
  symbol: {
    fontSize: 18,
    fontWeight: '600',
    color: '#FFF',
    marginBottom: 4,
  },
  name: {
    fontSize: 14,
    color: '#888',
  },
  priceInfo: {
    alignItems: 'flex-end',
    marginRight: 16,
  },
  price: {
    fontSize: 16,
    color: '#FFF',
    fontWeight: '500',
    marginBottom: 4,
  },
  change: {
    fontSize: 14,
    fontWeight: '500',
  },
  favoriteButton: {
    padding: 4,
  },
});