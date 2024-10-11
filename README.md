# ManageTelegramMembership

This project is a Telegram bot that allows users to manage their membership in Telegram channels and groups. It uses the `telethon` library for interacting with the Telegram API, and other libraries for user interaction and visual enhancements.

## Features

- Login using QR code or phone number
- Leave Telegram channels or groups
- Displays a stylized header using `pyfiglet` and `termcolor`
- Generates QR codes
- Interactive prompts using `inquirer`

## Requirements

- Python 3.10
- The following Python packages:
  - `telethon`
  - `termcolor`
  - `inputimeout`
  - `pyfiglet`
  - `qrcode`
  - `inquirer`

## Setup Instructions

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/mesamirh/ManageTelegramMembership.git
   cd ManageTelegramMembership
   ```
2. **Make the Setup Script Executable:**
   ```sh
   chmod +x setup_env.sh
   ```
3. **Activate the Virtual Environment**(if not activated):
   ```sh
   source venv/bin/activate
   ```
4. **Run the Setup Script:**
   ```sh
   ./setup_env.sh
   ```
5. **Run the Bot:**
   ```sh
   python bot.py
   ```

## Configuration

Replace the placeholders in bot.py with your actual Telegram API credentials:
   ```sh
   api_id = YOUR_API_ID
   api_hash = 'YOUR_API_HASH'
   ```

## Usage

When you run the bot, it will display a stylized header and prompt you to select a login method. Follow the on-screen instructions to log in to your Telegram account. You can then manage your membership in Telegram channels and groups.