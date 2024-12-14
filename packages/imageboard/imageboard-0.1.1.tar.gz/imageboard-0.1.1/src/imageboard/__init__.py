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

    def _set_fig(
        self,
        x: str | None = None,
        y: str | None = None,
        width: float | None = None,
        height: float | None = None,
        mode: Literal["save", "show"] = "show",
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

        img_width, img_height = filtered_data[0][1].size
        img_width_inches = img_width / dpi
        img_height_inches = img_height / dpi

        if x and y:
            # Extract x and y values from metadata
            x_values = sorted({record[0][x] for record in filtered_data})
            y_values = sorted({record[0][y] for record in filtered_data})

            x_count = len(x_values)
            y_count = len(y_values)
        elif x:
            y_values = sorted({record[0][x] for record in filtered_data})
            y_count = len(y_values)
            x_count = 1
        else:
            x_values = sorted({record[0][y] for record in filtered_data})
            y_count = 1
            x_count = len(x_values)

        width = width if width else img_width_inches * x_count
        height = height if height else img_height_inches * y_count

        fig = plt.figure(figsize=(height, width), dpi=dpi)

        grid = ImageGrid(
            fig,
            (0, 0, 1, 1),
            nrows_ncols=(x_count, y_count),
            axes_pad=0,
        )

        for ax, img in zip(grid, ib.data, strict=False):  # type: ignore
            ax.imshow(img.img)
            left_bottom_label = f"{x}: {img.metadata[x]}\n{y}: {img.metadata[y]}"
            text = ax.text(
                0,
                0,
                left_bottom_label,
                fontsize="large" if mode == "show" else (img_height * 0.04),
                color="white",
                ha="left",
                va="bottom",
                transform=ax.transAxes,
            )
            # font weight
            text.set_fontweight("bold")
            # text border
            text.set_path_effects(
                [
                    matplotlib.patheffects.Stroke(
                        linewidth=2 if mode == "show" else (img_height * 0.005),
                        foreground="black",
                    ),
                    matplotlib.patheffects.Normal(),
                ],
            )

            ax.axis("off")

    def show(self, x: str | None = None, y: str | None = None, width: int = 8, height: int = 8) -> None:
        """Show the ImageBoard in a grid."""
        self._set_fig(x, y, width, height)
        plt.show()

    def save(
        self,
        path: Path | str,
        x: str | None = None,
        y: str | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> None:
        """Save the ImageBoard to a file."""
        self._set_fig(x, y, width, height, mode="save")
        plt.savefig(path)


if __name__ == "__main__":

    def get_random_image_from_splash() -> Image.Image:
        """Get a random image from the Unsplash API."""
        import secrets

        from PIL import Image

        return Image.new("RGB", (512, 512), (secrets.randbelow(256), secrets.randbelow(256), secrets.randbelow(256)))

    ib = ImageBoard()
    for a in ["foo", "bar"]:
        for b in ["baz", "qux", "quux"]:
            img = get_random_image_from_splash()
            ib.append(img, {"a": a, "b": b})

    ib.show(x="a", y="b")
    ib.save("imageboard.png", x="a", y="b")
