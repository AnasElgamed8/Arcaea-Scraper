# Arcaea Scraper

***Arcaea online subscribtion needed*** 

A small script that fetches your scores from Arcaea's website

## Features

- Fetch all scores accross all difficulties
- Clean fetched scores and store them in a clean CSV
- B30 scores fetching (WIP)
- Creates a scores spreadsheet with your scores (WIP)

## Usage

### 1. Clone the repo

```bash
git clone https://github.com/AnasElgamed8/Arcaea-Scraper.git
cd Arcaea-Scraper
```

### 2. Get your cookie

open https://arcaea.lowiro.com/ and sign in

use a cookie editor browser extension, the value you need is in the "sid" field.

### 3. Save the cookie

open `example.env` and save your cookie there, then rename the file to `.env`

### 4. Run the script
uv required, you will have to install that first

```bash
uv sync
uv run src/Arcaea.py
```

Your scores will be saved in `data/`

## What's next

I will likely rework the whole project's structure, and I might add flet/streamlit integration

this is just the beginning
