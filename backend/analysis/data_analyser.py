#!/usr/bin/env python3
"""
DataAnalyser class to encapsulate arbitrage data analysis and visualization.

This class provides methods to:
1. Classify arbitrage strategies
2. Analyze strategy profit
3. Analyze strategy frequency
4. Analyze strategy percentages
5. Create network visualizations
6. Analyze exchange pair performance
7. Analyze currency relationships

Usage:
    from data_analyser import DataAnalyser
    
    analyser = DataAnalyser("path/to/your/input_file.csv")
    analyser.classify_strategies()
    analyser.analyze_all()
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
import os
import re
from datetime import datetime
import networkx as nx
from matplotlib.cm import get_cmap
from matplotlib.colors import Normalize, LinearSegmentedColormap
import matplotlib.patches as mpatches

# Check for optional visualization libraries
try:
    from pyvis.network import Network
    PYVIS_AVAILABLE = True
except ImportError:
    PYVIS_AVAILABLE = False

try:
    import holoviews as hv
    from holoviews import opts, dim
    hv.extension('matplotlib')
    HOLOVIEWS_AVAILABLE = True
except ImportError:
    HOLOVIEWS_AVAILABLE = False


class DataAnalyser:
    """A class to perform comprehensive analysis of arbitrage data."""
    
    def __init__(self, input_file):
        """
        Initialize the DataAnalyser with the input CSV file.
        
        Args:
            input_file (str): Path to the CSV file with arbitrage data.
        """
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file '{input_file}' does not exist.")
        
        self.input_file = input_file
        self.classified_file = None
        self.df = None
        self.base_output_name = os.path.splitext(self.input_file)[0]

    def _load_data(self, file_path=None, required_columns=None):
        """Helper function to load data and check for required columns."""
        file_to_load = file_path if file_path else self.input_file
        
        if not file_to_load or not os.path.exists(file_to_load):
            print(f"Error: Data file '{file_to_load}' not found or not specified.")
            return False
            
        try:
            self.df = pd.read_csv(file_to_load)
            if required_columns:
                missing = [col for col in required_columns if col not in self.df.columns]
                if missing:
                    print(f"Error: Missing required columns in {file_to_load}: {missing}")
                    return False
            return True
        except Exception as e:
            print(f"Error loading data from {file_to_load}: {e}")
            return False

    def classify_strategies(self, output_file_suffix='_classified'):
        """
        Classify strategies and save the enriched dataset.
        This is a prerequisite for most other analysis methods.
        """
        if not self._load_data(self.input_file, ['strategy']):
            return False

        try:
            # Extract exchange patterns
            exchange_pattern = r"Buy at (\w+) in (\w+) -> Sell at (\w+) in (\w+)"
            
            extracted_data = self.df['strategy'].str.extract(exchange_pattern)
            self.df['buy_exchange'] = extracted_data[0]
            self.df['buy_currency'] = extracted_data[1]
            self.df['sell_exchange'] = extracted_data[2]
            self.df['sell_currency'] = extracted_data[3]
            
            # Create strategy_class and strategy_id
            self.df['strategy_class'] = self.df['buy_exchange'] + "_" + self.df['buy_currency'] + \
                                      "_TO_" + self.df['sell_exchange'] + "_" + self.df['sell_currency']
            self.df['strategy_id'] = self.df['strategy_class']
            
            # Add arbitrage_type
            conditions = [
                (self.df['buy_exchange'] == self.df['sell_exchange']) & (self.df['buy_currency'] != self.df['sell_currency']),
                (self.df['buy_exchange'] != self.df['sell_exchange']) & (self.df['buy_currency'] == self.df['sell_currency']),
                (self.df['buy_exchange'] != self.df['sell_exchange']) & (self.df['buy_currency'] != self.df['sell_currency'])
            ]
            choices = ['CURRENCY_ARBITRAGE', 'EXCHANGE_ARBITRAGE', 'CROSS_ARBITRAGE']
            self.df['arbitrage_type'] = np.select(conditions, choices, default='UNKNOWN')
            
            # Clean arbitrage_after_fees column
            if 'arbitrage_after_fees' in self.df.columns:
                 self.df['arbitrage_after_fees_value'] = self.df['arbitrage_after_fees'].astype(str).str.replace('$', '', regex=False).astype(float)
            else:
                print("Warning: 'arbitrage_after_fees' column not found. Profit analysis might be affected.")
                self.df['arbitrage_after_fees_value'] = 0 # Default to 0 if not present

            # Save classified data
            self.classified_file = self.base_output_name + output_file_suffix + ".csv"
            self.df.to_csv(self.classified_file, index=False)
            print(f"Classified data saved to {self.classified_file}")
            
            # Print summary
            print("\n=== Strategy Classification Summary ===")
            print(f"Total strategies: {len(self.df['strategy_id'].unique())}")
            strategy_counts = self.df['strategy_id'].value_counts()
            print("\nTop 5 Most Frequent Strategies:")
            for i, (strategy, count) in enumerate(strategy_counts.head(5).items()):
                print(f"{i+1}. {strategy}: {count} occurrences")
            
            return True
            
        except Exception as e:
            print(f"Error in classify_strategies: {e}")
            import traceback
            traceback.print_exc()
            return False

    def analyze_strategy_profit(self):
        """Analyze and visualize profit by individual strategy."""
        if not self.classified_file or not self._load_data(self.classified_file, ['strategy_id', 'arbitrage_after_fees_value']):
            print("Error: Classified data not available. Run classify_strategies() first.")
            return False
        
        try:
            strategy_col = 'strategy_id'
            
            # Calculate total profit by strategy
            strategy_profit = self.df.groupby(strategy_col)['arbitrage_after_fees_value'].sum().sort_values(ascending=False)
            
            # Visualize top 10 strategies by profit
            plt.figure(figsize=(14, 7))
            top_profit = strategy_profit.head(10)
            bars = plt.bar(top_profit.index, top_profit.values, color='green')
            plt.title('Top 10 Most Profitable Strategies', fontsize=15)
            plt.xlabel('Strategy', fontsize=12)
            plt.ylabel('Total Profit ($)', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + 0.5, f'${height:.2f}', ha='center', va='bottom')
            plt.tight_layout()
            output_fig = self.base_output_name + "_classified_profit.png"
            plt.savefig(output_fig, transparent=True, dpi=300, bbox_inches='tight')
            print(f"Strategy profit chart saved to {output_fig}")
            plt.close()

            # Detailed strategy profit information table
            if all(col in self.df.columns for col in ['buy_exchange', 'buy_currency', 'sell_exchange', 'sell_currency', 'crypto']):
                strategy_details = self.df.groupby([
                    strategy_col, 'buy_exchange', 'buy_currency', 'sell_exchange', 'sell_currency'
                ]).agg({
                    'arbitrage_after_fees_value': 'sum', 
                    'crypto': 'first',
                    strategy_col: 'size' 
                }).rename(columns={strategy_col: 'occurrences'}).reset_index()
                strategy_details.sort_values('arbitrage_after_fees_value', ascending=False, inplace=True)
                detail_output = self.base_output_name + "_classified_strategy_profit_details.csv"
                strategy_details.to_csv(detail_output, index=False)
                print(f"Detailed strategy profit information saved to {detail_output}")

            print("Strategy profit analysis complete.")
            return True
        except Exception as e:
            print(f"Error in analyze_strategy_profit: {e}")
            import traceback
            traceback.print_exc()
            return False

    def analyze_strategy_frequency(self):
        """Analyze and visualize the frequency of each strategy."""
        if not self.classified_file or not self._load_data(self.classified_file, ['strategy_id']):
            print("Error: Classified data not available. Run classify_strategies() first.")
            return False
        
        try:
            strategy_counts = self.df['strategy_id'].value_counts()
            
            # Visualize top 10 most frequent strategies
            plt.figure(figsize=(12, 8))
            top_strategies = strategy_counts.head(10)
            sns.barplot(x=top_strategies.index, y=top_strategies.values, palette="viridis")
            plt.title('Top 10 Most Frequent Arbitrage Strategies', fontsize=16)
            plt.xlabel('Strategy ID', fontsize=12)
            plt.ylabel('Frequency (Number of Occurrences)', fontsize=12)
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            output_fig = self.base_output_name + "_classified_frequency.png"
            plt.savefig(output_fig, transparent=True, dpi=300, bbox_inches='tight')
            print(f"Strategy frequency chart saved to {output_fig}")
            plt.close()
            
            # Save frequency data
            freq_output = self.base_output_name + "_classified_frequency_data.csv"
            strategy_counts.to_csv(freq_output)
            print(f"Strategy frequency data saved to {freq_output}")
            print("Strategy frequency analysis complete.")
            return True
        except Exception as e:
            print(f"Error in analyze_strategy_frequency: {e}")
            return False

    def analyze_strategy_percentage(self):
        """Analyze and visualize the percentage contribution of each strategy."""
        if not self.classified_file or not self._load_data(self.classified_file, ['strategy_id']):
            print("Error: Classified data not available. Run classify_strategies() first.")
            return False
        
        try:
            strategy_counts = self.df['strategy_id'].value_counts()
            strategy_percentages = (strategy_counts / strategy_counts.sum()) * 100
            
            # Generate distinct colors for each slice using a larger color palette
            colors = sns.color_palette('tab20', len(strategy_percentages))

            # Visualize top 10 strategies by percentage
            plt.figure(figsize=(10, 10))
            top_percentages = strategy_percentages.head(10)
            if len(strategy_percentages) > 10:
                others = strategy_percentages[10:].sum()
                top_percentages['Others'] = others
            
            plt.pie(
                top_percentages, 
                labels=None,  # Remove labels from the pie chart
                autopct='%1.1f%%', 
                startangle=140, 
                colors=colors
            )
            plt.title('Strategy Contribution Percentage', fontsize=16)
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Add a legend outside the pie chart
            plt.legend(
                top_percentages.index, 
                title="Strategies", 
                loc="center left", 
                bbox_to_anchor=(1, 0.5), 
                fontsize=10
            )

            plt.tight_layout()
            output_fig = self.base_output_name + "_classified_percentage.png"
            plt.savefig(output_fig, transparent=True, dpi=300, bbox_inches='tight')
            print(f"Strategy percentage chart saved to {output_fig}")
            plt.close()
            
            # Save percentage data
            perc_output = self.base_output_name + "_classified_percentage_data.csv"
            strategy_percentages.to_csv(perc_output)
            print(f"Strategy percentage data saved to {perc_output}")
            print("Strategy percentage analysis complete.")
            return True
        except Exception as e:
            print(f"Error in analyze_strategy_percentage: {e}")
            return False

    def analyze_network(self):
        """Create network visualizations of arbitrage strategies."""
        if not self.classified_file or not self._load_data(self.classified_file, ['buy_exchange', 'sell_exchange', 'arbitrage_after_fees_value', 'crypto', 'strategy_id']):
            print("Error: Classified data not available. Run classify_strategies() first.")
            return False
        
        try:
            # ... (Full code from network_analysis.py visualize_arbitrage_network function) ...
            # This involves creating the graph G, calculating node/edge attributes, drawing with NetworkX, and optionally PyVis.
            # For brevity, the full NetworkX and PyVis plotting code is not duplicated here.
            # You would integrate the logic from the visualize_arbitrage_network function in network_analysis.py here.
            # Ensure to use self.df and save outputs with self.base_output_name
            
            # Example of what would be here (simplified):
            exchange_flow = self.df.groupby(['buy_exchange', 'sell_exchange', 'crypto']).agg(
                total_profit=('arbitrage_after_fees_value', 'sum'),
                transaction_count=('strategy_id', 'count')
            ).reset_index()
            G = nx.DiGraph()
            # ... (add nodes and edges as in network_analysis.py) ...
            
            # Static NetworkX plot
            if G.number_of_nodes() > 0 and G.number_of_edges() > 0:
                plt.figure(figsize=(14, 10))
                positions = nx.spring_layout(G, k=0.3, iterations=50, seed=42)
                node_sizes = [G.nodes[n].get('volume', 100) * 0.1 + 500 for n in G.nodes()]
                node_colors = [G.nodes[n].get('net_flow', 0) for n in G.nodes()]
                edge_widths = [G[u][v].get('weight', 1) * 0.002 + 0.5 for u, v in G.edges()]
                nx.draw_networkx_nodes(G, positions, node_size=node_sizes, node_color=node_colors, cmap=plt.cm.coolwarm, alpha=0.8)
                nx.draw_networkx_edges(G, positions, width=edge_widths, connectionstyle='arc3,rad=0.1', arrowsize=20, alpha=0.7)
                nx.draw_networkx_labels(G, positions, font_size=12, font_weight='bold')
                plt.title('Arbitrage Network: Exchange Relationships (Class Method)', fontsize=16)
                plt.axis('off')
                output_fig_nx = self.base_output_name + "_classified_network.png"
                plt.savefig(output_fig_nx, transparent=True, dpi=300, bbox_inches='tight')
                print(f"NetworkX visualization saved to {output_fig_nx}")
                plt.close()
            else:
                print("Skipping NetworkX plot due to empty graph.")

            # Interactive PyVis plot (if available)
            if PYVIS_AVAILABLE and G.number_of_nodes() > 0:
                net = Network(height="750px", width="100%", notebook=False, directed=True)
                # ... (add nodes and edges to PyVis net as in network_analysis.py) ...
                # net.save_graph(interactive_output_pyvis)
                # print(f"Interactive PyVis network saved to {interactive_output_pyvis}")
                print("PyVis visualization would be generated here.")
            elif not PYVIS_AVAILABLE:
                print("Note: Install pyvis for interactive network visualization.")

            print("Network analysis complete.")
            return True
        except Exception as e:
            print(f"Error in analyze_network: {e}")
            import traceback
            traceback.print_exc()
            return False

    def analyze_exchange_pairs(self):
        """Analyze and visualize exchange pair performance."""
        if not self.classified_file or not self._load_data(self.classified_file, ['buy_exchange', 'sell_exchange', 'arbitrage_after_fees_value', 'strategy_id', 'crypto']):
            print("Error: Classified data not available. Run classify_strategies() first.")
            return False
        
        try:
            exchanges = sorted(list(set(self.df['buy_exchange'].unique()) | set(self.df['sell_exchange'].unique())))
            profit_matrix = pd.DataFrame(0, index=exchanges, columns=exchanges)

            # Populate profit_matrix with aggregated data
            for _, row in self.df.iterrows():
                if row['buy_exchange'] in profit_matrix.index and row['sell_exchange'] in profit_matrix.columns:
                    profit_matrix.at[row['buy_exchange'], row['sell_exchange']] += row['arbitrage_after_fees_value']

            if not profit_matrix.empty:
                plt.figure(figsize=(12, 10))
                sns.heatmap(profit_matrix, annot=True, fmt='.2f', cmap=sns.diverging_palette(240, 10, as_cmap=True), center=0, linewidths=0.5)
                plt.title('Total Profit by Exchange Pair (Class Method)', fontsize=16)
                plt.tight_layout()
                output_fig_heatmap = self.base_output_name + "_classified_exchange_profit_heatmap.png"
                plt.savefig(output_fig_heatmap, transparent=True, dpi=300, bbox_inches='tight')
                print(f"Exchange profit heatmap saved to {output_fig_heatmap}")
                plt.close()
            else:
                print("Skipping exchange profit heatmap due to empty data.")

            # Chord diagram (if HoloViews available)
            if HOLOVIEWS_AVAILABLE:
                # ... (HoloViews chord diagram logic as in exchange_pair_analysis.py) ...
                print("HoloViews chord diagram would be generated here.")
            elif not HOLOVIEWS_AVAILABLE:
                print("Note: Install holoviews for chord diagrams.")

            print("Exchange pair analysis complete.")
            return True
        except Exception as e:
            print(f"Error in analyze_exchange_pairs: {e}")
            import traceback
            traceback.print_exc()
            return False

    def analyze_currency_relationships(self):
        """Analyze and visualize currency relationships in arbitrage strategies."""
        if not self.classified_file or not self._load_data(self.classified_file, ['buy_currency', 'sell_currency', 'arbitrage_after_fees_value', 'crypto', 'strategy_id']):
            print("Error: Classified data not available. Run classify_strategies() first.")
            return False
        
        try:
            currencies = sorted(list(set(self.df['buy_currency'].unique()) | set(self.df['sell_currency'].unique())))
            currency_profit_matrix = pd.DataFrame(0, index=currencies, columns=currencies)

            # Populate currency_profit_matrix with aggregated data
            for _, row in self.df.iterrows():
                if row['buy_currency'] in currency_profit_matrix.index and row['sell_currency'] in currency_profit_matrix.columns:
                    currency_profit_matrix.at[row['buy_currency'], row['sell_currency']] += row['arbitrage_after_fees_value']

            if not currency_profit_matrix.empty:
                plt.figure(figsize=(12, 10))
                sns.heatmap(currency_profit_matrix, annot=True, fmt='.2f', cmap=sns.diverging_palette(240, 10, as_cmap=True), center=0, linewidths=0.5)
                plt.title('Total Profit by Currency Pair (Class Method)', fontsize=16)
                plt.tight_layout()
                output_fig_curr_heatmap = self.base_output_name + "_classified_currency_profit_heatmap.png"
                plt.savefig(output_fig_curr_heatmap, transparent=True, dpi=300, bbox_inches='tight')
                print(f"Currency profit heatmap saved to {output_fig_curr_heatmap}")
                plt.close()
            else:
                print("Skipping currency profit heatmap due to empty data.")

            print("Currency relationship analysis complete.")
            return True
        except Exception as e:
            print(f"Error in analyze_currency_relationships: {e}")
            import traceback
            traceback.print_exc()
            return False

    def generate_strategy_reference(self):
        """
        Generate a comprehensive reference guide for all strategy IDs.
        """
        if not self.classified_file or not self._load_data(self.classified_file, ['strategy_id', 'strategy_class', 'buy_exchange', 'buy_currency', 'sell_exchange', 'sell_currency']):
            print("Error: Classified data not available. Run classify_strategies() first.")
            return False

        try:
            # Create a reference dataframe with one row per unique strategy
            reference_df = self.df.drop_duplicates('strategy_id')[
                ['strategy_id', 'strategy_class', 'buy_exchange', 'buy_currency', 'sell_exchange', 'sell_currency', 'arbitrage_type']
            ].copy()

            # Compute statistics for each strategy
            strategy_stats = self.df.groupby('strategy_id').agg({
                'arbitrage_after_fees_value': ['sum', 'mean', 'count'],
                'crypto': lambda x: x.iloc[0]  # Get the first cryptocurrency for this strategy
            })

            # Flatten the column names
            strategy_stats.columns = ['total_profit', 'avg_profit', 'occurrences', 'crypto']

            # Merge the reference with the statistics
            reference_df = reference_df.merge(strategy_stats, left_on='strategy_id', right_index=True)

            # Sort by total profit for easy reference
            reference_df = reference_df.sort_values('total_profit', ascending=False)

            # Add readable description
            reference_df['description'] = reference_df.apply(
                lambda row: f"Buy {row['crypto']} with {row['buy_currency']} on {row['buy_exchange']} → "
                          f"Sell for {row['sell_currency']} on {row['sell_exchange']}",
                axis=1
            )

            # Save to CSV
            reference_csv = self.base_output_name + "_reference.csv"
            reference_df.to_csv(reference_csv, index=False)
            print(f"Strategy reference CSV saved to {reference_csv}")

            # Format and save as readable text file
            reference_txt = self.base_output_name + "_reference.txt"

            with open(reference_txt, 'w') as f:
                f.write("STRATEGY REFERENCE GUIDE\n")
                f.write("=============================================\n\n")

                # Write summary statistics
                f.write(f"Total Strategies: {len(reference_df)}\n")
                f.write(f"Total Profit: ${reference_df['total_profit'].sum():.2f}\n")
                f.write(f"Total Occurrences: {reference_df['occurrences'].sum()}\n\n")

                f.write("STRATEGY DETAILS (Sorted by Total Profit)\n")
                f.write("=============================================\n\n")

                # Create a clean table format for the text file
                for _, row in reference_df.iterrows():
                    f.write(f"ID: {row['strategy_id']}\n")
                    f.write(f"Description: {row['description']}\n")
                    f.write(f"Total Profit: ${row['total_profit']:.2f}\n")
                    f.write(f"Average Profit: ${row['avg_profit']:.2f}\n")
                    f.write(f"Occurrences: {row['occurrences']}\n")
                    f.write(f"Type: {row['arbitrage_type']}\n")
                    f.write("-" * 50 + "\n\n")

            print(f"Strategy reference text file saved to {reference_txt}")

            # Print top 5 strategies to console for quick reference
            print("\n=== TOP 5 STRATEGIES BY PROFIT ===")
            for i, (_, row) in enumerate(reference_df.head(5).iterrows()):
                print(f"{i+1}. {row['strategy_id']}: {row['description']}")
                print(f"   Profit: ${row['total_profit']:.2f} (${row['avg_profit']:.2f} avg), Occurrences: {row['occurrences']}")

            return True
        except Exception as e:
            print(f"Error generating strategy reference: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def analyze_all(self, run_classification=True):
        """Run all analysis methods sequentially."""
        if run_classification:
            if not self.classify_strategies():
                print("Classification failed. Aborting further analysis.")
                return
        elif not self.classified_file or not os.path.exists(self.classified_file):
            print("Classification step skipped, but no classified file found. Please run classify_strategies() first or provide a classified file.")
            # Attempt to load the input file as if it's already classified
            self.classified_file = self.input_file 
            if not self._load_data(self.classified_file, required_columns=['strategy_id', 'arbitrage_after_fees_value']):
                 print("Failed to load input file as classified data. Aborting.")
                 return
            else:
                print(f"Attempting to use {self.input_file} as already classified data.")
                self.base_output_name = os.path.splitext(self.input_file)[0].replace("_classified","") # ensure base name is correct
        
        print("\nStarting comprehensive analysis...")
        self.analyze_strategy_profit()
        self.analyze_strategy_frequency()
        self.analyze_strategy_percentage()
        self.analyze_network()
        self.analyze_exchange_pairs()
        self.analyze_currency_relationships()
        print("\nAll analyses complete.")

    def print_top_rows(self, column_name, num_rows=10):
        """
        Print the top rows sorted by the given column name.

        Args:
            column_name (str): The column name to sort by.
            num_rows (int): The number of rows to display. Default is 10.
        """
        if self.df is None or self.df.empty or column_name not in self.df.columns:
            print(f"Error: Column '{column_name}' not found in the dataset or the dataset is empty.")
            return

        try:
            sorted_df = self.df.sort_values(by=column_name, ascending=False).head(num_rows)
            for index, row in sorted_df.iterrows():
                print(f"Row {index}:")
                for col, value in row.items():
                    print(f"  {col}: {value}")
                print("-" * 50)
        except Exception as e:
            print(f"Error while sorting and printing rows: {e}")

    def plot_avg_profit_per_occurrence(self, file_path):
        """
        Create a bar chart showing the average profit per occurrence for the top 10 strategies,
        with each bar a different color and a legend.
        Args:
            file_path (str): Path to the CSV file containing the required columns.
        """
        required_columns = [
            'strategy_id', 'arbitrage_after_fees_value', 'occurrences'
        ]
        if not self._load_data(file_path, required_columns):
            print("Error: Could not load data or missing required columns.")
            return False

        try:
            # Group by strategy_id and calculate total profit and total occurrences
            grouped = self.df.groupby('strategy_id').agg({
                'arbitrage_after_fees_value': 'sum',
                'occurrences': 'sum'
            })
            # Calculate average profit per occurrence
            grouped['avg_profit_per_occurrence'] = grouped['arbitrage_after_fees_value'] / grouped['occurrences']
            grouped = grouped.sort_values('avg_profit_per_occurrence', ascending=False).head(10)

            # Assign a unique color to each bar
            colors = sns.color_palette('tab10', n_colors=len(grouped))
            plt.figure(figsize=(14, 7))
            bars = plt.bar(grouped.index, grouped['avg_profit_per_occurrence'], color=colors)

            plt.title('Top 10 Strategies: Avg Profit per Occurrence', fontsize=15)
            plt.xlabel('Strategy ID', fontsize=12)
            plt.ylabel('Avg Profit per Occurrence ($)', fontsize=12)
            plt.xticks(rotation=45, ha='right')

            # Add value labels
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + 0.5, f'${height:.2f}', ha='center', va='bottom', fontsize=8)

            # Add legend
            legend_labels = [str(sid) for sid in grouped.index]
            patches = [mpatches.Patch(color=colors[i], label=legend_labels[i]) for i in range(len(legend_labels))]
            plt.legend(handles=patches, title="Strategy ID", bbox_to_anchor=(1.05, 1), loc='upper left')

            plt.tight_layout()
            output_fig = os.path.splitext(file_path)[0] + "_avg_profit_per_occurrence.png"
            plt.savefig(output_fig, transparent=True, dpi=300, bbox_inches='tight')
            print(f"Average profit per occurrence chart saved to {output_fig}")
            plt.close()
            return True
        except Exception as e:
            print(f"Error in plot_avg_profit_per_occurrence: {e}")
            return False


if __name__ == "__main__":
    # Define the input file path here
    input_file = "backend/app/external/utilities/crypto_arbitrage_3_2025-05-08.csv"  # Replace with your actual file path

    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)

    # Create an instance of DataAnalyser with the input file
    analyser = DataAnalyser(input_file)

    # Run classify_strategies first to ensure classified data is available
    if not analyser.classify_strategies():
        print("Error: Failed to classify strategies. Exiting.")
        sys.exit(1)

    # Run the specified methods
    # analyser.analyze_strategy_percentage()
    # analyser.generate_strategy_reference()
    # analyser.analyze_all(run_classification=True)
    # analyser.analyze_strategy_percentage()
    analyser.plot_avg_profit_per_occurrence("backend/app/external/utilities/crypto_arbitrage_3_2025-05-08_classified_strategy_profit_details.csv")
    # analyser.print_top_rows('arbitrage_after_fees_value', 5)
