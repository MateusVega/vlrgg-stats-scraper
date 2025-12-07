import json
import time
import requests as r
from bs4 import BeautifulSoup
import os
import random


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

json_path = os.path.join(BASE_DIR, "data", "players.json")

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"}

full_stats = []

def fetch(url):
    try:
        response = r.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response
    except r.RequestException as e:
        raise RuntimeError(f"Erro ao acessar {url}: {e}")

def get_picture(url):
    request = fetch(f"https://www.vlr.gg{url}/?timespan=all")
    site = BeautifulSoup(request.text, "html.parser")
    return site.select_one(".wf-avatar img")["src"]

def append_player_stats(id, name, img_url, kills, deaths, assists):
    player_stats = {
        "id" : id,
        "Player" : name,
        "Img" : img_url,
        "Kills" : kills,
        "Deaths" : deaths,
        "Assists" : assists
    }
    full_stats.append(player_stats)

def scraper(mode, urls, output_file_name, skip_players_without_picture=True):
    # mode -> "tournament" or "carrer"

    if len(urls) == 0:
        raise ValueError(f"The application needs at least one url.")
    
    players_links = []

    if mode == "carrer":
        for link in urls:
            request = fetch(link)
            site = BeautifulSoup(request.text, "html.parser")
            players = site.select("tr .mod-player a")
            for player in players:
                if not (player["href"] in players_links):
                    players_links.append(player["href"])

        for player in players_links:
            request = fetch(f"https://www.vlr.gg{player}/?timespan=all")
            site = BeautifulSoup(request.text, "html.parser")
            kills = 0
            deaths = 0
            assists = 0
            img_url = site.select_one(".wf-avatar img")["src"]
            if img_url == "/img/base/ph/sil.png" and skip_players_without_picture:
                continue
            stats = site.select("tbody tr")
            for s in stats:
                kills += int(s.select("td")[-4].text)
                deaths += int(s.select("td")[-3].text)
                assists += int(s.select("td")[-2].text)
            name = player.split("/")[-1].replace("'", "")
            id = player.split("/")[-2]
            append_player_stats(id, name, img_url, kills, deaths, assists)
            time.sleep(random.uniform(0.5, 1.2))
    elif mode == "tournament":
        if len(urls) > 1:
            raise ValueError(f"'tournament' mode just accept one url")
        request = fetch(urls[0])
        site = BeautifulSoup(request.text, "html.parser")
        players = site.select("tbody tr")
        for player in players:
            img_url = get_picture(player.select_one(".mod-player a")["href"])
            if img_url == "/img/base/ph/sil.png" and skip_players_without_picture:
                continue
            kills = int(player.select("td")[-5].text)
            deaths = int(player.select("td")[-4].text)
            assists = int(player.select("td")[-3].text)
            name = player.select_one(".mod-player a")["href"].split("/")[-1]
            id = player.select_one(".mod-player a")["href"].split("/")[-2]
            append_player_stats(id, name, img_url, kills, deaths, assists)
            time.sleep(random.uniform(0.5, 1.2))
    else:
        raise ValueError(f"Invalid Mode: {mode}. Use 'tournament' or 'carrer'.")
    
    with open(f"{output_file_name}.json", 'w', encoding="utf-8") as json_file:
        json.dump(full_stats, json_file, ensure_ascii=False, indent=4)

list_url_exemples = [
    "https://www.vlr.gg/event/stats/2283/valorant-champions-2025?exclude=33667.33671.33651.33652.33653.33654.33655.33656.33657.33658.33659.33660.33661.33662.33663.33664.33665.33666&min_rounds=0&agent=all"
]

if __name__ == '__main__':
    scraper(mode="tournament", urls=list_url_exemples, output_file_name="json_cool")