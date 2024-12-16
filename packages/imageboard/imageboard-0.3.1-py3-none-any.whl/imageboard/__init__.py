"""ImageBoard is a class for displaying images with metadata in a grid."""

import importlib.resources
import logging
import os
from pathlib import Path
from typing import IO

from PIL import Image, ImageDraw, ImageFont
from pydantic import BaseModel

logger = logging.getLogger("imageboard")


class ImgRecord(BaseModel):
    """ImgRecord is a Pydantic model for an image with metadata."""

    img: Image.Image
    metadata: dict

    class Config:
        """Pydantic configuration for ImgRecord."""

        arbitrary_types_allowed = True


class ImageGrid:
    """ImageGrid is a class for displaying images in a grid."""

    def __init__(self, images: list[list[Image.Image]], labels: list[list[str]] | None = None) -> None:
        """Initialize an ImageGrid object."""
        self.images = images
        self.labels = labels

    @property
    def canvas_width(self) -> int:
        """Return the width of the canvas."""
        # 获取每列最大宽度之和
        column_widths, _ = self._compute_offsets()
        return sum(column_widths)

    @property
    def canvas_height(self) -> int:
        """Return the height of the canvas."""
        _, row_heights = self._compute_offsets()
        return sum(row_heights)

    def to_image(self) -> Image.Image:
        """Return the ImageGrid as a PIL Image."""
        img = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        font_path = importlib.resources.files("imageboard.fonts") / "Roboto-Bold.ttf"
        for i, row in enumerate(self.images):
            for j, cur in enumerate(row):
                x, y = self._item_start_xy(i, j)
                img.paste(cur, (x, y))
                if self.labels:
                    label = self.labels[i][j]
                    draw = ImageDraw.Draw(img)
                    font = ImageFont.truetype(str(font_path), cur.size[1] // 16)

                    draw.text((x, y), label, fill="white", stroke_width=2, stroke_fill="black", font=font)
        return img

    def _compute_offsets(self) -> tuple[list[int], list[int]]:
        """Compute offsets based on the maximum width of each column and maximum height of each row."""
        if not self.images:
            return [], []

        num_rows = len(self.images)
        num_cols = len(self.images[0]) if num_rows > 0 else 0

        # Calculate the max widths of each column
        column_widths = [0] * num_cols
        for i in range(num_cols):
            column_widths[i] = max(self.images[row][i].width for row in range(num_rows))

        # Calculate the max heights of each row
        row_heights = [0] * num_rows
        for j in range(num_rows):
            row_heights[j] = max(self.images[j][col].height for col in range(num_cols))

        return column_widths, row_heights

    def _item_start_xy(self, i: int, j: int) -> tuple[int, int]:
        """Return the starting coordinates of the item."""
        column_widths, row_heights = self._compute_offsets()

        # Calculate x coordinate by summing widths of all preceding columns
        x = sum(column_widths[:j])

        # Calculate y coordinate by summing heights of all preceding rows
        y = sum(row_heights[:i])

        return (x, y)


class ImageBoard:
    """ImageBoard is a class for displaying images with metadata in a grid."""

    def __init__(self) -> None:
        """Initialize an ImageBoard object."""
        self.data: list[ImgRecord] = []

    def append(self, img: Image.Image | str | bytes | os.PathLike | IO[bytes], data: dict) -> None:
        """Append an image with metadata to the ImageBoard."""
        image = img if isinstance(img, Image.Image) else Image.open(img)
        self.data.append(ImgRecord(img=image, metadata=data))

    def load(self, path: Path | str) -> None:
        """Load an ImageBoard object from a file."""
        path = Path(path)
        if not path.exists():
            logger.warning("File does not exist.")
            return

    def _calculate_max_image_height(self, images: list[Image.Image]) -> int:
        """Calculate the maximum image height."""
        return max(image.size[1] for image in images)

    def _resize_images_to_max_height(self, images: list[Image.Image], max_height: int) -> list[Image.Image]:
        """Resize images to the maximum height while maintaining aspect ratio."""
        resized_images = []
        for image in images:
            aspect_ratio = image.size[0] / image.size[1]
            new_width = int(max_height * aspect_ratio)
            resized_images.append(image.resize((new_width, max_height), Image.Resampling.LANCZOS))
        return resized_images

    def to_image(
        self,
        x: str | None = None,
        y: str | None = None,
    ) -> Image.Image:
        """Show images in the ImageBoard in a grid or row/column if only one dimension is provided."""
        if not x and not y:
            msg = "Please provide x or y keys for metadata to display."
            raise ValueError(msg)

        # Filter images containing the key x or y
        filtered_data = [
            (record.metadata, record.img)
            for record in self.data
            if (x and x in record.metadata) or (y and y in record.metadata)
        ]

        # 根据 metadata x 和 y 的值，确定每个图片的key。然后，如果key 有重复，则只选用第一个，并弹出警告
        unique_data = []
        seen_keys = set()
        for record in filtered_data:
            key = (record[0].get(x), record[0].get(y))
            if key in seen_keys:
                logger.warning("Duplicate key found: %s", record[0])
            else:
                seen_keys.add(key)
                unique_data.append(record)
        filtered_data = unique_data

        if not filtered_data:
            msg = "No images found with the provided metadata keys."
            raise ValueError(msg)

        # Extract images and calculate max height
        images = [img_data[1] for img_data in filtered_data]
        max_height = self._calculate_max_image_height(images)

        # Resize images to max height
        resized_images = self._resize_images_to_max_height(images, max_height)

        x_count, _ = self._get_axes_count(x, y, filtered_data)
        resized_images_2d = [resized_images[i : i + x_count] for i in range(0, len(resized_images), x_count)]
        metadata_2d = [filtered_data[i : i + x_count] for i in range(0, len(filtered_data), x_count)]
        if x and y:
            label_2d = [[f"{record[0][x]}, {record[0][y]}" for record in row] for row in metadata_2d]
        elif x:
            label_2d = [[f"{record[0][x]}" for record in row] for row in metadata_2d]
        else:
            label_2d = [[f"{record[0][y]}" for record in row] for row in metadata_2d]
        return ImageGrid(resized_images_2d, labels=label_2d).to_image()

    def _calculate_max_image_size(self, filtered_data: list[tuple[dict, Image.Image]]) -> tuple[int, int]:
        max_width = 0
        max_height = 0
        for img in filtered_data:
            max_width = max(max_width, img[1].size[0])
            max_height = max(max_height, img[1].size[1])
        return max_width, max_height

    def _get_axes_count(
        self,
        x: str | None,
        y: str | None,
        filtered_data: list[tuple[dict, Image.Image]],
    ) -> tuple[int, int]:
        """Get the number of axes for the grid."""
        if x and y:
            # Extract x and y values from metadata
            y_values = sorted({record[0][x] for record in filtered_data})
            x_values = sorted({record[0][y] for record in filtered_data})

            y_count = len(y_values)
            x_count = len(x_values)
        elif x:
            x_values = sorted({record[0][x] for record in filtered_data})
            x_count = len(x_values)
            y_count = 1
        else:
            y_values = sorted({record[0][y] for record in filtered_data})
            x_count = 1
            y_count = len(y_values)
        return x_count, y_count

    def _adjust_canvas_size(self, mode: str, max_a: int, canvas_h: float, canvas_w: float) -> tuple[float, float]:
        """Adjust the canvas size if it exceeds the maximum size."""
        aspect_ratio = canvas_w / canvas_h
        if mode == "show" and (canvas_h > max_a or canvas_w > max_a):
            if canvas_h > canvas_w:
                canvas_h = max_a
                canvas_w = max_a / aspect_ratio
            else:
                canvas_w = max_a
                canvas_h = max_a * aspect_ratio
        return canvas_h, canvas_w

    def show(
        self,
        x: str | None = None,
        y: str | None = None,
    ) -> None:
        """Show the ImageBoard in a grid."""
        self.to_image(x, y).show()

    def save(
        self,
        path: Path | str,
        x: str | None = None,
        y: str | None = None,
    ) -> None:
        """Save the ImageBoard to a file."""
        self.to_image(x, y).save(path)


if __name__ == "__main__":

    def get_random_image_from_splash(width: int, height: int) -> Image.Image:
        """Generate an image with random background and centered text with specified dimensions."""
        import secrets

        from PIL import Image, ImageDraw, ImageFont

        img = Image.new(
            "RGB",
            (width, height),
            (secrets.randbelow(256), secrets.randbelow(256), secrets.randbelow(256)),
        )

        draw = ImageDraw.Draw(img)
        text = f"{width}x{height}"
        font_size = 40

        # Ensure 'arial.ttf' is available or replace with a path to a different font file
        font = ImageFont.truetype("arial.ttf", font_size)

        # Calculate the text bounding box to find its size
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Calculate position for centered text
        text_x = (width - text_width) / 2
        text_y = (height - text_height) / 2

        draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))
        return img

    ib = ImageBoard()
    for a in [1, 2]:
        for b in [3, 2, 1]:
            img = get_random_image_from_splash(256 * b, 512)
            ib.append(img, {"a": a, "b": b})
    ib.to_image(x="b").show()
