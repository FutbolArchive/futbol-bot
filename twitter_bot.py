import tweepy
import random
import os

# --- TUS CLAVES ---
API_KEY = "aF2K8bWZxGy5PpsTJpcxprEqQ"
API_SECRET = "teamxp0qRlrNMQYYJKawKbYM3zPvvYT1uHTm2SzUkSd3Yqd7cy"
ACCESS_TOKEN = "1924827300140355584-EomG5HfUPQrIHMqwBcu4GAvCERvjaM"
ACCESS_SECRET = "ei1FTvMCfnvil2ZiTXNOeYFG8FCFDP8YOHtjEboeYZ7TC"

# --- AUTENTICACIÓN API v2 ---
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# --- CARGAR TUITS COMO BLOQUES SEPARADOS POR ---TUIT--- ---
with open("tweets.txt", "r", encoding="utf-8") as f:
    content = f.read()
    tweets = [block.strip() for block in content.split("---TUIT---") if block.strip()]

# --- CARGAR TUITS USADOS ---
try:
    with open("used.txt", "r", encoding="utf-8") as f:
        used = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    used = set()

# --- PUBLICAR UN TUIT ÚNICO ---
def publicar_tuit():
    global used
    disponibles = [t for t in tweets if t not in used]
    if not disponibles:
        used = set()
        disponibles = tweets[:]
        with open("used.txt", "w", encoding="utf-8") as f:
            f.truncate(0)

    tweet = random.choice(disponibles)
    used.add(tweet)

    with open("used.txt", "a", encoding="utf-8") as f:
        f.write(tweet + "\n")

    try:
        lineas = tweet.split("\n")
        filtrado = [l for l in lineas if not (l.startswith("⬜") or l.startswith("🟥"))]
        tweet_final = "\n".join(filtrado).strip()

        client.create_tweet(text=tweet_final)
        print(f"Tuit publicado con API v2: {tweet_final}")
    except Exception as e:
        print(f"Error: {e}")

# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    publicar_tuit()
