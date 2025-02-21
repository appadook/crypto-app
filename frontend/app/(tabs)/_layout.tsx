import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

export default function TabLayout() {
  const insets = useSafeAreaInsets();

  return (
    <Tabs
      screenOptions={{
        tabBarStyle: {
          backgroundColor: '#1A1A1A',
          borderTopColor: '#333',
          height: 60 + insets.bottom,
          paddingBottom: insets.bottom,
          borderTopWidth: 0.5,
        },
        tabBarActiveTintColor: '#00FF9D',
        tabBarInactiveTintColor: '#888',
        headerStyle: {
          backgroundColor: '#000000',
        },
        headerTitleStyle: {
          color: '#00FF9D',
        },
        headerTintColor: '#FFF',
        headerShadowVisible: false,
        headerTransparent: true,
      }}>
      <Tabs.Screen
        name="index"
        options={{
          headerShown: false,
          title: 'Home',
          tabBarIcon: ({ size, color }) => (
            <Ionicons name="home" size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="LiveArbitrage"
        options={{
          headerShown: false,
          title: 'Live Arbitrage',
          tabBarIcon: ({ size, color }) => (
            <Ionicons name="trending-up" size={size} color={color} />
          ),
        }}
      />
    </Tabs>
  );
}