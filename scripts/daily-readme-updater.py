#!/usr/bin/env python3

import os
import json
import random
import sys
from datetime import datetime


class ReadmeUpdater:
    def __init__(self):
        # Seasonal images mapping (MMDD format)
        self.SEASONAL_IMAGES = {
            "1031": "halloween.png",
            "0908": "birthday.png",
            "0905": "onam.png",
            "0422": "earthday.png",
            "0912": "programmersday.png",
            "1225": "christmas.png",
            "1231": "newyear.png",
            "0101": "newyear.png",
            "1231-0101": "newyear.png",
        }

        # File paths (relative to repository root)
        self.SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.README_PATH = os.path.join(os.path.dirname(self.SCRIPT_DIR), "README.md")
        self.QUOTES_PATH = os.path.join(self.SCRIPT_DIR, "data", "quotes.json")

    def get_seasonal_image(self, default_image="header.png"):
        """
        Get the appropriate seasonal image based on current date.
        Returns default_image if no seasonal image matches.
        """
        today = datetime.now().strftime("%m%d")

        # Check exact match first
        if today in self.SEASONAL_IMAGES:
            return self.SEASONAL_IMAGES[today]

        # Check date ranges
        for date_range, image in self.SEASONAL_IMAGES.items():
            if "-" in date_range:
                start_date, end_date = date_range.split("-")
                if self.is_date_in_range(today, start_date, end_date):
                    return image

        return default_image

    def is_date_in_range(self, today, start, end):
        """
        Check if today's date (MMDD) is within a date range.
        Handles year-end wrapping.
        """
        if start <= end:
            return start <= today <= end
        else:
            # e.g., 1231–0101
            return today >= start or today <= end

    def get_daily_quote(self):
        """Get quote of the day or fallback message from quotes.json."""
        try:
            with open(self.QUOTES_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)

            today = datetime.now().strftime("%m-%d")
            special = data.get("special_days", {})
            random_quotes = data.get("random_quotes", [])

            return special.get(today, random.choice(random_quotes) if random_quotes else "Honestly, I think the computer is doing most of the work here.")
        except Exception as e:
            print(f"[ERROR] Failed to read quote: {e}")
            return "Honestly, I think the computer is doing most of the work here."  # Safe fallback

    def update_readme(self):
        """Update README.md with seasonal image and daily quote."""
        try:
            with open(self.README_PATH, "r", encoding="utf-8") as file:
                lines = file.readlines()

            seasonal_image = self.get_seasonal_image()
            lines[0] = (
                f"![HEADER](https://github.com/theamallalgi/TheAmalLalgi/blob/main/dependencies/{seasonal_image}?raw=true)\n"
            )

            daily_quote = self.get_daily_quote()
            lines[5] = f"> {daily_quote}\n"

            with open(self.README_PATH, "w", encoding="utf-8") as file:
                file.writelines(lines)

            print(f"[INFO] Updated README with image: {seasonal_image}")
            print(f"[INFO] Updated quote: {daily_quote}")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to update README: {e}")
            return False


def main():
    updater = ReadmeUpdater()
    success = updater.update_readme()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
