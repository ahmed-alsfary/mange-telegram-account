import asyncio
import re
from telethon.sync import TelegramClient
from telethon.tl import functions, types

api_id = 'api_id'
api_hash = 'api_hash'
phone_number = 'phone_number'

# Session name and client initialization
session_name = 'alish'

client = TelegramClient(session_name, api_id, api_hash)

async def delete_chats():
    dialogs = await client.get_dialogs()
    archived_dialogs = await client.get_dialogs(folder=1)
    all_dialogs = dialogs + archived_dialogs

    print(f"Found {len(all_dialogs)} dialogs (including archived).")

    for dialog in all_dialogs:
        entity = dialog.entity
        try:
            if isinstance(entity, types.User):
                name = entity.username if entity.username else f"{entity.first_name} {entity.last_name}"
                print(f'Deleting chat with {name}')
                input_peer = await client.get_input_entity(entity)
                await client(functions.messages.DeleteHistoryRequest(
                    peer=input_peer,
                    max_id=0,  # max_id set to 0 to delete all messages
                    just_clear=False,  # False to delete the chat, not just clear messages
                    revoke=True  # True to delete messages for everyone
                ))
            elif isinstance(entity, types.Chat):
                name = entity.title
                print(f'Deleting chat with {name} and leaving group')
                input_peer = await client.get_input_entity(entity)
                await client(functions.messages.DeleteHistoryRequest(
                    peer=input_peer,
                    max_id=0,
                    just_clear=False,
                    revoke=True
                ))
                await client(functions.messages.DeleteChatUserRequest(
                    chat_id=entity.id,
                    user_id='me'
                ))
            elif isinstance(entity, types.Channel):
                name = entity.username if entity.username else entity.title
                if entity.megagroup:
                    print(f'Deleting chat with {name} and leaving group')
                else:
                    print(f'Deleting chat with {name} and unsubscribing from channel')
                input_peer = await client.get_input_entity(entity)
                await client(functions.messages.DeleteHistoryRequest(
                    peer=input_peer,
                    max_id=0,
                    just_clear=False,
                    revoke=True
                ))
                await client(functions.channels.LeaveChannelRequest(channel=input_peer))
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

async def unblock_users():
    blocked_users = await client(functions.contacts.GetBlockedRequest(offset=0, limit=100))
    for user in blocked_users.blocked:
        try:
            print(f'Unblocking user {user.peer_id}')
            await client(functions.contacts.UnblockRequest(id=user.peer_id))
        except Exception as e:
            error_message = str(e).lower()
            if 'a wait of' in error_message:
                wait_time = int(re.search(r'a wait of (\d+) seconds is required', error_message).group(1))
                print(f'Waiting for {wait_time} seconds due to rate limit.')
                await asyncio.sleep(wait_time)
                print(f'Retrying to unblock user {user.peer_id}')
                await client(functions.contacts.UnblockRequest(id=user.peer_id))
            else:
                print(f'Error unblocking user {user.peer_id}: {str(e)}')

    print("All blocked users have been unblocked.")

async def delete_contacts():
    contacts = await client(functions.contacts.GetContactsRequest(hash=0))
    for contact in contacts.users:
        try:
            print(f'Deleting contact {contact.id}')
            await client(functions.contacts.DeleteContactsRequest(id=[contact.id]))
        except Exception as e:
            print(f'Error deleting contact {contact.id}: {str(e)}')

    print("All contacts have been deleted.")

def display_menu():
    print("\nPlease choose the operations you want to perform:")
    print("1. Delete all chats")
    print("2. Leave all groups")
    print("3. Unsubscribe from all channels")
    print("4. Unblock all users")
    print("5. Delete all contacts")
    print("6. Execute selected operations and exit")

def get_user_choices():
    choices = set()
    while True:
        display_menu()
        choice = input("Enter the number of your choice: ")
        if choice == '6':
            break
        if choice in ['1', '2', '3', '4', '5']:
            choices.add(choice)
    return choices

if __name__ == '__main__':
    user_choices = get_user_choices()

    with client:
        if '1' in user_choices or '2' in user_choices or '3' in user_choices:
            client.loop.run_until_complete(delete_chats())
        if '4' in user_choices:
            client.loop.run_until_complete(unblock_users())
        if '5' in user_choices:
            client.loop.run_until_complete(delete_contacts())
