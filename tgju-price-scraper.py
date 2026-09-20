import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime


# ==========================================
# تنظیمات
# ==========================================

BASE_URL = "https://www.tgju.org/profile/"

MARKETS = {
    "دلار": "price_dollar_rl",
    "یورو": "price_eur",
    "طلای 18 عیار": "geram18",
    "سکه امامی": "sekee",
    "انس طلا": "ons"
}


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "fa-IR,fa;q=0.9,en;q=0.8"
}


# ==========================================
# دریافت صفحه
# ==========================================

def get_page(url):

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
    )

    if response.status_code != 200:
        print(f"خطا در دریافت صفحه: {response.status_code}")
        return None

    return response.text


# ==========================================
# تبدیل اعداد فارسی و عربی به انگلیسی
# ==========================================

def normalize_digits(text):

    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    english_digits = "0123456789"

    translation_table = str.maketrans(
        persian_digits + arabic_digits,
        english_digits + english_digits
    )

    return text.translate(translation_table)


# ==========================================
# استخراج قیمت با BeautifulSoup + Regex
# ==========================================

def extract_price(html):

    soup = BeautifulSoup(html, "html.parser")

    # کل متن صفحه
    text = soup.get_text(" ", strip=True)

    # تبدیل اعداد فارسی/عربی
    text = normalize_digits(text)

    # Regex برای پیدا کردن "نرخ فعلی"
    pattern = r"نرخ فعلی\s*[:：]?\s*([\d,]+(?:\.\d+)?)"

    match = re.search(pattern, text)

    if not match:
        return None

    price = match.group(1)

    return price


# ==========================================
# دریافت قیمت تمام بازارها
# ==========================================

def get_all_prices():

    prices = {}

    for market_name, slug in MARKETS.items():

        url = BASE_URL + slug

        print(f"در حال دریافت {market_name}...")

        html = get_page(url)

        if html is None:
            prices[market_name] = "دریافت نشد"
            continue

        price = extract_price(html)

        if price is None:
            prices[market_name] = "پیدا نشد"
        else:
            prices[market_name] = price

    return prices


# ==========================================
# نمایش نتیجه
# ==========================================

def show_prices(prices):

    print("\n")
    print("=" * 55)
    print("       قیمت لحظه‌ای طلا و ارز")
    print("=" * 55)

    for name, price in prices.items():

        print(f"{name:<20} : {price}")

    print("=" * 55)


# ==========================================
# اجرای برنامه
# ==========================================

prices = get_all_prices()

show_prices(prices)

print(
    f"\nزمان دریافت اطلاعات: "
    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)