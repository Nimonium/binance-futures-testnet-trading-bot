import re
from bot.logging_config import logger
from bot.exceptions import BotValidationError

def validate_symbol(symbol: str) -> str:
    """Validates the trading pair symbol format using Regex."""
    symbol = symbol.upper().strip()
    if not re.match(r'^[A-Z0-9]+USDT$', symbol):
        logger.error(f"Invalid symbol format: {symbol}")
        raise BotValidationError(f"Invalid symbol '{symbol}'. Must end with 'USDT' (e.g., BTCUSDT).")
    return symbol

def validate_side(side: str) -> str:
    side = side.upper().strip()
    if side not in ["BUY", "SELL"]:
        logger.error(f"Invalid order side: {side}")
        raise BotValidationError("Side must be strictly 'BUY' or 'SELL'.")
    return side

def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper().strip()
    valid_types = ["MARKET", "LIMIT", "STOP_MARKET", "STOP"]
    if order_type not in valid_types:
        logger.error(f"Invalid order type: {order_type}")
        raise BotValidationError(f"Order type must be one of {valid_types}.")
    return order_type

def validate_quantity(quantity: float) -> float:
    """Enforces strict positive precision constraints."""
    if quantity <= 0:
        logger.error(f"Invalid quantity: {quantity}")
        raise BotValidationError("Quantity must be a positive number greater than 0.")
    return quantity

def validate_price(order_type: str, price: float) -> float:
    if order_type in ["LIMIT", "STOP"] and price is None:
        logger.error("Price missing for LIMIT/STOP order")
        raise BotValidationError("Price parameter is required for LIMIT and STOP orders.")
    if price is not None and price <= 0:
        logger.error(f"Invalid price: {price}")
        raise BotValidationError("Price must be a positive number greater than 0.")
    return price

def validate_stop_price(order_type: str, stop_price: float) -> float:
    if order_type in ["STOP_MARKET", "STOP"] and stop_price is None:
        logger.error("Stop price missing for STOP/STOP_MARKET order")
        raise BotValidationError("Stop price parameter is required for STOP and STOP_MARKET orders.")
    if stop_price is not None and stop_price <= 0:
        logger.error(f"Invalid stop price: {stop_price}")
        raise BotValidationError("Stop price must be a positive number greater than 0.")
    return stop_price
