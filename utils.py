import requests
from bs4 import BeautifulSoup

def get_live_streamers(usernames):
    live_streamers = []
    for username in usernames:
        url = f"https://twitchfa.tv/streamer/{username}"
        response = requests.get(url)
        if response.status_code != 200:
            continue
        soup = BeautifulSoup(response.text, 'html.parser')
        view_count_elem = soup.select_one("span.text-viewers")
        if view_count_elem:
            views = int(view_count_elem.text.strip().replace("نفر", "").strip())
            live_streamers.append((username, views))
    return sorted(live_streamers, key=lambda x: x[1], reverse=True)

def read_streamers():
    try:
        with open("streamers.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def add_streamer(username):
    usernames = read_streamers()
    if username not in usernames:
        with open("streamers.txt", "a") as f:
            f.write(username + "\n")
        return True
    return False
