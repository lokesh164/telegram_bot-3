import telebot
import requests
from bs4 import BeautifulSoup
import time
import threading

API_TOKEN = '7862033921:AAG6P0Kd0ugxzjvb6iek7A7IFysfQDd1Vy8'  # अपने बॉट का API टोकन यहां डालें
bot = telebot.TeleBot(API_TOKEN)

CHANNEL_ID = '-1002417993469'  # आपके टेलीग्राम चैनल का आईडी

SITEMAP_URL = 'https://techyfile.com/post-sitemap1.xml'  # आपकी वेबसाइट का साइटमैप URL

# स्टॉप फ्लैग
stop_bot = False
sent_links = set()  # पहले से भेजे गए लिंक को ट्रैक करने के लिए सेट

# सभी पोस्ट के लिंक प्राप्त करने के लिए फ़ंक्शन
def fetch_post_links():
    response = requests.get(SITEMAP_URL)
    soup = BeautifulSoup(response.content, 'xml')
    links = [loc.text for loc in soup.find_all('loc')]
    return links

# लिंक से पोस्ट का शीर्षक प्राप्त करने के लिए फ़ंक्शन
def get_post_title(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('title').text  # <title> टैग से शीर्षक प्राप्त करें
    return title

# पोस्ट भेजने के लिए फ़ंक्शन
def send_post(link):
    title = get_post_title(link)  # लिंक से शीर्षक प्राप्त करें
    message = f"""
🌟 {title} 🌟

Quality Options:

480p: {link}  

720p: {link}  

1080p: {link}  

🔍 How to Download [कैसे डाउनलोड करें]:
https://t.me/c/2359773096/203

📢 Join Our Backup Account for Updates:
https://t.me/techyBackup
"""
    bot.send_message(CHANNEL_ID, message, parse_mode='Markdown')

# सभी पोस्ट को समय के साथ भेजने के लिए फ़ंक्शन
def share_posts():
    global stop_bot
    post_links = fetch_post_links()  # सभी पोस्ट लिंक प्राप्त करें
    for link in post_links:
        if stop_bot:  # यदि बॉट को रोकने का संकेत है
            break
        if link not in sent_links:  # यदि लिंक पहले से नहीं भेजा गया है
            send_post(link)  # प्रत्येक लिंक के लिए पोस्ट भेजें
            sent_links.add(link)  # लिंक को पहले से भेजे गए लिंक में जोड़ें
        time.sleep(5)  # 60 सेकंड का इंतज़ार करें

# स्टॉप कमांड के लिए हैंडलर
@bot.message_handler(commands=['stop'])
def stop_bot_command(message):
    global stop_bot
    stop_bot = True  # बॉट को रोकने के लिए फ्लैग सेट करें
    bot.reply_to(message, "बॉट को सफलतापूर्वक रोका गया है।")

# स्टार्ट कमांड के लिए हैंडलर
@bot.message_handler(commands=['start'])
def start_bot_command(message):
    global stop_bot
    stop_bot = False  # बॉट को स्टार्ट करने के लिए फ्लैग रीसेट करें
    bot.reply_to(message, "बॉट को पुनः प्रारंभ किया गया है।")
    
    # नए थ्रेड में पोस्ट शेयर करना शुरू करें
    share_thread = threading.Thread(target=share_posts)
    share_thread.start()

# बॉट शुरू करें
if __name__ == '__main__':
    bot.polling()  # बॉट को चलाते रहें
