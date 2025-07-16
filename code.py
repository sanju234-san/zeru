import json
import pandas as pd
import os

def load_json_to_dataframe(file_path):
    """Load JSON file into a pandas DataFrame."""
    with open(file_path, 'r') as f:
        data = json.load(f)
        return pd.DataFrame(data)

def preprocess_data(df):
    """Preprocess and create features for each wallet."""
    print("📋 Columns in the data:", df.columns.tolist())

    # Use the actual wallet column
    if 'userWallet' in df.columns:
        wallet_col = 'userWallet'
    else:
        raise ValueError("❌ Wallet column not found. Expected 'userWallet'.")

    grouped = df.groupby(wallet_col)

    # Use only 'count' if no amount column
    if 'amount' in df.columns:
        wallet_features = grouped.agg({
            'amount': ['count', 'sum', 'mean'],
            'action': lambda x: x.value_counts().to_dict()
        }).reset_index()
        wallet_features.columns = [wallet_col, 'txn_count', 'total_amount', 'avg_amount', 'action_counts']
    else:
        wallet_features = grouped.agg({
            'action': lambda x: x.value_counts().to_dict()
        }).reset_index()
        wallet_features['txn_count'] = df.groupby(wallet_col)['action'].count().values
        wallet_features['avg_amount'] = 0  # fallback if no amount
        wallet_features['total_amount'] = 0
        wallet_features.columns = [wallet_col, 'action_counts', 'txn_count', 'avg_amount', 'total_amount']

    # Expand action dictionary into individual columns
    action_df = wallet_features['action_counts'].apply(pd.Series).fillna(0)
    wallet_features = pd.concat([wallet_features.drop('action_counts', axis=1), action_df], axis=1)

    # Add any missing expected actions
    for action in ['deposit', 'withdraw', 'transfer', 'borrow', 'repay', 'redeemunderlying', 'liquidationcall']:
        if action not in wallet_features.columns:
            wallet_features[action] = 0

    return wallet_features

def score_wallet(row):
    """Assign a credit score to a wallet based on its transaction behavior."""
    score = 500  # Base score

    # Apply heuristics based on DeFi behavior
    score += row.get('deposit', 0) * 2
    score += row.get('repay', 0) * 3
    score -= row.get('borrow', 0) * 1.5
    score -= row.get('liquidationcall', 0) * 5
    score += row.get('transfer', 0) * 0.5

    # Activity and amount-based bonuses
    if row['txn_count'] > 10:
        score += 50
    if row.get('avg_amount', 0) > 1000:
        score += 100

    return max(0, min(int(score), 1000))  # Clamp score to [0, 1000]

def main():
    file_path = r'C:\Users\sanjeevni\Desktop\zeru\user-wallet-transactions.json'

    if not os.path.exists(file_path):
        print(f"❌ File {file_path} does not exist.")
        return

    print("📥 Loading data...")
    df = load_json_to_dataframe(file_path)

    print("⚙️ Preprocessing...")
    wallet_features = preprocess_data(df)

    print("🔢 Scoring wallets...")
    wallet_features['score'] = wallet_features.apply(score_wallet, axis=1)

    output_file = 'wallet_scores.csv'
    wallet_features.to_csv(output_file, index=False)

    print(f"✅ Wallet scores saved to '{output_file}'")

if __name__ == "__main__":
    main()
