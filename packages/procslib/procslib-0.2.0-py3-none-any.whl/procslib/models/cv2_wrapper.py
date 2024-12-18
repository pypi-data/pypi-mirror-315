# src/procslib/models/opencv_metrics_inference.py
import glob

import numpy as np
import pandas as pd
from PIL import Image
from torch.utils.data import DataLoader
from tqdm.auto import tqdm

from .base_inference import BaseImageInference, ImagePathDataset, custom_collate


def calculate_brightness_contrast(image: np.ndarray):
    # brightness = mean pixel value
    brightness = np.mean(image)
    # contrast = std deviation of pixel values
    contrast = np.std(image)
    return brightness, contrast


class OpenCVMetricsInference(BaseImageInference):
    """A class to calculate simple image metrics (brightness, contrast, etc.)
    using OpenCV or NumPy.
    """

    def __init__(self, device="cpu", batch_size=32):
        # device is mostly irrelevant here since no GPU ops
        super().__init__(device=device, batch_size=batch_size)

    def _load_model(self, checkpoint_path: str = None):
        # No model to load
        pass

    def _preprocess_image(self, pil_image: Image.Image):
        # Convert PIL to OpenCV format
        # Note: PIL is RGB, OpenCV expects BGR, but for brightness/contrast doesn't matter
        np_image = np.array(pil_image.convert("RGB"))
        return np_image  # Just return the raw array

    def _postprocess_output(self, metrics):
        # metrics is a dict of results
        return metrics

    def infer_one(self, pil_image: Image.Image):
        np_image = self._preprocess_image(pil_image)
        brightness, contrast = calculate_brightness_contrast(np_image)
        return {"brightness": brightness, "contrast": contrast}

    def infer_batch(self, pil_images: list[Image.Image]):
        results = []
        for img in pil_images:
            np_image = self._preprocess_image(img)
            brightness, contrast = calculate_brightness_contrast(np_image)
            results.append({"brightness": brightness, "contrast": contrast})
        return results

    def infer_many(self, image_paths: list[str]):
        dataset = ImagePathDataset(image_paths, preprocess_fn=self._preprocess_image)
        dataloader = DataLoader(
            dataset,
            batch_size=self.batch_size,
            num_workers=0,  # CPU ops are cheap and no need to decode PIL in multiple workers
            pin_memory=False,
            collate_fn=custom_collate,
        )

        results = []
        for batch in tqdm(dataloader, desc="Calculating OpenCV metrics"):
            if batch is None:
                continue
            np_images, paths = batch
            # np_images is a batch of numpy arrays converted to tensors. We must convert back to np arrays.
            # Actually, due to how ImagePathDataset and custom_collate might work, ensure that preprocessed
            # images are arrays. If they are arrays, they might be stacked into a torch tensor automatically.
            # If so, convert back to numpy:
            if isinstance(np_images, torch.Tensor):
                np_images = np_images.cpu().numpy()

            # If shape is [B, H, W, C], we can iterate
            for np_image, path in zip(np_images, paths):
                brightness, contrast = calculate_brightness_contrast(np_image)
                results.append({"filename": path, "brightness": brightness, "contrast": contrast})

        return pd.DataFrame(results)


# Demo usage
def demo_cv2_wrapper():
    folder_to_infer = "/rmt/image_data/dataset-ingested/gallery-dl/twitter/___Jenil"
    image_paths = glob.glob(folder_to_infer + "/*.jpg")
    inference = OpenCVMetricsInference(batch_size=2)

    # Single image
    img = Image.open(image_paths[0])
    print("Single image metrics:", inference.infer_one(img))

    # Batch
    imgs = [Image.open(p) for p in image_paths]
    print("Batch metrics:", inference.infer_batch(imgs))

    # Many images
    df = inference.infer_many(image_paths)
    df.to_csv("cv2_scores.csv", index=False)
    print("Inference completed. Results saved to 'cv2_scores.csv'.")


if __name__ == "__main__":
    demo_cv2_wrapper()
