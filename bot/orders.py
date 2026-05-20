import time
import requests
from typing import Dict, Any, Optional
from binance.exceptions import BinanceAPIException, BinanceRequestException

from bot.client import BinanceTestnetClient
from bot.logging_config import logger, time_execution
from bot.exceptions import BotAPIError, BotNetworkError
from bot.config import Config

class OrderManager:
    """
    Manages order placement on the Binance Futures Testnet API.
    Includes built-in retry handling for network errors to ensure reliability.
    """
    def __init__(self):
        self.testnet_client = BinanceTestnetClient()
        self.client = self.testnet_client.get_client()

    @time_execution
    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, 
                   price: Optional[float] = None, stop_price: Optional[float] = None,
                   dry_run: bool = False) -> Dict[str, Any]:
        """Places an order with the provided parameters, with resiliency and tracking."""
        logger.info(f"Preparing to place {order_type} {side} order for {quantity} {symbol}.")
        
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity
        }

        if order_type == 'LIMIT':
            params['timeInForce'] = 'GTC'
            params['price'] = price
        elif order_type == 'STOP':
            params['timeInForce'] = 'GTC'
            params['price'] = price
            params['stopPrice'] = stop_price
        elif order_type == 'STOP_MARKET':
            params['stopPrice'] = stop_price
            
        if dry_run:
            logger.info("DRY RUN MODE: Validating params without executing order.")
            return {"status": "DRY_RUN_SUCCESS", "params": params}
            
        return self._execute_with_retries(params)
        
    def _execute_with_retries(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Internal method handling the robust retry mechanism."""
        max_retries = Config.MAX_NETWORK_RETRIES
        
        for attempt in range(1, max_retries + 1):
            try:
                logger.debug(f"Attempt {attempt}/{max_retries}: Sending order request to Binance API...")
                response = self.client.futures_create_order(**params)
                
                logger.info(f"Order successfully placed. Order ID: {response.get('orderId')}")
                return response
                
            except BinanceAPIException as e:
                # 400/401 type errors - No retry
                logger.error(f"Binance API Exception (Code: {e.status_code}): {e.message}")
                raise BotAPIError(e.message, e.status_code)
            except (BinanceRequestException, requests.exceptions.RequestException) as e:
                # Network/Timeout Errors - Retry
                logger.warning(f"Network error on attempt {attempt}: {str(e)}")
                if attempt == max_retries:
                    logger.error("Max network retries exceeded. Aborting.")
                    raise BotNetworkError(f"Failed to place order due to persistent network issues: {str(e)}")
                
                logger.info(f"Retrying in {Config.RETRY_DELAY} seconds...")
                time.sleep(Config.RETRY_DELAY)
            except Exception as e:
                logger.error(f"Unexpected system error: {str(e)}")
                raise
