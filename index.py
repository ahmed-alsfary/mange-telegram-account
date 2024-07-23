from telethon.sync import TelegramClient
from telethon.tl import functions, types

api_id = 'api_id'
api_hash = 'api_hash'
phone_number = 'phone_number'

# Session name and client initialization
session_name = 'session_name'

client = TelegramClient(session_name, api_id, api_hash)

async def delete_all_chats_and_leave_groups():
    await client.start(phone_number)
    try:
        # Get a list of all the chats (groups and channels) that the user is a member of
        dialogs = await client.get_dialogs()

        print(f"Found {len(dialogs)} dialogs.")

        for dialog in dialogs:
            entity = dialog.entity
            try:
                if isinstance(entity, types.User):
                    name = entity.username if entity.username else f"{entity.first_name} {entity.last_name}"
                    print(f'Deleting chat with {name}')
                    await client(functions.messages.DeleteHistoryRequest(
                        peer=entity,
                        max_id=0,  # max_id set to 0 to delete all messages
                        just_clear=False,  # False to delete the chat, not just clear messages
                        revoke=True  # True to delete messages for everyone
                    ))
                elif isinstance(entity, types.Chat):
                    name = entity.title
                    print(f'Deleting chat with {name} and leaving group')
                    await client(functions.messages.DeleteHistoryRequest(
                        peer=entity,
                        max_id=0,  # max_id set to 0 to delete all messages
                        just_clear=False,  # False to delete the chat, not just clear messages
                        revoke=True  # True to delete messages for everyone
                    ))
                    await client(functions.channels.LeaveChannelRequest(channel=entity))
                elif isinstance(entity, types.Channel):
                    name = entity.username if entity.username else entity.title
                    if entity.megagroup:
                        print(f'Deleting chat with {name} and leaving group')
                    else:
                        print(f'Deleting chat with {name} and unsubscribing from channel')
                    await client(functions.messages.DeleteHistoryRequest(
                        peer=entity,
                        max_id=0,  # max_id set to 0 to delete all messages
                        just_clear=False,  # False to delete the chat, not just clear messages
                        revoke=True  # True to delete messages for everyone
                    ))
                    await client(functions.channels.LeaveChannelRequest(channel=entity))
                else:
                    print(f'Skipping unknown entity type: {entity}')
                    continue

            except Exception as e:
                error_message = str(e).lower()
                if 'admin privileges' in error_message:
                    print(f'Skipping {name}: Requires admin privileges.')
                elif 'invalid peer' in error_message:
                    print(f'Skipping {name}: Invalid peer type or permissions.')
                elif 'flood' in error_message:
                    print(f'Skipping {name}: Too many requests in a short period, try again later.')
                else:
                    print(f'Error deleting chat with {name}: {str(e)}')

        # Get a list of archived chats (groups and channels) that the user is a member of
        archived_dialogs = await client.get_dialogs(folder=1)

        print(f"Found {len(archived_dialogs)} archived dialogs.")

        for dialog in archived_dialogs:
            entity = dialog.entity
            try:
                if isinstance(entity, types.User):
                    name = entity.username if entity.username else f"{entity.first_name} {entity.last_name}"
                    print(f'Deleting archived chat with {name}')
                    await client(functions.messages.DeleteHistoryRequest(
                        peer=entity,
                        max_id=0,  # max_id set to 0 to delete all messages
                        just_clear=False,  # False to delete the chat, not just clear messages
                        revoke=True  # True to delete messages for everyone
                    ))
                elif isinstance(entity, types.Chat):
                    name = entity.title
                    print(f'Deleting archived chat with {name} and leaving group')
                    await client(functions.messages.DeleteHistoryRequest(
                        peer=entity,
                        max_id=0,  # max_id set to 0 to delete all messages
                        just_clear=False,  # False to delete the chat, not just clear messages
                        revoke=True  # True to delete messages for everyone
                    ))
                    await client(functions.channels.LeaveChannelRequest(channel=entity))
                elif isinstance(entity, types.Channel):
                    name = entity.username if entity.username else entity.title
                    if entity.megagroup:
                        print(f'Deleting archived chat with {name} and leaving group')
                    else:
                        print(f'Deleting archived chat with {name} and unsubscribing from channel')
                    await client(functions.messages.DeleteHistoryRequest(
                        peer=entity,
                        max_id=0,  # max_id set to 0 to delete all messages
                        just_clear=False,  # False to delete the chat, not just clear messages
                        revoke=True  # True to delete messages for everyone
                    ))
                    await client(functions.channels.LeaveChannelRequest(channel=entity))
                else:
                    print(f'Skipping unknown entity type: {entity}')
                    continue

            except Exception as e:
                error_message = str(e).lower()
                if 'admin privileges' in error_message:
                    print(f'Skipping {name}: Requires admin privileges.')
                elif 'invalid peer' in error_message:
                    print(f'Skipping {name}: Invalid peer type or permissions.')
                elif 'flood' in error_message:
                    print(f'Skipping {name}: Too many requests in a short period, try again later.')
                else:
                    print(f'Error deleting chat with {name}: {str(e)}')
        
        print("Attempted to delete all chats, leave all groups, and unsubscribe from all channels.")

    except Exception as e:
        print(f'Error deleting chats: {str(e)}')

    await client.disconnect()

if __name__ == '__main__':
    client.loop.run_until_complete(delete_all_chats_and_leave_groups())
