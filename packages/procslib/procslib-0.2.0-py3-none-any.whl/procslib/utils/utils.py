import os

import pandas as pd
import unibox as ub
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms


class ImageDataset(Dataset):
    def __init__(self, image_files, img_size):
        self.image_files = image_files
        self.img_size = img_size
        self.transform = transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Resize((self.img_size, self.img_size), antialias=True),
                transforms.CenterCrop(self.img_size),
            ],
        )

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        image_path = self.image_files[idx]
        try:
            image = Image.open(image_path).convert("RGB")
            image = self.transform(image)
            return image, image_path
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None  # Return None for corrupted images


def list_images_as_dataframe(image_root_dir: str):
    """List all image files in a directory and return them as a DataFrame.

    Args:
        image_root_dir (str): Path to the root directory containing image files.

    Returns:
        pd.DataFrame: DataFrame with columns `local_path` and `filename`.
    """
    image_files = ub.traverses(image_root_dir, ub.IMG_FILES)
    print(f"{len(image_files)} images found in {image_root_dir} | preview: {image_files[:5]}")

    image_df = pd.DataFrame(image_files, columns=["local_path"])
    image_df["filename"] = image_df["local_path"].apply(lambda x: os.path.basename(x))
    return image_df


def split_dataframe_into_chunks(df: pd.DataFrame, save_directory: str, num_chunks: int = 8):
    """把一个df分成num_chunks份, 保存到save_directory下, 命名为{idx}.parquet"""
    # Split DataFrame into chunks
    data_chunks = [df.iloc[i::num_chunks] for i in range(num_chunks)]

    # Ensure the split covers all rows
    assert sum(len(chunk) for chunk in data_chunks) == len(df)

    # Save chunks to disk
    os.makedirs(save_directory, exist_ok=True)
    for idx, chunk in enumerate(data_chunks):
        chunk_path = os.path.join(save_directory, f"{idx}.parquet")
        ub.saves(chunk, chunk_path)
        # print(f"Chunk {idx} saved to {chunk_path}")


def list_image_dirs_to_chunks(image_root_dirs: list[str], save_directory: str, num_chunks=8):
    """Process a list of image directories by listing images, converting to DataFrame,
    splitting into chunks, and saving to disk. Also saves a configuration file.

    Args:
        image_root_dirs (list of str): List of paths to root directories containing image files.
        save_directory (str): Directory to save the resulting chunks.
        num_chunks (int): Number of chunks to split the DataFrame into.

    Returns:
        None
    """
    print(f"Processing image directories: {image_root_dirs} -> {save_directory} ({num_chunks} chunks)")

    combined_df = pd.DataFrame()
    for image_root_dir in image_root_dirs:
        image_df = list_images_as_dataframe(image_root_dir)
        combined_df = pd.concat([combined_df, image_df], ignore_index=True)

    print(f"Combined DataFrame preview: {ub.peeks(combined_df)}")
    split_dataframe_into_chunks(combined_df, save_directory, num_chunks=num_chunks)

    # Save configuration info
    chunking_info_path = os.path.join(save_directory, "CHUNKING_INFO.txt")
    with open(chunking_info_path, "w") as f:
        f.write(f"Image root directories: {image_root_dirs}\n")
        f.write(f"Save directory: {save_directory}\n")
        f.write(f"Number of chunks: {num_chunks}\n")
        f.write(f"Total images: {len(combined_df)}\n")
        f.write(f"Date: {pd.Timestamp.now()}\n")
    print(f"Chunking configuration saved to {chunking_info_path}")
