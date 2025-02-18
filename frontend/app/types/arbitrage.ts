interface ArbitrageData {
    status: 'success' | 'waiting' | 'no_arbitrage' | 'error';
    message?: string;
    crypto?: string;
    lowest_price?: number;
    lowest_price_exchange?: string;
    highest_price?: number;
    highest_price_exchange?: string;
    buy_currency?: string;
    sell_currency?: string;
    total_fees?: number;
    arbitrage_after_fees?: number;
}

export type { ArbitrageData };