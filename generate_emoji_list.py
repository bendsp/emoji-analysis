#!/usr/bin/env python3
import emoji
import json
import re
import random
from render_emoji import render_emoji
import os
import sys
import unicodedata
from PIL import Image

def analyze_image(image_path):
    if not os.path.exists(image_path):
        return None, None

    with Image.open(image_path) as img:
        img = img.convert("RGBA")
        pixels = list(img.getdata())

        total_pixels = len(pixels)
        transparent_pixels = sum(1 for p in pixels if p[3] == 0)
        area_ratio = 1 - (transparent_pixels / total_pixels)

        channels = list(zip(*pixels))
        avg_rgb = tuple(sum(channels[i]) // total_pixels for i in range(3))

        return avg_rgb, area_ratio

def generate_emoji_list():
    all_emojis = emoji.EMOJI_DATA
    emoji_list = []
    seen_emojis = set()

    pictorial_categories = {
        'face', 'person', 'animal', 'food', 'plant', 'place',
        'transport', 'object', 'symbol', 'flag'
    }

    excluded_patterns = [
        r'^:[a-z0-9_\-]+:$',
        r'^\d+.*$',
        r'^[#*].*$',
        r'^[↖↙↗↘⬆⬇].*$',
    ]

    for emoji_char, data in all_emojis.items():
        if any(re.match(pattern, emoji_char) for pattern in excluded_patterns):
            continue

        if len(emoji_char) == 1 and ord(emoji_char) < 0x1F000:
            continue

        emoji_group = data.get('group', '').lower()
        is_pictorial = any(category in emoji_group for category in pictorial_categories)

        if not emoji_group or not is_pictorial:
            code_point = ord(emoji_char[0])
            is_pictorial = (0x1F300 <= code_point <= 0x1F9FF) or (0x2600 <= code_point <= 0x26FF)

        if is_pictorial:
            shortcode = data.get('en', '')
            clean_name = shortcode.strip(':')
            normalized_emoji = unicodedata.normalize('NFC', emoji_char)
            if normalized_emoji not in seen_emojis:
                seen_emojis.add(normalized_emoji)
                emoji_list.append({'emoji': normalized_emoji, 'name': clean_name})

    emoji_list.sort(key=lambda x: ord(x['emoji'][0]))
    return emoji_list

def save_emoji_list(emoji_list, filename='emoji_list.json', output_dir='emojis/', skip_render=False):
    os.makedirs(output_dir, exist_ok=True)

    for emoji_item in emoji_list:
        emoji_char = emoji_item['emoji']
        emoji_name = emoji_item['name'].replace(" ", "_")
        output_path = os.path.join(output_dir, f"{emoji_name}.png")

        if not skip_render:
            render_emoji(emoji_char, output_path)

        avg_rgb, area = analyze_image(output_path)
        emoji_item['rgb'] = avg_rgb
        emoji_item['area'] = area
        print(f"Processed {emoji_char}: RGB={avg_rgb}, Area Ratio={area}")

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(emoji_list, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(emoji_list)} emojis to {filename}")

def print_emoji_sample(emoji_list, count=10):
    print(f"Sample of {count} random emojis from the list:")
    sample_count = min(count, len(emoji_list))
    for i, emoji_item in enumerate(random.sample(emoji_list, sample_count)):
        print(f"{i+1}. {emoji_item['emoji']} - {emoji_item['name']}")

if __name__ == "__main__":
    skip_render = '--skip' in sys.argv
    emoji_list = generate_emoji_list()
    print(f"Total pictorial emojis found: {len(emoji_list)}")
    print_emoji_sample(emoji_list)
    save_emoji_list(emoji_list, skip_render=skip_render)