import pandas as pd
import os
import sys
import json

def _load_lookup_data(lookup_dir):
    all_lookup_df = []
    if not os.path.exists(lookup_dir):
        return pd.DataFrame(columns=['card_id', 'card_name', 'card_number', 'set_id', 'set_name', 'card_market_value'])
    for filename in os.listdir(lookup_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(lookup_dir, filename)
            with open(filepath, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode JSON from {filename}", file=sys.stderr)
                    continue

            if 'data' not in data or not data['data']:
                continue

            df = pd.json_normalize(data['data'])

            if 'tcgplayer.prices.holofoil.market' not in df.columns:
                df['tcgplayer.prices.holofoil.market'] = pd.NA
            if 'tcgplayer.prices.normal.market' not in df.columns:
                df['tcgplayer.prices.normal.market'] = pd.NA

            df['card_market_value'] = df['tcgplayer.prices.holofoil.market'].fillna(df['tcgplayer.prices.normal.market']).fillna(0.0)

            rename_dict = {
                'name': 'card_name',
                'number': 'card_number',
                'set.id': 'set_id',
                'set.name': 'set_name'
            }
            df = df.rename(columns=rename_dict)

            # Create 'card_id' from set.id and number to ensure consistency with inventory data
            if 'set_id' in df.columns and 'card_number' in df.columns:
                df['card_id'] = df['set_id'].astype(str) + '-' + df['card_number'].astype(str)
            else:
                df['card_id'] = pd.NA

            required_cols = ['card_id', 'card_name', 'card_number', 'set_id', 'set_name', 'card_market_value']
            
            for col in required_cols:
                if col not in df.columns:
                    df[col] = pd.NA
            
            all_lookup_df.append(df[required_cols].copy())

    if not all_lookup_df:
        return pd.DataFrame(columns=['card_id', 'card_name', 'card_number', 'set_id', 'set_name', 'card_market_value'])

    lookup_df = pd.concat(all_lookup_df, ignore_index=True)

    lookup_df = lookup_df.sort_values(by='card_market_value', ascending=False)
    lookup_df = lookup_df.drop_duplicates(subset=['card_id'], keep='first')
    return lookup_df

def _load_inventory_data(inventory_dir):
    inventory_data = []
    if not os.path.exists(inventory_dir):
        return pd.DataFrame()
    for filename in os.listdir(inventory_dir):
        if filename.endswith(".csv"):
            filepath = os.path.join(inventory_dir, filename)
            inventory_data.append(pd.read_csv(filepath))
    
    if not inventory_data:
        return pd.DataFrame()

    inventory_df = pd.concat(inventory_data, ignore_index=True)

    inventory_df['card_id'] = inventory_df['set_id'].astype(str) + '-' + inventory_df['card_number'].astype(str)

    return inventory_df

def update_portfolio(inventory_dir, lookup_dir, output_file):
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)

    if inventory_df.empty:
        print("Error: Inventory is empty.", file=sys.stderr)
        final_cols = ['index', 'card_name', 'set_name', 'card_market_value', 'card_id', 'set_id', 'card_number', 'binder_name', 'page_number', 'slot_number']
        pd.DataFrame(columns=final_cols).to_csv(output_file, index=False)
        return

    merged_df = pd.merge(
        inventory_df,
        lookup_df[['card_id', 'set_name', 'card_market_value']],
        on='card_id',
        how='left'
    )

    merged_df['card_market_value'] = merged_df['card_market_value'].fillna(0.0)
    merged_df['set_name'] = merged_df['set_name'].fillna('NOT_FOUND')

    merged_df['index'] = merged_df['binder_name'].astype(str) + '-' + merged_df['page_number'].astype(str) + '-' + merged_df['slot_number'].astype(str)

    final_cols = ['index', 'card_name', 'set_name', 'card_market_value', 'card_id', 'set_id', 'card_number', 'binder_name', 'page_number', 'slot_number']
    
    final_df = merged_df[final_cols]

    final_df.to_csv(output_file, index=False)

    print(f"Successfully updated portfolio to {output_file}")

def main():
    update_portfolio(
        inventory_dir='./card_inventory/',
        lookup_dir='./card_set_lookup/',
        output_file='card_portfolio.csv'
    )

def test():
    update_portfolio(
        inventory_dir='./card_inventory_test/',
        lookup_dir='./card_set_lookup_test/',
        output_file='test_card_portfolio.csv'
    )

if __name__ == "__main__":
    print("Starting portfolio update in Test Mode...", file=sys.stderr)
    test()
