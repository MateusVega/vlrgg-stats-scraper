# VLR Stats Scraper

A lightweight Python tool that scrapes **player career statistics** from **VLR.gg** and exports them into a clean JSON file.  
Perfect for data analysis, small projects, or game ideas that need accurate Valorant player stats.

---

## Features
- Scrapes **kills, deaths, assists** from each player's career.
- Supports two modes:
  - **career** → Collect stats from all players found in one or more event pages.
  - **tournament** → Scrape stats directly for one or more events.
- Automatically extracts each player’s **profile picture**.
- Optionally **skips players without images**.
- Outputs structured JSON ready for use.

---

## Project Structure
```text
vlr-stats-scraper/
│
├── data/
│   └── stats.json        # generated output (example)
│
├── scraper.py            # main script with CLI
├── requirements.txt      # dependencies
└── README.md
```

## Installation
```bash
pip install -r requirements.txt
python scraper.py
```
**Note: You need Python 3.12.0 installed**

## Usage

When running the scraper, you must provide the following arguments:

### **Mode** (`Career` / `Tournament`)


### **Competition URLs**
Provide one or more links to the competitions you want to scrape.

### **Output File Name**
The name of the JSON file to generate.  
The file will be saved in the project directory.

### **Skip Players Without Profile Pictures** (`y` / `n`)
If enabled, the scraper will ignore players who do not have a profile image.

---

## Output

A structured **JSON file** containing all scraped player statistics will be generated in the project folder.

### Example Output
```json
[
    {
        "id": 0,
        "Player": "Kingg",
        "Img": "https://.../player.png",
        "Kills": 2834,
        "Deaths": 2471,
        "Assists": 912
    }
]

```


## Notes
Made for personal and educational use.

This project is not affiliated with VLR.gg.

Heavy scraping may cause temporary rate limits — use responsibly.

The scrape process may take some time too avoid request restrition
