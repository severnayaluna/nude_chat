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

cp .env.example .env.local
cp .env.example .env.prod

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Windows

```shell
git clone --branch main https://github.com/severnayaluna/nude_chat.git

cd nude_chat

copy .env.example .env.local
copy .env.example .env.prod

python3 -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
```

# Running
> [!IMPORTANT]
> FIll thet .env.local or .env.prod files!

## Linux

```shell
source env/bin/activate
python main.py <.env file name> <logging level>
```

## Windows

> [!IMPORTANT]
> You must have redis installed on your system!

```shell
.\env\Scripts\activate
python main.py <.env file name> <logging level>
```
