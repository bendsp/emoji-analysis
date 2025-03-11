# Emoji Info

**Emoji Info** is a tool that extracts and analyzes emoji images to compute their **average color** and **visibility area**. It processes emojis, determines their dominant color based on non-transparent pixels, and calculates how much of the image is actually visible.

> [!TIP]
> If you only want the resulting data, it's free to use and contained in `emoji_list.json`

## Features

- Extracts emojis and saves them as images
- Computes the **average RGB color**
- Calculates the **visible area ratio** (0 to 1) based on transparency
- Supports skipping image re-rendering for faster processing

## Installation

Clone the repository and install dependencies:

```sh
git clone https://github.com/bendsp/emoji-info.git
cd emoji-info
pip install -r requirements.txt
```

## Usage

To generate and analyze emojis, run:

```sh
python generate_emoji_list.py
```

To skip re-rendering emoji images and only recalculate the data:

```sh
python generate_emoji_list.py --skip
```

## Output

The script generates an `emoji_list.json` file resembling the following:

```json
[
  {
    "emoji": "☃️",
    "name": "snowman",
    "unicode": "U+2603 U+FE0F",
    "rgb": [164, 174, 181],
    "area": 0.631317138671875
  },
  {
    "emoji": "☄️",
    "name": "comet",
    "unicode": "U+2604 U+FE0F",
    "rgb": [228, 156, 113],
    "area": 0.531829833984375
  },
  {
    "emoji": "☎️",
    "name": "telephone",
    "unicode": "U+260E U+FE0F",
    "rgb": [188, 83, 80],
    "area": 0.8698272705078125
  }
]
```

## How It Works

1. **Extracts Emoji Data** – Uses `emoji.EMOJI_DATA` to find and categorize emojis.
2. **Renders Each Emoji** – Saves emojis as PNG images.
3. **Analyzes Images** – Opens each emoji image and calculates:
   - The **average RGB color**, considering only visible pixels.
   - The **area ratio**, measuring how much of the image is non-transparent.
4. **Saves Data** – Outputs a JSON file with the processed results.

> [!NOTE]
> Emoji Info currently only supports Apple's family of emojis.
