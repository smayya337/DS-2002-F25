import pandas as pd
import os
import sys

def generate_summary(portfolio_file):
    if not os.path.exists(portfolio_file):
        print(f"Error: Portfolio file not found at {portfolio_file}", file=sys.stderr)
        sys.exit(1)

    try:
        df = pd.read_csv(portfolio_file)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame()

    if df.empty:
        print("Portfolio is empty. No summary to generate.")
        return

    total_portfolio_value = df['card_market_value'].sum()

    most_valuable_card = df.loc[df['card_market_value'].idxmax()]

    print("--- Portfolio Summary ---")
    print(f"Total Portfolio Value: ${total_portfolio_value:,.2f}")
    print("--- Most Valuable Card ---")
    print(f"Name: {most_valuable_card['card_name']}")
    print(f"ID: {most_valuable_card['card_id']}")
    print(f"Value: ${most_valuable_card['card_market_value']:,.2f}")

def main():
    generate_summary('card_portfolio.csv')

def test():
    generate_summary('test_card_portfolio.csv')

if __name__ == "__main__":
    test()
