import os 
from dotenv import load_dotenv
from classes.btc_monitor import BTCMonitor

load_dotenv()

def main():
    bot = BTCMonitor()
    bot.run(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    main()