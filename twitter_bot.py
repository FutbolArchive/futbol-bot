import tweepy
import random
import os

# --- TUS CLAVES ---
API_KEY = "aF2K8bWZxGy5PpsTJpcxprEqQ"
API_SECRET = "teamxp0qRlrNMQYYJKawKbYM3zPvvYT1uHTm2SzUkSd3Yqd7cy"
ACCESS_TOKEN = "1924827300140355584-wofRnD2m7JEmFEP9P7E1FBZ5PxWkyT"
ACCESS_SECRET = "pWUPPo9Ww96HcfkM2zMABC5mzltrh1Q48h6GxRlx2uf8f"

# --- AUTENTICACIÓN ---
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# --- CARGAR TUITS ---
with open("tweets.txt", "r", encoding="utf-8") as f:
    tweets = [line.strip() for line in f if line.strip()]

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
            f.truncate(0)  # borrar el contenido anterior

    tweet = random.choice(disponibles)
    used.add(tweet)

    with open("used.txt", "a", encoding="utf-8") as f:
        f.write(tweet + "\n")

    try:
        api.update_status(tweet)
        print(f"Tuit publicado: {tweet}")
    except Exception as e:
        print(f"Error: {e}")

# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    publicar_tuit()
