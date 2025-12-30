import matplotlib.pyplot as plt
import numpy as np
import json

with open('data/career-stats.json', 'r') as json_file:
    data = json.load(json_file)

players, kills, deaths, assists = [], [], [], []
max_value = 0

for p in data:
    players.append(p["Player"])
    kills.append(p["Kills"])
    deaths.append(p["Deaths"])
    assists.append(p["Assists"])
    max_value = max(max_value, p["Kills"], p["Deaths"], p["Assists"])

x = np.arange(len(players))
width = 0.25

fig, ax = plt.subplots(figsize=(len(players) * 0.4, 8))

bars_kills = ax.bar(x - width, kills, width, label='Kills', color="#099d11")
bars_deaths = ax.bar(x, deaths, width, label='Deaths', color="#b30909")
bars_assists = ax.bar(x + width, assists, width, label='Assists', color="#0178a8")

# 🔥 VALORES EM CIMA DAS BARRAS
ax.bar_label(bars_kills, padding=3, fontsize=7)
ax.bar_label(bars_deaths, padding=3, fontsize=7)
ax.bar_label(bars_assists, padding=3, fontsize=7)

ax.set_title('Players attributes by KDA')
ax.set_xticks(x)
ax.set_xticklabels(players, rotation=60, ha='right')
ax.legend()
ax.set_ylim(0, round(max_value, -2))

plt.tight_layout()
plt.show()
