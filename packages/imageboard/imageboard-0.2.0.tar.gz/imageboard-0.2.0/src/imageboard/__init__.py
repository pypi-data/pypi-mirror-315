"""ImageBoard is a class for displaying images with metadata in a grid."""

import logging
import os
from pathlib import Path
from typing import IO, Literal

import matplotlib.patheffects
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from PIL import Image
from pydantic import BaseModel

logger = logging.getLogger("imageboard")


class ImgRecord(BaseModel):
    """ImgRecord is a Pydantic model for an image with metadata."""

    img: Image.Image
    metadata: dict

    class Config:
        """Pydantic configuration for ImgRecord."""

        arbitrary_types_allowed = True


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

    def _set_fig(
        self,
        x: str | None = None,
        y: str | None = None,
        mode: Literal["save", "show"] = "save",
    ) -> None:
        """Show images in the ImageBoard in a grid or row/column if only one dimension is provided."""
        dpi = 100

        if not x and not y:
            logger.warning("Please provide x or y keys for metadata to display.")
            return

        # Filter images containing the key x or y
        filtered_data = [
            (record.metadata, record.img)
            for record in self.data
            if (x and x in record.metadata) or (y and y in record.metadata)
        ]

        if not filtered_data:
            logger.warning("No images found with the provided x or y keys.")
            return

        # Extract images and calculate max height
        images = [img_data[1] for img_data in filtered_data]
        max_height = self._calculate_max_image_height(images)

        # Resize images to max height
        resized_images = self._resize_images_to_max_height(images, max_height)

        x_count, y_count = self._get_axes_count(x, y, filtered_data)

        resized_images_2d = [resized_images[i : i + x_count] for i in range(0, len(resized_images), x_count)]

        max_x_width = 0
        max_y_height = 0
        for row in resized_images_2d:
            for col in row:
                max_x_width = max(max_x_width, col.size[0])
                max_y_height = max(max_y_height, col.size[1])

        canvas_h = max_y_height / dpi
        canvas_w = max_x_width / dpi
        fig = plt.figure(figsize=(canvas_w, canvas_h), dpi=dpi)
        grid = ImageGrid(
            fig,
            (0, 0, 1, 1),
            nrows_ncols=(y_count, x_count),
            axes_pad=0,
        )
        row_height = canvas_h / y_count
        for ax, (img_data, resized_img) in zip(grid, zip(filtered_data, resized_images, strict=False), strict=False):  # type: ignore
            ax.imshow(resized_img)
            if x and y:
                x_val = img_data[0][x]
                y_val = img_data[0][y]
                left_bottom_label = f"{x}: {x_val}\n{y}: {y_val}"
            elif x:
                x_val = img_data[0][x]
                left_bottom_label = f"{x_val}"
            else:
                y_val = img_data[0][y]
                left_bottom_label = f"{y_val}"
            text = ax.text(
                0,
                0,
                left_bottom_label,
                fontsize="large" if mode == "show" else (row_height * 0.03 * dpi),
                color="white",
                ha="left",
                va="bottom",
                transform=ax.transAxes,
            )
            text.set_fontweight("bold")
            text.set_path_effects(
                [
                    matplotlib.patheffects.Stroke(
                        linewidth=2 if mode == "show" else (row_height * 0.005 * dpi),
                        foreground="black",
                    ),
                    matplotlib.patheffects.Normal(),
                ],
            )
            ax.axis("off")

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
        self._set_fig(x, y, mode="show")
        plt.show()

    def save(
        self,
        path: Path | str,
        x: str | None = None,
        y: str | None = None,
    ) -> None:
        """Save the ImageBoard to a file."""
        self._set_fig(x, y)
        plt.savefig(path)

    def to_image(self, x: str | None = None, y: str | None = None) -> Image.Image:
        """Convert the ImageBoard to a PIL Image."""
        self._set_fig(x, y)
        fig = plt.gcf()
        fig.canvas.draw()
        return Image.frombytes("RGBA", fig.canvas.get_width_height(), fig.canvas.buffer_rgba())  # type: ignore


if __name__ == "__main__":

    def get_random_image_from_splash(width: int, height: int) -> Image.Image:
        """Get a random image from the Unsplash API."""
        import secrets

        from PIL import Image

        return Image.new(
            "RGB",
            (width, height),
            (secrets.randbelow(256), secrets.randbelow(256), secrets.randbelow(256)),
        )

    ib = ImageBoard()
    for a in [1, 2]:
        for b in [3, 2, 1]:
            img = get_random_image_from_splash(256 * b, 512)
            ib.append(img, {"a": a, "b": b})
    ib.to_image(x="a", y="b").show()
