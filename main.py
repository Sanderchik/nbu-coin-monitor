import requests
import time
import random
from bs4 import BeautifulSoup
from config import TOKEN, CHAT_ID

CHECK_URL = "https://coins.bank.gov.ua/shop/moneti/"
CHECK_INTERVAL = (8, 12)  # секунд


def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Error sending message:", e)


def check_coins():
    try:
        r = requests.get(CHECK_URL, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        coins = soup.find_all("div", class_="product-item")
        found = []
        for c in coins:
            title = c.find("div", class_="product-title").text.strip()
            status = c.find("div", class_="product-status").text.strip()
            link = c.find("a")["href"]
            full_link = "https://coins.bank.gov.ua" + link
            found.append((title, status, full_link))
        return found
    except Exception as e:
        print("Error parsing page:", e)
        return []


if __name__ == "__main__":
    print("Bot started, monitoring NBU coins...")
    prev_data = set()
    while True:
        coins = check_coins()
        current_data = set(coins)
        new_items = current_data - prev_data
        if new_items:
            for item in new_items:
                title, status, link = item
                send_message(f"🪙 <b>{title}</b>\nStatus: {status}\n{link}")
        prev_data = current_data
        time.sleep(random.randint(*CHECK_INTERVAL))
