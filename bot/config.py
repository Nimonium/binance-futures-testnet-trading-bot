import os
from dotenv import load_dotenv

# Load environment variables explicitly from the project root
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path=env_path, override=True)

class Config:
    """Centralized configuration for the Trading Bot."""
    
    # Binance API Configuration
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
    TESTNET_URL = 'https://testnet.binancefuture.com/fapi'
    
    # Networking & Resiliency
    API_TIMEOUT = 10  # Seconds before giving up on a request
    MAX_NETWORK_RETRIES = 3
    RETRY_DELAY = 2
    
    # Logging
    LOG_DIR = "logs"
    LOG_FILE_MAX_BYTES = 5 * 1024 * 1024  # 5 MB
    LOG_BACKUP_COUNT = 3

def validate_environment():
    """Ensures all required environment variables are set."""
    missing = []
    if not Config.BINANCE_API_KEY:
        missing.append("BINANCE_API_KEY")
    if not Config.BINANCE_API_SECRET:
        missing.append("BINANCE_API_SECRET")
        
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}\n"
                               "Please check your .env file.")
