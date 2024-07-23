# Telegram Chat Cleaner and Group Leaver

This script uses the [Telethon](https://github.com/LonamiWebs/Telethon) library to delete all chats, leave all groups, and unsubscribe from all channels in a Telegram account.

## Features

- Deletes all messages in individual chats.
- Leaves all groups.
- Unsubscribes from all channels.
- Handles archived chats as well.

## Prerequisites

- Python 3.6+
- A Telegram API ID and Hash. You can obtain these by creating a new application on [my.telegram.org](https://my.telegram.org).

## Installation

1. Clone this repository:
    ```sh
    git clone https://github.com/yourusername/telegram-chat-cleaner.git
    cd telegram-chat-cleaner
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Update the `api_id`, `api_hash`, and `phone_number` variables in `cleaner.py` with your Telegram API credentials and phone number.

2. Run the script:
    ```sh
    python cleaner.py
    ```

## Code Explanation

The script performs the following steps:
1. Initializes the Telegram client with the provided API ID, API hash, and session name.
2. Starts the client and logs in using the provided phone number.
3. Retrieves all dialogs (including archived ones).
4. Iterates through each dialog:
    - Deletes all messages in individual chats.
    - Leaves groups and channels.
5. Disconnects the client.

## Important Notes

- Ensure that you have the necessary permissions to delete messages and leave groups/channels.
- Be aware of Telegram's rate limits to avoid getting temporarily banned for too many requests in a short period.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Acknowledgements

- [Telethon](https://github.com/LonamiWebs/Telethon) for the Telegram client library.

