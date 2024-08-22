import sys
import time
import serial
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
import os.path
import pickle

# Path to your OAuth 2.0 client secrets file
CLIENT_SECRETS_FILE = './client_secret.json'

# Scopes required for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service

def get_message_count(service, query=''):
    """Get the count of messages based on the query and pagination."""
    try:
        messages = []
        response = service.users().messages().list(userId='me', q=query).execute()
        messages.extend(response.get('messages', []))

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
            messages.extend(response.get('messages', []))

        return len(messages)
    except HttpError as error:
        print(f'An error occurred: {error}')
        return 0

def update_lcd(lcd_serial, unread_count, total_count):
    """Update the LCD screen with the email counts."""
    # Clear the screen (verify the correct command for your LCD)
    lcd_serial.write('\x1b'.encode('ascii'))  # Common clear screen command

    # Format the display string
    display_str = (f'Unread \n\r'
                   f'Emails: {unread_count}\n\r'
                   f'Total\n\r'
                   f'Emails: {total_count}')

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

    # Initialize Gmail API service
    service = get_service()

    try:
        while True:
            # Get unread email count and total email count
            unread_count = get_message_count(service, query='in:inbox is:unread')
            total_count = get_message_count(service)

            # Print counts to console for debugging
            print(f'Unread Emails: {unread_count}')
            print(f'Total Emails: {total_count}')

            # Update the LCD screen
            update_lcd(lcd_serial, unread_count, total_count)

            # Wait for 30 seconds before updating
            time.sleep(1)

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        # Close the serial connection
        lcd_serial.close()
