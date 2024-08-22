import sys
import time
import serial
import requests

def get_crypto_prices():
    """Fetch the current market prices for Bitcoin and Ethereum."""
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': 'bitcoin,ethereum',
        'vs_currencies': 'usd'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        prices = response.json()
        bitcoin_price = prices['bitcoin']['usd']
        ethereum_price = prices['ethereum']['usd']
        return bitcoin_price, ethereum_price
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None

def update_lcd(lcd_serial, bitcoin_price, ethereum_price):
    """Update the LCD screen with the Bitcoin and Ethereum prices."""
    # Clear the screen
    lcd_serial.write('\x1b'.encode('ascii'))

    # Format the display string
    display_str = (f'BTC: ${bitcoin_price:.2f}\n'
                   f'ETH: ${ethereum_price:.2f}')

    # Display the information on the LCD
    lcd_serial.write(display_str.encode('ascii'))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 notification.py PORT")
        print("  e.g: python3 notification.py /dev/tty.usbmodemXXXX")
        exit(1)

    # Create serial connection on specified port with baud rate of 57600
    lcd_serial = serial.Serial()
    lcd_serial.baudrate = 57600
    lcd_serial.port = sys.argv[1]

    # Open serial connection
    try:
        lcd_serial.open()
    except Exception as e:
        print(f"Unable to open specified serial port: {sys.argv[1]}")
        print(e)
        exit(1)

    try:
        while True:
            # Get Bitcoin and Ethereum prices
            bitcoin_price, ethereum_price = get_crypto_prices()

            # Update the LCD screen
            if bitcoin_price is not None and ethereum_price is not None:
                update_lcd(lcd_serial, bitcoin_price, ethereum_price)

            # Print prices to console (optional)
            print(f'BTC: ${bitcoin_price:.2f}\nETH: ${ethereum_price:.2f}')

            # Wait for 3 seconds before updating
            time.sleep(3)

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        # Close the serial connection
        lcd_serial.close()
