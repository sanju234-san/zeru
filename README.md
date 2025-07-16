# DeFi Wallet Credit Scoring 🔗

This project assigns a **credit score to DeFi wallets** based on their on-chain transaction history using the Aave V2 protocol.

Each wallet's behavior — such as deposits, borrowings, repayments, and liquidations — is analyzed to determine its financial reliability. The system uses a custom heuristic scoring model and outputs a score between 0 and 1000 for each wallet.

## 🛠 Features

- Parses JSON transaction data from Aave V2 users
- Groups data by wallet and engineers key behavioral features
- Assigns credit scores using a rule-based model
- Saves scores to a CSV file for reporting or integration
- Designed for on-chain credit risk modeling and DeFi analytics

## 📁 Output

- `wallet_scores.csv`: Contains each wallet address and its final credit score

## 🧪 Example Use Case

> "Given a dataset of wallet transactions, identify which users are most trustworthy in terms of borrowing and repayment."

This kind of scoring can be used for:
- DeFi lending platforms
- Sybil resistance
- On-chain identity profiling
- DAO voter trust analysis

## 📦 Requirements

- Python 3.8+
- pandas

## 🚀 Usage

```bash
python code.py
