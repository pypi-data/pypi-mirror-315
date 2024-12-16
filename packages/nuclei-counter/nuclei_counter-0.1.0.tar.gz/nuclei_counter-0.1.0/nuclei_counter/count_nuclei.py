import argparse
import multiprocessing
import os
from pathlib import Path
import pandas as pd

from nuclei_counter.counter import count_objects

from tqdm.contrib.concurrent import process_map


if __name__ == "__main__":
    multiprocessing.freeze_support()

    parser = argparse.ArgumentParser(description="Process and count nuclei in images.")
    parser.add_argument(
        "--img_dir",
        help="Path to the directory containing images.",
    )

    parser.add_argument(
        "--output_dir",
        default=Path(os.getcwd()) / "results",
        help="Save directory for results files.",
    )

    parser.add_argument(
        "--save_images",
        action="store_true",
        help="Include this flag to save transformed images used for counting.",
    )

    parser.add_argument(
        "--output_count_filename",
        default="count_results.csv",
        help="Output file name of the resulting CSV. Defaults to count_results.csv",
    )

    args = parser.parse_args()

    img_dir = Path(args.img_dir)
    output_file_name = args.output_count_filename
    save_path = Path(args.output_dir)
    save_images = args.save_images

    file_names = os.listdir(img_dir)
    os.makedirs(save_path, exist_ok=True)

    args_list = [(f, img_dir, save_path, save_images) for f in file_names]
    num_cores = multiprocessing.cpu_count()
    # when running as a windows executable, the process often breaks and throws a broken process pool error.
    # Adding in a chunksize >1 seems to help.

    results = process_map(count_objects, args_list, max_workers=num_cores, chunksize=10)

    # with Pool(processes=num_cores) as pool:
    #     results = list(
    #         tqdm(pool.imap(count_objects_wrapper, args_list), total=len(file_names))
    #     )

    df = pd.DataFrame([result for result in results if result is not None])
    df.to_csv(save_path / output_file_name, index=False)
