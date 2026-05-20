from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from bot.config import Config, validate_environment
from bot.logging_config import logger
from bot.exceptions import BotAPIError
import time

class BinanceTestnetClient:
    """Manages secure connections to the Binance Futures Testnet."""
    
    def __init__(self):
        # Validate environment variables safely upon initialization
        validate_environment()
        
        try:
            self.client = Client(
                Config.BINANCE_API_KEY, 
                Config.BINANCE_API_SECRET, 
                testnet=True,
                requests_params={'timeout': Config.API_TIMEOUT}
            )
            self.client.FUTURES_URL = Config.TESTNET_URL
            
            # Automatically synchronize clock offset to prevent "Timestamp ahead" errors
            server_time = self.client.futures_time()['serverTime']
            local_time = int(time.time() * 1000)
            self.client.timestamp_offset = server_time - local_time
            
            logger.info(f"Successfully initialized Binance Futures Testnet API Client (Time Offset: {self.client.timestamp_offset}ms).")
        except BinanceAPIException as e:
            logger.error(f"API initialization failed: {e.message}")
            raise BotAPIError(e.message, e.status_code)
        except Exception as e:
            logger.error(f"Unexpected error during client setup: {e}")
            raise
            
    def get_client(self) -> Client:
        return self.client
        
    def test_connectivity(self) -> bool:
        """Pings the Binance API to ensure server is reachable."""
        try:
            self.client.futures_ping()
            return True
        except Exception as e:
            logger.error(f"Connectivity test failed: {e}")
            return False
            
    def get_account_information(self):
        """Fetches account futures balance and limits."""
        try:
            return self.client.futures_account()
        except BinanceAPIException as e:
            raise BotAPIError(e.message, e.status_code)
