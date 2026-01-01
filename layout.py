import sys

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from config_loader import load_points, load_config, load_title_img, parse_config

import argparse

# 图片背景色
BG_COLOR = (245, 245, 245)

def load_all_configs(input_dir: str):
    points = load_points(input_dir)
    config = load_config(input_dir)
    title = load_title_img(input_dir)
    return title, points, parse_config(config)

def resize_and_crop(image: Image.Image, size: int) -> Image.Image:
    w, h = image.size
    scale = size / min(w, h)
    new_w, new_h = int(w * scale), int(h * scale)

    image = image.resize((new_w, new_h), Image.Resampling.LANCZOS)

    left = (new_w - size) // 2
    top = (new_h - size) // 2
    right = left + size
    bottom = top + size

    return image.crop((left, top, right, bottom))


def draw_meme(input_dir: str):
    title, points, config = load_all_configs(input_dir)

    # 计算画布高度
    rows = (len(points) + config.layout.points_per_row - 1) // config.layout.points_per_row
    points_block_height = (
        rows * (config.image.point_image_size + config.font.point_text_size + config.layout.margin)
        + (rows - 1) * config.layout.row_spacing
    )
    canvas_height = (
        config.canvas.top_margin
        + max(config.image.title_image_size, config.font.title_size)
        + config.canvas.section_spacing
        + points_block_height
        + config.canvas.top_margin
    )
    canvas_width = (
        config.canvas.side_margin
        + config.layout.points_per_row * config.image.point_image_size
        + (config.layout.points_per_row - 1) * config.layout.column_spacing
        + config.canvas.side_margin
    )

    # 创建画布
    img = Image.new("RGB", (canvas_width, canvas_height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 加载字体
    font_title = ImageFont.truetype(
        config.font.font_file,
        config.font.title_size
    )
    font_point = ImageFont.truetype(
        config.font.font_file,
        config.font.point_text_size
    )

    # 画标题区域
    title_text_bbox = draw.textbbox((0, 0), config.title_text, font=font_title)
    title_text_width = title_text_bbox[2] - title_text_bbox[0]

    total_title_width = (
        config.image.title_image_size
        + config.layout.title_image_text_spacing
        + title_text_width
    )

    if total_title_width > canvas_width:
        raise ValueError("标题宽度大于画布宽度，请考虑在每行排版更多的元素")
    start_x = (canvas_width - total_title_width) // 2
    center_y = config.canvas.top_margin + config.image.title_image_size // 2

    # 图标方框
    icon_x = int(start_x)
    icon_y = config.canvas.top_margin
    title_img = Image.open(title).convert("RGBA")
    title_img = resize_and_crop(title_img, config.image.title_image_size)
    img.paste(title_img, (icon_x, icon_y), title_img)
    
    # 标题文字
    text_x = (
        icon_x
        + config.image.title_image_size
        + config.layout.title_image_text_spacing
    )
    text_y = center_y - config.font.title_size // 2
    draw.text((text_x, text_y), config.title_text, fill="black", font=font_title)

    # 画吐槽点区域
    current_y = (
        config.canvas.top_margin
        + config.image.title_image_size
        + config.canvas.section_spacing
    )

    for idx, item in enumerate(points):
        row = idx // config.layout.points_per_row
        col = idx % config.layout.points_per_row

        x = (
            config.canvas.side_margin
            + col * (config.image.point_image_size + config.layout.column_spacing)
        )
        y = current_y + row * (
            config.image.point_image_size
            + config.font.point_text_size
            + config.layout.margin
            + config.layout.row_spacing
        )

        # 图片
        point_img = Image.open(item.image_path).convert("RGBA")
        point_img = resize_and_crop(point_img, config.image.point_image_size)
        img.paste(point_img, (x, y), point_img)

        # 文本
        text_bbox = draw.textbbox((0, 0), item.text, font=font_point)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = x + (config.image.point_image_size - text_width) // 2
        text_y = y + config.image.point_image_size + config.layout.margin
        draw.text((text_x, text_y), item.text, fill="black", font=font_point)
    
    # 保存
    img.save(Path(input_dir) / "output.png")
    print("输出保存到：" + str((Path(input_dir) / "output.png").absolute()))
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir")

    args = parser.parse_args()
    input_dir = Path(args.input_dir)

    if not input_dir.exists():
        print(f"路径不存在：{input_dir}")
        sys.exit(1)

    if not input_dir.is_dir():
        print(f"路径不是目录：{input_dir}")
        sys.exit(1)

    draw_meme(str(input_dir))
