import random

def generate():
    browsers = [("Google Chrome", 100, 115), ("Chromium", 100, 115), ("Not:A-Brand", 99, 99)]
    platforms = ["Windows", "macOS", "Linux"]

    sec_ch_ua = ", ".join([
        f'"{name}";v="{random.randint(min_v, max_v)}"' for name, min_v, max_v in random.sample(browsers, len(browsers))
    ])
    platform = random.choice(platforms)

    return {"Sec-CH-UA": sec_ch_ua, "Sec-CH-UA-Platform": f'"{platform}"', "Sec-CH-UA-Mobile": "?0", "User-Agent": f"Mozilla/5.0 ({platform}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(100, 115)}.0.0.0 Safari/537.36"}
