# This is no-nude chat-roulette bot.

A telegram-based chat-roulette bot, that filters content via neural-nework.

# Installing

> [!WARNING]
> **You must have python >= 3.10**

## Linux

```shell
sudo apt install redis
git clone --branch main https://github.com/severnayaluna/nude_chat.git
cd nude_chat
touch .env
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Windows

```shell
git clone --branch main https://github.com/severnayaluna/nude_chat.git
cd nude_chat
copy NUL .env
python3 -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
```

# Running

> [!IMPORTANT]
> **.env file requiered!**
>
> **~/.../nude_chat/.env**:
> ```
> export BOT_TOKEN=1234567890
> ```

## Linux

```shell
source env/bin/activate
python src/main.py
```

## Windows

```shell
.\env\Scripts\activate
python src/main.py
```