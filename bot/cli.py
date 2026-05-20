import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.traceback import install

from bot.validators import (
    validate_symbol, validate_side, validate_order_type,
    validate_quantity, validate_price, validate_stop_price
)
from bot.orders import OrderManager
from bot.client import BinanceTestnetClient
from bot.logging_config import logger
from bot.exceptions import BotAPIError, BotValidationError, BotNetworkError

# Format unhandled exceptions beautifully
install(show_locals=False)

console = Console()

def print_banner():
    banner_text = (
        "[bold cyan]:: Binance Futures Testnet Trading Bot ::[/bold cyan]\n"
        "[dim]Elite Internship-Quality Automated Trading System[/dim]"
    )
    console.print(Panel.fit(banner_text, box=box.HEAVY, border_style="cyan"))

def display_order_summary(response: dict, is_dry_run: bool = False):
    title = "[bold green][SUCCESS] Dry Run Execution Summary[/bold green]" if is_dry_run else "[bold green][SUCCESS] Order Execution Summary[/bold green]"
    table = Table(title=title, box=box.ROUNDED, header_style="bold yellow")
    
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="magenta", justify="right")
    
    if is_dry_run:
        params = response.get('params', {})
        for k, v in params.items():
            if v is not None:
                table.add_row(k.capitalize(), str(v))
        table.add_row("Status", "[bold]DRY_RUN_SUCCESS[/bold]")
    else:
        table.add_row("Order ID", str(response.get('orderId', 'N/A')))
        table.add_row("Symbol", response.get('symbol', 'N/A'))
        table.add_row("Status", f"[bold]{response.get('status', 'N/A')}[/bold]")
        table.add_row("Side", response.get('side', 'N/A'))
        table.add_row("Type", response.get('type', 'N/A'))
        table.add_row("Executed Qty", str(response.get('executedQty', '0')))
        
        avg_price = response.get('avgPrice', '0')
        if avg_price and avg_price != '0':
            table.add_row("Avg Fill Price", str(avg_price))
        
    console.print(table)
    console.print("[bold green]Process complete.[/bold green]\n")

def execute_health_check():
    with console.status("[bold blue]Pinging Binance Servers...[/bold blue]", spinner="dots"):
        client = BinanceTestnetClient()
        is_reachable = client.test_connectivity()
    
    if is_reachable:
        console.print(Panel("[bold green][SUCCESS] Health Check Passed[/bold green]\n"
                            "Successfully connected to Binance Futures Testnet.\n"
                            "API Keys are loaded and valid.", border_style="green"))
    else:
        console.print(Panel("[bold red][ERROR] Health Check Failed[/bold red]\n"
                            "Could not reach Binance servers. Check your network or API keys.", border_style="red"))

def execute_account_info():
    with console.status("[bold blue]Fetching account data...[/bold blue]", spinner="bouncingBar"):
        client = BinanceTestnetClient()
        account_data = client.get_account_information()
        
    table = Table(title="[bold cyan][INFO] Futures Account Information[/bold cyan]", box=box.ROUNDED)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="yellow", justify="right")
    
    table.add_row("Total Wallet Balance", f"${account_data.get('totalWalletBalance', '0.00')}")
    table.add_row("Available Margin", f"${account_data.get('availableBalance', '0.00')}")
    table.add_row("Total Unrealized PNL", f"${account_data.get('totalUnrealizedProfit', '0.00')}")
    
    can_trade = "Yes" if account_data.get('canTrade') else "No"
    table.add_row("Trading Enabled", can_trade)
    
    console.print(table)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Elite CLI application for Binance Futures Testnet trading.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python main.py --health-check\n"
               "  python main.py --account-info\n"
               "  python main.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001\n"
               "  python main.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --dry-run"
    )
    
    sys_group = parser.add_argument_group("System Commands")
    sys_group.add_argument('--health-check', action='store_true', help="Verify Binance connectivity and API keys")
    sys_group.add_argument('--account-info', action='store_true', help="Fetch futures wallet balance and margin")
    
    trade_group = parser.add_argument_group("Trading Commands")
    trade_group.add_argument('--symbol', type=str, help="Trading pair symbol (e.g., BTCUSDT)")
    trade_group.add_argument('--side', type=str, choices=['BUY', 'SELL', 'buy', 'sell'], help="Order side (BUY or SELL)")
    trade_group.add_argument('--type', type=str, dest='order_type', 
                        choices=['MARKET', 'LIMIT', 'STOP', 'STOP_MARKET', 'market', 'limit', 'stop', 'stop_market'], 
                        help="Order type")
    trade_group.add_argument('--quantity', type=float, help="Base asset quantity")
    trade_group.add_argument('--price', type=float, help="Order price (Required for LIMIT/STOP)")
    trade_group.add_argument('--stop-price', type=float, dest='stop_price', help="Trigger stop price (Required for STOP/STOP_MARKET)")
    trade_group.add_argument('--dry-run', action='store_true', help="Validate inputs and logic without sending order to Binance")
    
    return parser.parse_args()

def main():
    try:
        print_banner()
        args = parse_args()
        
        # Route to System Commands
        if args.health_check:
            execute_health_check()
            sys.exit(0)
            
        if args.account_info:
            execute_account_info()
            sys.exit(0)
            
        # Ensure trading arguments exist if not a system command
        if not all([args.symbol, args.side, args.order_type, args.quantity]):
            console.print("[bold red][ERROR] Missing Arguments:[/bold red] --symbol, --side, --type, and --quantity are required for trading.")
            sys.exit(1)
        
        # Execute Trading Command
        with console.status("[bold yellow]Validating user inputs...[/bold yellow]", spinner="dots"):
            symbol = validate_symbol(args.symbol)
            side = validate_side(args.side)
            order_type = validate_order_type(args.order_type)
            quantity = validate_quantity(args.quantity)
            price = validate_price(order_type, args.price)
            stop_price = validate_stop_price(order_type, args.stop_price)
            
        with console.status("[bold blue]Processing order...[/bold blue]", spinner="bouncingBar"):
            manager = OrderManager()
            response = manager.place_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price,
                stop_price=stop_price,
                dry_run=args.dry_run
            )
            
        display_order_summary(response, is_dry_run=args.dry_run)
        
    except BotValidationError as e:
        console.print(f"\n[bold red][ERROR] Validation Error:[/bold red] {str(e)}")
        sys.exit(1)
    except BotAPIError as e:
        console.print(f"\n[bold red][ERROR] Binance API Error ({e.status_code}):[/bold red] {str(e)}")
        console.print("[dim]Hint: Check your API keys, balance, and symbol format.[/dim]")
        sys.exit(1)
    except BotNetworkError as e:
        console.print(f"\n[bold red][ERROR] Network Failure:[/bold red] {str(e)}")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[bold yellow][WARN] Process interrupted by user. Shutting down gracefully...[/bold yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red][ERROR] Unexpected System Error:[/bold red] {str(e)}")
        logger.exception("Unexpected error in main flow")
        sys.exit(1)

if __name__ == "__main__":
    main()
