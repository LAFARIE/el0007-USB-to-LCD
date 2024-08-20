```markdown
# el0007-USB-to-LCD

This repository contains various projects utilizing the EL0007 USB-to-LCD board. The scripts provided demonstrate how to use the EL0007 board to display real-time system information, such as CPU temperature and RAM usage, as well as other custom data.

## Features

- Real-time display of system performance metrics on the EL0007 LCD board
- Examples include CPU temperature and RAM usage monitoring
- Easy integration with serial communication for various applications

## Requirements

- Python 3.x
- `psutil` library (for RAM usage)
- `osx-cpu-temp` command (for CPU temperature on macOS)
- `pyserial` library (for serial communication)

## Installation

### Python Dependencies

You need to install the required Python packages. Run the following command to install them:

```bash
pip install psutil pyserial
```

### macOS Specific

To get the CPU temperature on macOS, you need to install the `osx-cpu-temp` command. You can install it using Homebrew:

```bash
brew install osx-cpu-temp
```

### Windows Specific

For Windows, ensure you have a compatible command or method to get the CPU temperature if necessary. The provided script may require adjustments for Windows environments.

## Usage

1. **Connect your EL0007 LCD screen** to the appropriate serial port on your computer.
2. **Run the script** by providing the serial port as an argument.

### Example Command

For macOS:

```bash
python3 test.py /dev/tty.usbmodemXXXX
```

For Windows (replace `COMX` with your actual COM port):

```bash
python test.py COMX
```

### Arguments

- `PORT`: The serial port to which your EL0007 LCD screen is connected. For macOS, this might look like `/dev/tty.usbmodemXXXX`. For Windows, it might look like `COM3`.

## Code Overview

The script performs the following tasks:

1. **Establishes a Serial Connection:** Opens a connection to the EL0007 LCD screen using the provided serial port.
2. **Fetches System Information:** Retrieves CPU temperature and RAM usage.
3. **Displays Information:** Sends the information to the LCD screen, updating every 3 seconds.
4. **Handles Graceful Exit:** Closes the serial connection properly when interrupted.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code, provided that the original license and copyright notice are included.

## Contributions

Contributions are welcome! If you have any improvements or suggestions, please fork the repository and submit a pull request.

## Contact

For any questions or issues, feel free to reach out to me on [LinkedIn](https://www.linkedin.com/in/farhadlafarie/) or email me at [farhadlafarie@gmail.com](mailto:farhadlafarie@gmail.com).

## Acknowledgments

Special thanks to Simtelic for providing the tools and support necessary for this project.

---

**Happy Coding!** 🚀
```
