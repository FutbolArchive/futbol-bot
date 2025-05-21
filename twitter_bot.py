import tweepy
import feedparser
import random
import os
from datetime import datetime, timedelta, timezone

# --- TUS CLAVES ---
API_KEY = "aF2K8bWZxGy5PpsTJpcxprEqQ"
API_SECRET = "teamxp0qRlrNMQYYJKawKbYM3zPvvYT1uHTm2SzUkSd3Yqd7cy"
ACCESS_TOKEN = "1924827300140355584-EomG5HfUPQrIHMqwBcu4GAvCERvjaM"
ACCESS_SECRET = "ei1FTvMCfnvil2ZiTXNOeYFG8FCFDP8YOHtjEboeYZ7TC"
BEARER_TOKEN = ""

# --- AUTENTICACIÓN API v2 ---
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# --- FUENTES RSS DE FUTBOL ---
rss_feeds = [
    "https://e00-marca.uecdn.es/rss/futbol.xml",
    "https://as.com/rss/futbol.html",
    "https://www.mundodeportivo.com/rss/futbol.xml"
]

# --- PALABRAS CLAVE PARA FILTRAR ---
keywords = ["barça", "barcelona", "madrid", "real madrid", "premier", "serie a", "bundesliga", "ligue 1"]

# --- COMENTARIOS AUTOMÁTICOS ---
def opinar(titulo):
    titulo_lower = titulo.lower()
    if "messi" in titulo_lower: return "🐐 No hay debate, Leo está por encima."
    if "cristiano" in titulo_lower: return "💪 Siempre competitivo, lo de Cristiano no es normal."
    if "madrid" in titulo_lower: return "⚪ El Madrid nunca descansa..."
    if "barça" in titulo_lower or "barcelona" in titulo_lower: return "🔵🔴 El Barça siempre da que hablar."
    if "premier" in titulo_lower: return "🏴 La Premier siempre al filo."
    if "serie a" in titulo_lower: return "🇮🇹 Vuelve la lucha en Italia."
    if "bundesliga" in titulo_lower: return "🇩🇪 Mucho más que el Bayern."
    if "ligue 1" in titulo_lower: return "🇫🇷 Todo depende de Mbappé."
    return "👀 ¿Qué opináis vosotros?"

# --- OBTENER Y PUBLICAR NOTICIA ---
def publicar_noticia():
    noticias = []
    hace_12h = datetime.now(timezone.utc) - timedelta(hours=12)
    for url in rss_feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            titulo = entry.title
            enlace = entry.link
            publicado = entry.get("published_parsed")
            if publicado:
                fecha_pub = datetime(*publicado[:6], tzinfo=timezone.utc)
                if fecha_pub < hace_12h:
                    continue
            if any(palabra in titulo.lower() for palabra in keywords):
                opinion = opinar(titulo)
                tweet = f"🗞️ {titulo}\n{opinion}\n{enlace}"
                noticias.append(tweet)

    if noticias:
        tweet = random.choice(noticias)
        try:
            client.create_tweet(text=tweet)
            print(f"Tuit publicado: {tweet}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("No hay noticias relevantes por ahora.")

# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    publicar_noticia()
