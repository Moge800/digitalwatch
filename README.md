# Digital Watch with Raspberry Pi + Inky PHAT

**Languages:** [English](README.md) | [日本語](README_ja.md)

Digital clock project - A stylish digital clock using Raspberry Pi and Inky PHAT e-paper display

![Raspberry Pi + Inky PHAT Digital Watch](./image/pict.png)

## Overview

This project creates a power-efficient and stylish digital clock using Raspberry Pi and Pimoroni Inky PHAT e-paper display. Thanks to the e-paper display characteristics, it enables low power consumption with always-on display, functioning as an easy-to-read clock.

### Key Features

- **Date and Time Display**: Shows year/month/day, day of the week, and hour/minute
- **Auto Update**: Automatically updates time every minute
- **Low Power Consumption**: Energy-efficient design with e-paper display
- **Auto Start**: Automatic startup on system boot (systemd service)
- **Rotation Support**: Supports 180-degree rotation display

## Hardware Requirements

### Required Components
- **Raspberry Pi Zero 2 W** (recommended) or other Raspberry Pi models
- **Pimoroni Inky PHAT** e-paper display
- microSD card (8GB or larger recommended)
- Power adapter (5V 2.5A recommended)

### Connection Method
Connect the Inky PHAT directly to the Raspberry Pi GPIO header. No additional wiring required.

## Software Requirements

### OS
- Raspberry Pi OS (Bullseye or later recommended)
- Python 3.7 or later

### Required Python Packages
- `inky` - Inky PHAT control library
- `Pillow` - Image processing library

## Installation Instructions

### 1. Prerequisites Check
```bash
# Check Python version
python3 --version

# Check and update pip
sudo apt update
sudo apt install python3-pip
```

### 2. Clone the Project
```bash
git clone https://github.com/Moge800/digitalwatch.git
cd digitalwatch
```

### 3. Install Dependencies
```bash
# Install required system packages
sudo apt install python3-venv

# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install Python packages
pip install inky pillow
```

### 4. Manual Test Execution
```bash
# Execute Hello World test
python3 hello_world.py

# Execute main program test
python3 main.py
```

### 5. Register as System Service
```bash
# Register and start service
sudo bash register_service.sh

# Reboot system
sudo reboot
```

## Usage

### Manual Execution
```bash
cd digitalwatch
source .venv/bin/activate
python3 main.py
```

### Service Control
```bash
# Check service status
sudo systemctl status digitalwatch.service

# Start service
sudo systemctl start digitalwatch.service

# Stop service
sudo systemctl stop digitalwatch.service

# Restart service
sudo systemctl restart digitalwatch.service

# Check logs
sudo journalctl -u digitalwatch.service -f
```

### Stopping the Program
When running manually, you can stop with `Ctrl+C`.

## Configuration Customization

You can customize the display by changing constants in the `main.py` file:

```python
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Font path
FONT_SIZE = 35                # Font size
UPDATE_INTERVAL = 1           # Update check interval (seconds)
ROTATION_DEGREE = 180         # Screen rotation angle (0, 90, 180, 270)
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Display Not Showing
- **Cause**: Inky PHAT is not properly connected
- **Solution**: Check GPIO connection and restart Raspberry Pi

#### 2. Import Error
```bash
# Error example: ModuleNotFoundError: No module named 'inky'
pip install inky pillow
```

#### 3. Permission Error
```bash
# Check GPIO access permissions
sudo usermod -a -G gpio $USER
# Logout and login required
```

#### 4. Font Not Displaying
- **Cause**: Specified font file does not exist
- **Solution**: Default font will be used automatically

#### 5. Service Won't Start
```bash
# Check service status and logs
sudo systemctl status digitalwatch.service
sudo journalctl -u digitalwatch.service --since "10 minutes ago"
```

### Log Checking Methods
```bash
# Real-time log monitoring
sudo journalctl -u digitalwatch.service -f

# Last 5 minutes of logs
sudo journalctl -u digitalwatch.service --since "5 minutes ago"
```

## File Structure

```
digitalwatch/
├── main.py                 # Main program
├── hello_world.py          # Test program
├── launch.sh              # Launch script
├── register_service.sh    # Service registration script
├── README.md              # This file (English)
├── README_ja.md           # Japanese README
├── license.txt            # License information
└── image/
    └── pict.png           # Project image
```

## Development Information

### Development Environment Setup
```bash
# Create development virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install inky pillow

# Code editing
# VS Code workspace file: digitalwatch.code-workspace
```

### Code Structure
- `get_formatted_time()`: Time formatting processing
- `load_font()`: Font loading
- `update_display()`: Display update
- `calculate_sleep_time()`: Calculate wait time until next minute boundary
- `main()`: Main loop

## License

This project is licensed under Apache License 2.0. See [license.txt](license.txt) for details.

## Contributing

Bug reports and feature requests are welcome via GitHub Issues or Pull Requests.

## Author

- **Moge800** - Project creator

---

**Note**: This project is designed specifically for Raspberry Pi. Operation on other platforms is not guaranteed.