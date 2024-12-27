import os
from datetime import datetime

# Dictionary mapping dates/periods to special images
SEASONAL_IMAGES = {
    # Holidays
    "1031": "halloween.png",
    "0908": "birthday.png",
    "2204": "earthday.png",
    "0701": "programmersday.png",
    "1225": "christmas.png",

    # Holiday seasons (date ranges)
    "3112-0101": "newyear.png",
}

def get_current_seasonal_image(default_image="header.png"):
    """
    Determine the appropriate image based on the current date.

    Args:
        default_image (str): Default image to use if no seasonal image matches

    Returns:
        str: Filename of the image to use
    """
    today = datetime.now()
    today_str = today.strftime("%m%d")

    # Check for exact date matches first
    if today_str in SEASONAL_IMAGES:
        return SEASONAL_IMAGES[today_str]

    # Check for date ranges
    for date_range, image in SEASONAL_IMAGES.items():
        if "-" in date_range:
            start_date, end_date = date_range.split("-")
            if start_date <= today_str <= end_date:
                return image

    # If no match is found, return the default image (header.png)
    return default_image

def update_readme(image_filename):
    """
    Update README.md with the new image URL in the first line.

    Args:
        image_filename (str): Filename of the image to use
    """
    readme_path = "README.md"

    # Read the content of the README.md
    with open(readme_path, 'r') as file:
        content = file.readlines()

    # Update the first line with the new image URL
    content[0] = f"![HEADER](https://github.com/theamallalgi/TheAmalLalgi/blob/main/dependencies/{image_filename}?raw=true)\n"

    # Write the updated content back to the README.md
    with open(readme_path, 'w') as file:
        file.writelines(content)

    print(f"README updated with {image_filename} in the first line.")

def main():
    # Get the seasonal image
    seasonal_image = get_current_seasonal_image()

    # Print current date and matching image
    today = datetime.now()
    print(f"Current date: {today.strftime('%d/%m')}, Matching header image: {seasonal_image}")

    # Update README with the seasonal image
    update_readme(seasonal_image)

if __name__ == "__main__":
    main()
