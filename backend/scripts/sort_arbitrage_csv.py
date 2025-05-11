#!/usr/bin/env python3
"""
Sort a CSV file based on the arbitrage_after_fees column and print the first 5 rows.

Usage:
    python sort_arbitrage_csv.py <input_csv_file> [output_csv_file]

If output_csv_file is not provided, the sorted data will be written to a file 
with "_sorted" appended to the original filename.

You can also import and use this as a module:
    from sort_arbitrage_csv import print_top_arbitrage_opportunities
    print_top_arbitrage_opportunities('path/to/csv', n=5)
"""

import sys
import csv
import os
from datetime import datetime


def sort_csv_by_arbitrage(input_file, output_file=None):
    """
    Sort a CSV file based on the arbitrage_after_fees column in descending order.
    
    Args:
        input_file (str): Path to the input CSV file
        output_file (str, optional): Path to the output CSV file. If not provided,
                                     a default name will be generated.
    
    Returns:
        list: Sorted rows from the CSV
        str: Path to the output file
    """
    # Generate default output filename if not provided
    if not output_file:
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}_sorted{ext}"
    
    try:
        # Read the CSV file
        with open(input_file, 'r') as f:
            reader = csv.DictReader(f)
            # Store all rows
            rows = list(reader)
            
            # Check if 'arbitrage_after_fees' column exists
            if 'arbitrage_after_fees' not in reader.fieldnames:
                print(f"Error: Column 'arbitrage_after_fees' not found in {input_file}")
                return None, None
            
            # Clean and convert arbitrage_after_fees values for sorting
            for row in rows:
                value = row['arbitrage_after_fees']
                # Remove $ and any other non-numeric characters, but keep the negative sign
                if value.startswith('$'):
                    value = value[1:]
                try:
                    row['_sort_value'] = float(value)
                except ValueError:
                    # If conversion fails, use a very negative number to sort to the bottom
                    row['_sort_value'] = float('-inf')
            
            # Sort rows by arbitrage_after_fees in descending order
            sorted_rows = sorted(rows, key=lambda x: x['_sort_value'], reverse=True)
            
            # Remove temporary sort value
            for row in sorted_rows:
                del row['_sort_value']
            
        # Write the sorted data to the output file
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(sorted_rows)
        
        print(f"Sorted data written to {output_file}")
        return sorted_rows, output_file
        
    except Exception as e:
        print(f"Error sorting CSV file: {str(e)}")
        return None, None


def print_top_arbitrage_opportunities(csv_file, n=5):
    """
    Print the top N arbitrage opportunities from a CSV file.
    
    Args:
        csv_file (str): Path to the CSV file
        n (int): Number of top opportunities to print
    """
    sorted_rows, _ = sort_csv_by_arbitrage(csv_file)
    
    if not sorted_rows:
        return
    
    print(f"\n===== TOP {n} ARBITRAGE OPPORTUNITIES =====")
    print(f"From file: {csv_file}")
    print("=" * 50)
    
    # Get important columns for display
    display_cols = ['crypto', 'strategy', 'arbitrage', 'arbitrage_after_fees']
    
    # Print header
    header = {}
    for col in display_cols:
        if col in sorted_rows[0]:
            header[col] = col
    
    # Print column headers
    header_str = " | ".join(f"{col.upper()}" for col in header.keys())
    print(header_str)
    print("-" * len(header_str))
    
    # Print top N rows
    for i, row in enumerate(sorted_rows[:n]):
        row_str = " | ".join(f"{row.get(col, 'N/A')}" for col in header.keys())
        print(f"{i+1}. {row_str}")


def main():
    """Main function to handle command-line arguments and run the script."""
    if len(sys.argv) < 2:
        print(f"Usage: python {os.path.basename(__file__)} <input_csv_file> [output_csv_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)
    
    # Sort the CSV and print top 5 opportunities
    print_top_arbitrage_opportunities(input_file, 5)
    
    # If output file was provided, we already wrote the sorted data there
    if not output_file:
        # Let the user know where the full sorted data was written
        base, ext = os.path.splitext(input_file)
        print(f"\nFull sorted data available in: {base}_sorted{ext}")


if __name__ == "__main__":
    main()