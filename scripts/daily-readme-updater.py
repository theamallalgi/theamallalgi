#!/usr/bin/env python3

import os
import json
import random
from datetime import datetime


class ReadmeUpdater:
    def __init__(self):
        # Seasonal images mapping (MMDD format)
        self.SEASONAL_IMAGES = {
            # Holiday images
            "1031": "halloween.png",
            "0908": "birthday.png",
            "2204": "earthday.png",
            "0701": "programmersday.png",
            "1225": "christmas.png",
            "3112": "newyear.png",
            "0101": "newyear.png",
            # Holiday ranges
            # "3112-0101": "newyear.png",
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

        # Check exact date matches
        if today in self.SEASONAL_IMAGES:
            return self.SEASONAL_IMAGES[today]

        # Check date ranges
        for date_range, image in self.SEASONAL_IMAGES.items():
            if "-" in date_range:
                start_date, end_date = date_range.split("-")
                if start_date <= today <= end_date:
                    return image

        return default_image

    def get_daily_quote(self):
        """Get quote of the day or special message from quotes.json."""
        try:
            with open(self.QUOTES_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)

            today = datetime.now().strftime("%m-%d")
            # Return special day quote if exists, otherwise random quote
            return data["special_days"].get(today, random.choice(data["random_quotes"]))
        except Exception as e:
            print(f"Error getting quote: {e}")
            return "Welcome to my profile!"  # Fallback quote

    def update_readme(self):
        """Update README with new image and quote."""
        try:
            # Read current README content
            with open(self.README_PATH, "r", encoding="utf-8") as file:
                lines = file.readlines()

            # Update header image (line 1)
            seasonal_image = self.get_seasonal_image()
            lines[0] = (
                f"![HEADER](https://github.com/theamallalgi/TheAmalLalgi/blob/main/dependencies/{seasonal_image}?raw=true)\n"
            )

            # Update quote (line 5)
            daily_quote = self.get_daily_quote()
            lines[5] = f"> {daily_quote}\n"

            # Write updated content
            with open(self.README_PATH, "w", encoding="utf-8") as file:
                file.writelines(lines)

            print(f"Updated README with image: {seasonal_image}")
            print(f"Updated quote to: {daily_quote}")
            return True

        except Exception as e:
            print(f"Error updating README: {e}")
            return False


def main():
    updater = ReadmeUpdater()
    success = updater.update_readme()

    # Exit with appropriate status code for GitHub Actions
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
