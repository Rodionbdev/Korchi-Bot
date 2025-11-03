# 🛡️ Korchi – Discord Moderation Bot

**Korchi** is a powerful and flexible Discord moderation bot developed in Python using [discord.py](https://github.com/Rapptz/discord.py).  
It helps server admins and moderators manage communities with essential tools like warnings, mutes, bans, timeouts, and user information commands. Perfect for small to medium-sized Discord servers.

## ✨ Features

- `!warn @user [reason]` — Issue a warning to a user  
- `!unwarn @user` — Remove one warning  
- `!checkwarns @user` — View all warnings for a user  
- `!clearwarns @user` — Clear all warnings  
- `!mutechat` / `!unmutechat` — Mute/unmute users in **text** channels  
- `!mutevoice` / `!unmutevoice` — Mute/unmute users in **voice** channels  
- `!timeout @user 10m` / `!untimeout @user` — Temporarily mute or remove timeout  
- `!ban`, `!unban`, `!kick` — Full moderation control  
- `!purge 20` — Delete recent messages  
- `!rules` — Display server rules  
- `!info` — Developer and bot info  
- `!whois` — View user account info  
- Auto punishments:
  - 3 warnings → chat mute  
  - 5 warnings → automatic ban

## ⚙️ Requirements

- Python 3.10 or higher  
- Discord bot token  
- Libraries:
  - `discord.py`
  - `sqlite3` (built-in)
  - `json`, `datetime` (built-in)

> Bot automatically creates `MutedFromChat` and `MutedFromVoice` roles if they don't exist.

## 🚀 Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Rodionbdev/Korchi-Bot.git
    cd Korchi-Bot
    ```

2. Install required libraries:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `config.json` file in the root folder:
    ```json
    {
      "prefix": "!",
      "token": "YOUR_BOT_TOKEN"
    }
    ```

4. Run the bot:
    ```bash
    python main.py
    ```

## 🧠 How It Works

Korchi uses a local SQLite database (`warns.db`) to store warnings for each server.  
It tracks how many times a user has been warned and applies punishments based on thresholds (mute at 3, ban at 5). The database is created automatically on launch.

## 📄 License

This project is open-source under the MIT License.  
See [LICENSE](LICENSE) for details.

---

👤 **Developer**: Rodion  
📨 Telegram: [@Rodionbdev](https://t.me/Rodionbdev)  
🆔 Discord: `1255968122754699305`
