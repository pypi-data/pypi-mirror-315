from .bot import SaintBot
from .config_loader import load_config
from .decos import saintess, guild, user, only, cool
import inspect

BOT_INSTANCE = None

def init(path=None, token=None, prefix="!", owners=None):
    global BOT_INSTANCE
    if path:
        config = load_config(path)
        token = config.get("token", None)
        prefix = config.get("prefix", "!")
        owners = config.get("owners", [])
    
    if not token:
        print("❌ Error: Bot token is required. Use 'init()' with a token or a valid config path.")
        exit(1)

    BOT_INSTANCE = SaintBot(command_prefix=prefix, owners=owners, token=token)
    return BOT_INSTANCE

def start(bot=None):
    global BOT_INSTANCE
    bot = bot or BOT_INSTANCE
    
    if not bot:
        print("❌ Error: No bot instance found. Did you forget to call `init()`?")
        exit(1)

    if not bot.token:
        print("❌ Error: Missing bot token.")
        exit(1)

    print("✅ Starting the bot...")
    bot.run(bot.token)
