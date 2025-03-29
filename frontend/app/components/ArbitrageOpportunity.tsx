import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { ArbitrageData, ArbitrageOpportunityData } from '@/app/types/arbitrage';

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

const OpportunityCard = ({ opportunity }: { opportunity: ArbitrageOpportunityData }) => {
    const profitColor = opportunity.arbitrage_after_fees > 0 ? '#00ff00' : '#ff4c4c';

    return (
        <View style={styles.arbitrageContainer}>
            <View style={styles.headerContainer}>
                <Text style={styles.cryptoName}>{opportunity.crypto}</Text>
                <View style={styles.profitContainer}>
                    <Text style={styles.profitLabel}>Profit After Fees</Text>
                    <Text style={[styles.profitAmount, { color: profitColor }]}>
                        {formatCurrency(opportunity.arbitrage_after_fees)}
                    </Text>
                    <Text style={styles.profitPercentage}>
                        ({opportunity.profit_percentage.toFixed(2)}%)
                    </Text>
                </View>
            </View>
            
            <View style={styles.opportunityContainer}>
                <View style={styles.buySection}>
                    <Text style={styles.sectionTitle}>Buy At</Text>
                    <Text style={styles.exchangeName}>{opportunity.lowest_price_exchange}</Text>
                    <Text style={styles.price}>{formatCurrency(opportunity.lowest_price)}</Text>
                    <Text style={styles.currency}>{opportunity.buy_currency}</Text>
                </View>
                
                <View style={styles.sellSection}>
                    <Text style={styles.sectionTitle}>Sell At</Text>
                    <Text style={styles.exchangeName}>{opportunity.highest_price_exchange}</Text>
                    <Text style={styles.price}>{formatCurrency(opportunity.highest_price)}</Text>
                    <Text style={styles.currency}>{opportunity.sell_currency}</Text>
                </View>
            </View>

            <View style={styles.feesSection}>
                <Text style={styles.feesTitle}>Total Fees</Text>
                <Text style={styles.feesAmount}>{formatCurrency(opportunity.total_fees)}</Text>
            </View>
        </View>
    );
};

export default function ArbitrageOpportunity({ data }: ArbitrageOpportunityProps) {
    const sortedOpportunities = [...data.opportunities].sort((a, b) => 
        a.crypto.localeCompare(b.crypto)
    );

    return (
        <View style={styles.wrapper}>
            <ScrollView style={styles.container}>
                {sortedOpportunities.map((opportunity, index) => (
                    <OpportunityCard key={`${opportunity.crypto}-${index}`} opportunity={opportunity} />
                ))}
            </ScrollView>
        </View>
    );
}

const styles = StyleSheet.create({
    wrapper: {
        flex: 1,
        marginTop: 8,
    },
    container: {
        flex: 1,
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
    headerContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 16,
    },
    cryptoName: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#fff',
    },
    profitContainer: {
        alignItems: 'flex-end',
    },
    profitLabel: {
        fontSize: 14,
        color: '#888',
        marginBottom: 2,
    },
    opportunityContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: 16,
    },
    buySection: {
        flex: 1,
        alignItems: 'flex-start',
    },
    sellSection: {
        flex: 1,
        alignItems: 'flex-end',
    },
    sectionTitle: {
        fontSize: 16,
        color: '#888',
        marginBottom: 8,
    },
    exchangeName: {
        fontSize: 18,
        color: '#fff',
        marginBottom: 4,
    },
    price: {
        fontSize: 20,
        color: '#fff',
        fontWeight: '600',
    },
    currency: {
        fontSize: 14,
        color: '#888',
        marginTop: 2,
    },
    profitAmount: {
        fontSize: 20,
        fontWeight: 'bold',
    },
    profitPercentage: {
        fontSize: 14,
        color: '#888',
        marginTop: 2,
    },
    feesSection: {
        borderTopWidth: 1,
        borderTopColor: '#333',
        paddingTop: 12,
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    feesTitle: {
        fontSize: 16,
        color: '#888',
    },
    feesAmount: {
        fontSize: 16,
        color: '#ff4c4c',
    },
});