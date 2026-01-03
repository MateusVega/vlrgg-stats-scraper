import matplotlib.pyplot as plt
import numpy as np
import json
import math

mode_full_name = {
    "K" : "Kills",
    "D" : "Deaths",
    "A" : "Assists",
    "KDA" : "KDA"
}

def gen_graph_bars(filename, mode, title, max_players, download, output_file):
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print("\n\033[31m✖ The file does not exist.\nIf the file is inside data folder, remember writing 'data/' before the file name.\033[0m\n")
        exit(1)
    except OSError as e:
        print(f"\n\033[31m ✖ I/O error: {e}\033[0m\n")
        exit(1)

    if mode != "KDA":
        data = sorted(data, key=lambda x: x[mode_full_name[mode]], reverse=True)[:max_players]
    else:
        data = sorted(data, key=lambda x: ((x["Kills"] + x["Deaths"]) / x["Deaths"]), reverse=True)[:max_players]
    
    players = []
    if mode == "K":
        kills = []
    elif mode == "D":
        deaths = []
    elif mode == "A":
        assists = []
    elif mode == "KDA":
        kda = []
    max_value = 0

    for p in data:
        players.append(p["Player"])
        if mode == "K":
            kills.append(p["Kills"])
            max_value = max(max_value, p["Kills"])
        elif mode == "D":
            deaths.append(p["Deaths"])
            max_value = max(max_value, p["Deaths"])
        elif mode == "A":
            assists.append(p["Assists"])
            max_value = max(max_value, p["Assists"])
        elif mode == "KDA":
            kda_value = round((p["Kills"] + p["Deaths"]) / p["Deaths"], 2)
            kda.append(kda_value)
            max_value = max(max_value, kda_value)

    x = np.arange(len(players))
    width = 0.25

    fig, ax = plt.subplots()

    if mode == "K":
        bars_kills = ax.bar(x, kills, width, label='Kills', color="#099d11")
        ax.bar_label(bars_kills, padding=3, fontsize=7)
    elif mode == "D":
        bars_deaths = ax.bar(x, deaths, width, label='Deaths', color="#b30909")
        ax.bar_label(bars_deaths, padding=3, fontsize=7)
    elif mode == "A":
        bars_assists = ax.bar(x, assists, width, label='Assists', color="#0178a8")
        ax.bar_label(bars_assists, padding=3, fontsize=7)
    elif mode == "KDA":
        bars_kda = ax.bar(x, kda, width, label='KDA', color="#d99f09")
        ax.bar_label(bars_kda, padding=3, fontsize=7)

    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(players, rotation=60, ha='right')
    ax.legend()
    top = math.ceil(max_value * 1.1)
    ax.set_ylim(0, top)

    plt.tight_layout()

    if download:
        plt.gcf()
        plt.savefig(f"graphs/{output_file}.png")
        print(f"\nDone! Picture saved as: {output_file}.png.")

    plt.show()


if __name__ == '__main__':
    print("=== VLR Stats Graph Generator ===")

    while True:
        filename = input("Stats file path (e.g. data/career-stats.json): ").strip()
        if filename == "":
            print("Input the file path.")
        elif not filename.lower().endswith(".json"):
            print("Input a file path from a '.json' file")
        else:
            break

    mode_map = {
        "KILLS" : "K",
        "DEATHS" : "D",
        "ASSISTS" : "A"
    }

    while True:
        mode = input("Choose the data to analyze (K / D / A / KDA): ").strip().upper()
        if mode in {"K", "D", "A", "KDA"}:
            break
        if mode in {"KILLS", "DEATHS", "ASSISTS"}:
            mode = mode_map[mode]
            break
        print("Input K, D, A or KDA")

    while True:
        title = input("Graph title (e.g. Champions 2023 – Kills): ")
        if title != "":
            break
        print("Input a title.")

    while True:
        try:
            max_players = int(input("Number of players to display (Top X — 15–20 recommended — large values may clutter the graph.): "))
            if max_players <= 0:
                raise ValueError
            break
        except ValueError:
            print("Enter a valid positive number.")

    while True:
        download = input("Save graph as image? (Y/n): ").strip().lower()
        if download in {"y", "n"}:
            download = (download == "y")
            break
        print("Input 'y' or 'n'")

    if download:
        output_file = input("Output file name (without .png): ").strip()
        if output_file.endswith(".png"):
            output_file = output_file[:-4]
        if output_file == "":
            print("\n\033[31m✖ Output file name cannot be empty when download is enabled.\033[0m\n")
            exit(1)
    else:
        output_file = ""

    gen_graph_bars(
        filename=filename,
        mode=mode,
        title=title,
        max_players=max_players,
        download=download,
        output_file=output_file,
    )