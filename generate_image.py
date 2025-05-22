import base64
import json
import requests
import time
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


def generate_image_with_text(
    word, definition, output_path="./image.png", position="top-left"
):
    """
    Generate image with text
    """

    api_key = "B9458F5B1553027A378FCF195C91F65E"
    secret_key = "CCE87E040997BA70BAF240C9A2127FCA"
    url = "https://api-key.fusionbrain.ai/"

    config = {
        "word": word,
        "definition": definition,
        "output_path": output_path,
        "font_path": "arial_unicode.ttf",
        "word_font_ratio": 0.1,
        "def_font_ratio": 0.066,
        "margin_ratio": 0.05,
        "brightness_threshold": 127,
        "position": position,
    }

    auth_headers = {
        "X-Key": f"Key {api_key}",
        "X-Secret": f"Secret {secret_key}",
    }

    response = requests.get(url + "key/api/v1/pipelines", headers=auth_headers)
    pipeline_id = response.json()[0]["id"]

    params = {
        "type": "GENERATE",
        "numImages": 1,
        "width": 1024,
        "height": 1024,
        "generateParams": {"query": f"{word}: {definition}"},
    }

    data = {
        "pipeline_id": (None, pipeline_id),
        "params": (None, json.dumps(params), "application/json"),
    }

    response = requests.post(
        url + "key/api/v1/pipeline/run", headers=auth_headers, files=data
    )

    request_id = response.json()["uuid"]

    attempts = 20
    delay = 2
    image_data = None

    while attempts > 0:
        response = requests.get(
            url + "key/api/v1/pipeline/status/" + request_id, headers=auth_headers
        )
        data = response.json()
        if data["status"] == "DONE":
            image_data = data["result"]["files"][0]
            break

        attempts -= 1
        time.sleep(delay)

    if not image_data:
        raise Exception("Unable to genereate an image.")

    image_bytes = base64.b64decode(image_data)
    img = Image.open(BytesIO(image_bytes))

    result_image = apply_text_overlay(img, config)

    return result_image


def apply_text_overlay(img, config):
    """
    Apply text overlay
    """

    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")

    text_color, outline_color = determine_text_colors(img, config)

    try:
        word_font = ImageFont.truetype(
            config["font_path"], size=int(img.size[1] * config["word_font_ratio"])
        )
        def_font = ImageFont.truetype(
            config["font_path"], size=int(img.size[1] * config["def_font_ratio"])
        )
    except IOError:
        word_font = ImageFont.load_default()
        def_font = ImageFont.load_default()

    width, height = img.size
    margin = int(width * config["margin_ratio"])

    if config["position"] == "top-right":
        anchor = "rt"
        word_pos = (width - margin, margin)
        def_pos = (width - margin, margin + int(height * 0.1))
    elif config["position"] == "top-left":
        anchor = "lt"
        word_pos = (margin, margin)
        def_pos = (margin, margin + int(height * 0.1))
    elif config["position"] == "bottom-right":
        anchor = "rb"

        lines = split_text_into_lines(config["definition"], 30)
        def_height = len(lines) * (
            def_font.getbbox("Hg")[3] - def_font.getbbox("Hg")[1]
        )

        word_pos = (width - margin, height - margin - def_height)
        def_pos = (width - margin, height - margin)
    elif config["position"] == "bottom-left":
        anchor = "lb"

        lines = split_text_into_lines(config["definition"], 30)
        def_height = len(lines) * (
            def_font.getbbox("Hg")[3] - def_font.getbbox("Hg")[1]
        )

        word_pos = (margin, height - margin - def_height)
        def_pos = (margin, height - margin)
    else:
        anchor = "rt"
        word_pos = (width - margin, margin)
        def_pos = (width - margin, margin + int(height * 0.1))

    draw = ImageDraw.Draw(img)

    draw_text_with_outline(
        draw, config["word"], word_pos, word_font, text_color, outline_color, anchor
    )

    draw_multiline_text(
        draw,
        config["definition"],
        def_pos,
        def_font,
        text_color,
        outline_color,
        30,
        anchor,
        config["position"],
    )

    if config["output_path"]:
        img.save(config["output_path"])

    return img


def determine_text_colors(img, config):
    """
    Determine text colors
    """

    width, height = img.size

    if config["position"] == "top-right":
        region = img.crop((width - width // 3, 0, width, height // 3))
    elif config["position"] == "top-left":
        region = img.crop((0, 0, width // 3, height // 3))
    elif config["position"] == "bottom-right":
        region = img.crop((width - width // 3, height - height // 3, width, height))
    elif config["position"] == "bottom-left":
        region = img.crop((0, height - height // 3, width // 3, height))
    else:
        region = img

    gray_region = region.convert("L")
    brightness = sum(gray_region.getdata()) / (gray_region.width * gray_region.height)

    if brightness > config["brightness_threshold"]:
        return (0, 0, 0), (255, 255, 255)
    return (255, 255, 255), (0, 0, 0)


def draw_text_with_outline(
    draw, text, position, font, text_color, outline_color, anchor
):
    """
    Draw text with outline
    """
    x, y = position

    for dx in [-2, 0, 2]:
        for dy in [-2, 0, 2]:
            if dx != 0 or dy != 0:
                draw.text(
                    (x + dx, y + dy), text, font=font, fill=outline_color, anchor=anchor
                )

    draw.text(position, text, font=font, fill=text_color, anchor=anchor)


def split_text_into_lines(text, max_length):
    """
    Split text into lines
    """
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + " " + word) <= max_length:
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def draw_multiline_text(
    draw,
    text,
    position,
    font,
    text_color,
    outline_color,
    max_line_length,
    anchor,
    pos_type,
):
    """
    Draw multiline text
    """
    lines = split_text_into_lines(text, max_line_length)
    x, y = position

    bbox = font.getbbox("Hg")
    line_height = bbox[3] - bbox[1]

    if "bottom" in pos_type:
        for i, line in enumerate(reversed(lines)):
            current_y = y - (i * line_height)
            draw_text_with_outline(
                draw, line, (x, current_y), font, text_color, outline_color, anchor
            )
    else:
        for i, line in enumerate(lines):
            current_y = y + (i * line_height)
            draw_text_with_outline(
                draw, line, (x, current_y), font, text_color, outline_color, anchor
            )


def get_vocabulary_info(word):
    """
    Get word information from vocabulary.com
    """

    url = f"https://www.vocabulary.com/dictionary/{word}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise KeyError("Info not available.")
    bs = BeautifulSoup(response.text, "html.parser")
    info = bs.find("meta", attrs={"name": "description"})
    if info:
        return info.get("content")
    else:
        definitions = bs.find("div", class_="definition")
        if definitions:
            for child in definitions.children:
                if child.name != "div":
                    first_definition = str(child).strip()
                    break
            return first_definition
        else:
            raise KeyError("Info not found.")


if __name__ == "__main__":
    word = input()
    generate_image_with_text(word, get_vocabulary_info(word), f"./{word}.png")
