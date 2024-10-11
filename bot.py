from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.contacts import BlockRequest
from telethon.tl.functions.messages import DeleteHistoryRequest
from inputimeout import inputimeout, TimeoutOccurred
from termcolor import colored
import pyfiglet
import time
import qrcode
import inquirer
import asyncio

api_id = YOUR_API_ID  # Get your API ID from my.telegram.org
api_hash = 'YOUR_API_HASH'  # Get your API Hash from my.telegram.org
string_session = StringSession('')

DELAY_BETWEEN_ACTIONS = 10

header = pyfiglet.figlet_format("mesamirh")
for line in header.split("\n"):
    print(colored(line, 'blue', attrs=['bold']))
    time.sleep(0.1)

async def main():
    client = TelegramClient(string_session, api_id, api_hash)

    questions = [
        inquirer.List(
            'login_method',
            message="Please select a login method",
            choices=['QR Code Login', 'Phone Number Login'],
        ),
    ]
    answers = inquirer.prompt(questions)
    login_method = answers['login_method']

    if login_method == 'QR Code Login':
        await client.connect()
        if not await client.is_user_authorized():
            qr_login = await client.qr_login()
            qr = qrcode.QRCode()
            qr.add_data(qr_login.url)
            qr.make(fit=True)
            qr.print_ascii(invert=True)
            print(colored('Please scan the QR code with your Telegram app to log in.', 'blue'))
            await qr_login.wait()
            print(colored('Logged in successfully.', 'blue'))

    elif login_method == 'Phone Number Login':
        await client.start(
            phone=lambda: input(colored('Please enter your phone (or bot token): ', 'blue')),
            password=lambda: input(colored('Please enter your password: ', 'blue')),
            code_callback=lambda: input(colored('Please enter the code you received: ', 'blue')),
        )
        print(colored('Logged in successfully.', 'blue'))

    print(colored('Session:', 'blue'), client.session.save())

    print(colored('Fetching joined channels/groups/private chats...', 'blue'))
    dialogs = await client.get_dialogs()
    print(colored('Fetched joined channels/groups/private chats.', 'blue'))

    channels = [dialog for dialog in dialogs if dialog.is_channel]
    private_chats = [dialog for dialog in dialogs if dialog.is_user and not dialog.entity.bot]
    bot_chats = [dialog for dialog in dialogs if dialog.is_user and dialog.entity.bot]

    try:
        choice = inputimeout(prompt=colored("Choose an action for channels/groups:\n"
                                            "1. Leave from all\n"
                                            "2. Leave only from group and channels\n"
                                            "Your choice (1/2): ", 'blue'), timeout=30)
    except TimeoutOccurred:
        choice = '2'

    if choice == '1':
        for dialog in channels:
            print(colored(f'Leaving channel/group: {dialog.title}', 'blue'))
            await client(LeaveChannelRequest(dialog.entity))
            await asyncio.sleep(DELAY_BETWEEN_ACTIONS)
        print(colored('Left all channels/groups.', 'blue'))
    elif choice == '2':
        groups = [dialog for dialog in channels if dialog.is_group]
        for dialog in groups:
            print(colored(f'Leaving group: {dialog.title}', 'blue'))
            await client(LeaveChannelRequest(dialog.entity))
            await asyncio.sleep(DELAY_BETWEEN_ACTIONS)
        print(colored('Left all group channels.', 'blue'))

    async def handle_chats(chats, chat_type):
        print(colored(f'{chat_type} Chats:', 'blue'))
        for index, dialog in enumerate(chats):
            print(colored(f'{index + 1}. {dialog.title}', 'blue'))

        action_choice = input(colored(f"Do you want to delete, block, or skip all {chat_type} chats? (delete/block/skip): ", 'blue'))
        hold_list = input(colored(f"Enter chat numbers to skip (like 1,2) or press Enter to continue: ", 'blue')).split(',')

        for index, dialog in enumerate(chats):
            if str(index + 1) in hold_list:
                print(colored(f'Skipping chat: {dialog.title}', 'blue'))
                continue

            try:
                if action_choice == 'delete':
                    await client(DeleteHistoryRequest(peer=dialog.entity, max_id=0))
                    print(colored(f'Deleted chat: {dialog.title}', 'blue'))
                elif action_choice == 'block':
                    await client(BlockRequest(dialog.entity))
                    print(colored(f'Blocked user: {dialog.title}', 'blue'))
                else:
                    print(colored(f'Skipped chat: {dialog.title}', 'blue'))

                await asyncio.sleep(DELAY_BETWEEN_ACTIONS)

            except Exception as e:
                print(colored(f"Error on {action_choice} for {dialog.title}: {e}", 'red'))

    await handle_chats(private_chats, "Private")
    await handle_chats(bot_chats, "Bot")

    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
