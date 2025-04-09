import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_prices_in_usd(file_path):
    """Plot prices in USD across exchanges over time."""
    # Load the CSV file
    df = pd.read_csv(file_path)

    # Filter rows for trading_pair == BTC/USD
    df = df[df['trading_pair'] == 'BTC/USD']

    # Convert timestamp to datetime
    df['datetime'] = pd.to_datetime(df['timestamp'])

    # Filter columns for USD prices
    usd_columns = ['BINANCE_price', 'COINBASE_price', 'KRAKEN_price']

    # Check if required columns exist
    for col in usd_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Plot the data
    plt.figure(figsize=(12, 6))
    for col in usd_columns:
        plt.plot(df['datetime'], df[col], label=col.split('_')[0])

    # Format the plot
    plt.title('Cryptocurrency Prices in USD Across Exchanges')
    plt.xlabel('Time')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    # Format the x-axis for better readability
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)

    # Show the plot
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Plot USD prices across exchanges.")
    parser.add_argument('file_path', help="Path to the CSV file containing price data.")
    args = parser.parse_args()

    plot_prices_in_usd(args.file_path)
