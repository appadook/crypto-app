export interface ArbitrageOpportunityData {
    crypto: string;
    lowest_price: number;
    lowest_price_exchange: string;
    highest_price: number;
    highest_price_exchange: string;
    buy_currency: string;
    sell_currency: string;
    spread_percentage: number;
    total_fees: number;
    arbitrage_after_fees: number;
    profit_percentage: number;
}

export interface ArbitrageData {
    status: 'success' | 'waiting' | 'no_arbitrage' | 'error';
    message?: string;
    opportunities: ArbitrageOpportunityData[];
}

export type { ArbitrageData, ArbitrageOpportunityData };