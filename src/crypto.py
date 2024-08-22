import sys
import time
import serial
import requests

def get_crypto_prices():
    """Fetch the current market prices for Bitcoin and Ethereum using CoinCap API."""
    url = 'https://api.coincap.io/v2/assets'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        bitcoin_data = next(item for item in data['data'] if item['id'] == 'bitcoin')
        ethereum_data = next(item for item in data['data'] if item['id'] == 'ethereum')

        bitcoin_price = float(bitcoin_data['priceUsd'])
        ethereum_price = float(ethereum_data['priceUsd'])

        return bitcoin_price, ethereum_price
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching crypto prices: {e}")
        return None, None

def update_lcd(lcd_serial, bitcoin_price, ethereum_price):
    """Update the LCD screen with the Bitcoin and Ethereum prices."""
    # Clear the screen
    lcd_serial.write('\x1b'.encode('ascii'))

    # Format the display string
    display_str = (f'BTC: ${bitcoin_price:.2f}\n\r'
                   f'ETH: ${ethereum_price:.2f}')

    # Display the information on the LCD
    lcd_serial.write(display_str.encode('ascii'))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 crypto.py PORT")
        print("  e.g: python3 crypto.py /dev/tty.usbmodemXXXX")
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

            if bitcoin_price is not None and ethereum_price is not None:
                # Update the LCD screen
                update_lcd(lcd_serial, bitcoin_price, ethereum_price)

                # Print prices to console (optional)
                print(f'BTC: ${bitcoin_price:.2f}\nETH: ${ethereum_price:.2f}')
            else:
                print("Failed to fetch prices. Retrying...")

            # Wait for 3 seconds before updating
            time.sleep(3)

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        # Close the serial connection
        lcd_serial.close()
