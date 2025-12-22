import requests
import hashlib
import os

URL = "https://empleopublico.carm.es/web/pagina?IDCONTENIDO=2340&IDTIPO=200&CODIGO_CUERPO=AIA00&CODIGO_CONVOCATORIA=AIA00L22&TIPO_ACCESO=L&RASTRO=c$m61986,62006"

HASH_FILE = "last_hash.txt"

def get_page_hash():
    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    return hashlib.sha256(r.text.encode()).hexdigest()

def send_telegram(msg):
    token = os.environ["TG_TOKEN"]
    chat_id = os.environ["TG_CHAT_ID"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": msg})

def main():
    new_hash = get_page_hash()

    # Primera ejecución
    if not os.path.exists(HASH_FILE):
        with open(HASH_FILE, "w") as f:
            f.write(new_hash)
        send_telegram("🆕 Estado inicial guardado. Aún no hay comparación.")
        return

    with open(HASH_FILE) as f:
        old_hash = f.read()

    if new_hash != old_hash:
        send_telegram(f"⚠️ CAMBIO DETECTADO\n{URL}")
        with open(HASH_FILE, "w") as f:
            f.write(new_hash)
    else:
        send_telegram(f"✅ Sin cambios\n{URL}")


if __name__ == "__main__":
    main()
