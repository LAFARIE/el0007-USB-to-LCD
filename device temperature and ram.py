import sys
import time
import serial
import os
import psutil

def get_cpu_temperature():
    # Use osx-cpu-temp to get the CPU temperature
    temp = os.popen('osx-cpu-temp').readline().strip()
    return temp

def get_ram_usage():
    ram = psutil.virtual_memory()
    used_ram = ram.used / (1024 ** 3)  # Convert to GB
    free_ram = ram.available / (1024 ** 3)  # Convert to GB
    return used_ram, free_ram

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 test.py PORT")
        print("  e.g: python3 test.py /dev/tty.usbmodemXXXX")
        exit(1)

    # Create serial connection on specified port with baud rate of 57600 and 8N1 configuration.
    lcd_serial = serial.Serial()
    lcd_serial.baudrate = 57600
    lcd_serial.port = sys.argv[1]

    # Open serial connection.
    try:
        lcd_serial.open()
    except Exception as e:
        if not lcd_serial.is_open:
            print("Unable to open specified serial port: " + sys.argv[1])
        else:
            print(e)
        exit(1)

    try:
        while True:
            # Get CPU temperature and RAM usage
            cpu_temp = get_cpu_temperature()
            used_ram, free_ram = get_ram_usage()

            # Format the string to display on LCD
            display_str = (f'\x1bCPU Temp: {cpu_temp}\n\r'
                           f'Used RAM: {used_ram:.2f}GB\n\r'
                           f'Free RAM: {free_ram:.2f}GB')

            # Clear the screen
            lcd_serial.write('\x1b'.encode('ascii'))

            # Display the temperature and RAM usage
            lcd_serial.write(display_str.encode('latin-1'))

            # Wait for 3 seconds before updating
            time.sleep(1)

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        # Close the serial connection
        lcd_serial.close()
