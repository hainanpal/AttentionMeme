from dataclasses import dataclass
from pathlib import Path

import re
import yaml

IMAGE_EXTS = {".png", ".jpg", ".jpeg"}
POINT_PATTERN = re.compile(r"^(\d+)-(.*)$")

@dataclass
class PointItem:
    index: int
    text: str
    image_path: Path

# ---------------------
# layout
# ---------------------
@dataclass
class LayoutConfig:
    points_per_row: int
    margin: int
    row_spacing: int
    column_spacing: int
    title_image_text_spacing: int


# ---------------------
# font
# ---------------------
@dataclass
class FontConfig:
    title_size: int
    point_text_size: int
    font_file: str


# ---------------------
# image
# ---------------------
@dataclass
class ImageConfig:
    title_image_size: int
    point_image_size: int


# ---------------------
# canvas
# ---------------------
@dataclass
class CanvasConfig:
    top_margin: int
    section_spacing: int
    side_margin: int


# ---------------------
# root config
# ---------------------
@dataclass
class AppConfig:
    title_text: str
    layout: LayoutConfig
    font: FontConfig
    image: ImageConfig
    canvas: CanvasConfig

def load_points(input_dir: str) -> list[PointItem]:
    points: list[PointItem] = []

    input_path = Path(input_dir)
    for path in input_path.iterdir():
        if not path.is_file():
            continue

        if path.suffix.lower() not in IMAGE_EXTS:
            continue

        stem = path.stem  # 不含扩展名
        match = POINT_PATTERN.match(stem)
        if not match:
            continue  # 不是吐槽点文件，直接忽略

        index = int(match.group(1))
        text = match.group(2).strip()

        if not text:
            raise ValueError(f"吐槽点文件名缺少文本内容: {path.name}")

        points.append(
            PointItem(
                index=index,
                text=text,
                image_path=path
            )
        )

    if not points:
        raise ValueError("未找到任何吐槽点图片")

    # 按 index 排序
    points.sort(key=lambda p: p.index)
    return points


def load_config(input_dir: str) -> dict:
    config_path = Path(input_dir) / "config.yaml"
    if not config_path.exists():
        raise FileNotFoundError("未找到 config.yaml")

    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not isinstance(config, dict):
        raise ValueError("config.yaml 顶层必须是一个 mapping")

    return config

def parse_config(raw: dict) -> AppConfig:
    return AppConfig(
        title_text=raw["title_text"],
        layout=LayoutConfig(**raw["layout"]),
        font=FontConfig(**raw["font"]),
        image=ImageConfig(**raw["image"]),
        canvas=CanvasConfig(**raw["canvas"]),
    )


def load_title_img(input_dir: str) -> Path:
    input_path = Path(input_dir)
    for path in input_path.iterdir():
        if not path.is_file():
            continue
        if path.suffix.lower() not in IMAGE_EXTS:
            continue
        if path.stem == "title":
            return path
    raise ValueError("找不到名为title的图片")