from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class RandomCrop:
    output_size: tuple[int, int]

    def __call__(self, image: np.ndarray) -> np.ndarray:
        h, w = image.shape[:2]
        nh, nw = self.output_size
        top = np.random.randint(0, h - nh + 1)
        left = np.random.randint(0, w - nw + 1)
        return image[top : top + nh, left : left + nw]


class RandomHorizontalFlip:
    def __init__(self, p: float = 0.5) -> None:
        self.p = p

    def __call__(self, image: np.ndarray) -> np.ndarray:
        if np.random.rand() < self.p:
            return np.fliplr(image)
        return image


class AddGaussianNoise:
    def __init__(self, sigma: float = 0.05) -> None:
        self.sigma = sigma

    def __call__(self, image: np.ndarray) -> np.ndarray:
        return image + np.random.normal(0, self.sigma, size=image.shape).astype(image.dtype)


class Compose:
    def __init__(self, transforms: list) -> None:
        self.transforms = transforms

    def __call__(self, image: np.ndarray) -> np.ndarray:
        out = image
        for t in self.transforms:
            out = t(out)
        return out
