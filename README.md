# 🚀 Binance Futures Testnet Trading Bot
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Binance API](https://img.shields.io/badge/Binance-API-yellow.svg)](https://binance-docs.github.io/apidocs/testnet/en/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Elite](https://img.shields.io/badge/Code%20Style-Elite-purple.svg)]()

A professional, elite-tier CLI Python application for automated trading on the Binance USDT-M Futures Testnet. Built with clean architecture, fault tolerance, and comprehensive observability in mind.

## 🌟 Technical Overview
This system is engineered for resilience and scalability. It features:
- **Centralized Configuration** (`bot/config.py`)
- **Domain-Specific Exception Hierarchy** (`bot/exceptions.py`)
- **Fault-Tolerant Networking** with automatic retry mechanisms for dropped connections.
- **Strict Validation** utilizing Regex and boundary checks.
- **Rich Terminal UI** separating rendering logic from API concerns.
- **Asynchronous Rotating Logs** with execution tracking.

## 🚀 Features
- **Trading Operations:** Execute MARKET, LIMIT, STOP, and STOP_MARKET orders safely.
- **Dry-Run Mode:** Validate inputs and API parameters *without* sending a real order to the exchange.
- **Health Checks & Diagnostics:** `--health-check` and `--account-info` commands to verify connectivity and margin instantly.
- **Execution Tracking:** Built-in decorators to measure API call latency.
- **Graceful Shutdowns:** Traps `SIGINT` (Ctrl+C) to prevent dirty exits.

---

## 📸 Screenshots

### Health Check
<img width="1186" height="360" alt="Screenshot 2026-05-21 011842" src="https://github.com/user-attachments/assets/773490fa-5622-4751-9e93-44102b5f278e" />


### Market Order
<img width="1021" height="411" alt="Screenshot 2026-05-21 015234" src="https://github.com/user-attachments/assets/63a310f4-9a4e-4c7b-8711-77c15a9dd3a1" />


### Limit Order
<img width="1091" height="392" alt="Screenshot 2026-05-21 015344" src="https://github.com/user-attachments/assets/68baeeec-b7ae-4912-a996-a5d6c650870a" />


---

## 📂 Architecture Structure
```text
trading_bot/
│
├── bot/
│   ├── __init__.py
│   ├── config.py         # Central configuration and environment validation
│   ├── exceptions.py     # Domain-specific exception hierarchy
│   ├── client.py         # Secure Binance API client 
│   ├── orders.py         # Order placement logic and retry-handlers
│   ├── validators.py     # Regex and boundary argument validation
│   ├── logging_config.py # Rotating file logs and execution trackers
│   └── cli.py            # Argparse CLI interface and Rich UI panels
│
├── logs/                 # Auto-generated audit logs
│
├── .env                  # Environment variables (API keys)
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
├── .gitignore            # Git ignore file
└── main.py               # Main entry point script
```

---

## ⚙️ Setup Instructions

### 1. Binance Testnet Setup
1. Go to [Binance Futures Testnet](https://testnet.binancefuture.com).
2. Create an account, scroll to the bottom, and generate your Testnet API Key and Secret.

### 2. Local Installation
```bash
git clone https://github.com/yourusername/binance-trading-bot.git
cd binance-trading-bot

python -m venv venv
# Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

---

## 💻 Elite CLI Commands

**1. System Diagnostics**
```bash
python main.py --health-check
python main.py --account-info
```

**2. Dry-Run (No execution)**
```bash
python main.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01 --dry-run
```

**3. Real Market Order**
```bash
python main.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

**4. Limit Order**
```bash
python main.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.5 --price 3500
```

---

## 🔮 Future Improvements
1. **Websockets Integration:** Transition from REST to Websockets for sub-millisecond price streams.
2. **Asynchronous I/O:** Migrate `requests` to `aiohttp` for non-blocking concurrent order placement.
3. **Strategy Engine Plugin System:** Add abstract base classes for users to implement algorithms (e.g., VWAP, MACD crosses).
4. **Local SQLite Persistence:** Persist trades in a local database for analytics rather than just parsing `.log` files.
5. **Dockerization & CI/CD:** Add a `Dockerfile` and GitHub Actions for automated unit testing before deployment.
