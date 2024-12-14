# --------------------------------------
import os

# --------------------------------------
import json

# --------------------------------------
import time

# --------------------------------------
import random

# --------------------------------------
from pathlib import Path

# --------------------------------------
from functools import reduce

# --------------------------------------
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

# --------------------------------------
from tqdm import tqdm

# --------------------------------------
import pandas as pd

# --------------------------------------
import requests as rq

# --------------------------------------
from streetscapes import conf
from streetscapes import types as sst
from streetscapes.conf import logger

def mkdir(directory: Path | str) -> Path:
    """
    Resolve and expand a directory path and
    create the directory if it doesn't exist.

    Args:
        directory (Path):
            A directory path.

    Returns:
        Path:
            The expanded path.
    """

    directory = Path(directory).expanduser().resolve().absolute()
    directory.mkdir(exist_ok=True, parents=True)
    return directory


def convert_csv_to_parquet(
    data_dir: Path | str = conf.DATA_DIR,
    out_dir: Path | str = conf.OUTPUT_DIR,
    filename: str = "streetscapes-data.parquet",
    silent: bool = False,
):
    """
    Converts a list of global-streetscapes csv files into a single merged dataframe.

    Constructs a pd.DataFrame resulting from merging all csvs on the
    columns "uuid", "source", and "orig_id" using a left join.

    Args:
        data_dir (Path, optional):
            The data directory containing the CSV files.
            Defaults to conf.DATA_DIR.

        out_dir (Path, optional):
            The destinatoin directory for the Parquet file.
            Defaults to conf.OUTPUT_DIR.

        filename (str, optional):
            The name of the Parquet file.
            Defaults to "streetscapes-data.parquet".

        silent (bool, optional):
            Do not prompt the user if the destination file exists.
            Defaults to False.

    Raises:
        FileNotFoundError:
            Error if the data directory does not exist.
    """

    data_dir = Path(data_dir)
    out_dir = Path(out_dir)

    if not data_dir.exists():
        raise FileNotFoundError(f"The specified directory '{data_dir}' does not exist.")

    out_dir.mkdir(exist_ok=True, parents=True)

    parquet_file = out_dir / filename

    if parquet_file.exists() and not silent:
        ok = input("==[ The target filename exists. Overwrite? (y/[n]) ")
        if not ok.lower().startswith("y"):
            logger.info(f"Exiting.")
            return

    csv_files = data_dir.glob("*.csv")

    csv_dfs = []
    dtypes = {
        "sequence_id": str,
        "capital": str,
        "pano_status": str,
        "view_direction": str,
    }
    for file in csv_files:
        logger.info(f"Processing file '{file.name}'...")
        df = pd.read_csv(file, dtype=dtypes)
        df["orig_id"] = df["orig_id"].astype("int64")
        csv_dfs.append(df)

    logger.info(f"Merging files...")
    merged_df = reduce(
        lambda left, right: pd.merge(
            left, right, on=["uuid", "source", "orig_id"], how="left"
        ),
        csv_dfs,
    )

    logger.info(f"Saving file '{parquet_file.name}'...")
    merged_df.to_parquet(parquet_file, compression="gzip")


def load_city_subset(
    city: str = None,
    directory: str | Path = conf.OUTPUT_DIR,
    recreate: bool = False,
) -> pd.DataFrame | None:
    """
    Load and return a Parquet file for a specific city, if it exists.

    Args:
        city (str, optional):
            The city name. Defaults to None.

        directory (str | Path, optional):
            Directory to look into for the file.
            Defaults to conf.OUTPUT_DIR.

        recreate (bool, optional):
            Recreate the city subset if it exists.
            Defaults to False.

    Returns:
        pd.DataFrame | None:
            The Pandas dataframe with data for the requested city, if it exists.
    """

    directory = Path(directory)

    if city is None:
        filename = "streetscapes-data.parquet"
    else:
        filename = f"{city}.parquet"

    fpath = directory / filename
    if not fpath.exists() or (fpath.exists() and recreate):
        logger.info(f"Creating subset for '{city}'...")
        df_all = pd.read_parquet(conf.OUTPUT_DIR / "streetscapes-data.parquet")
        df_city = df_all[df_all["city"] == city]
        df_city.to_parquet(fpath)

    logger.info(f"Loading '{fpath.name}'...")
    return pd.read_parquet(fpath)


def get_missing_image_ids(
    records: pd.DataFrame,
    directory: Path,
    image_paths: set[Path] = None,
) -> tuple[set[Path], set[int]]:
    """
    Extract the set of IDs for images that have not been downloaded yet.

    Args:
        records (pd.DataFrame):
            A Pandas dataframe containing image ID information.

        directory (Path):
            The directory to search.

        image_paths (set[Path], optional):
            A set of paths that has already been collected. Defaults to None.

    Returns:
        tuple[set[Path], set[int]]:
            A tuple containing:
                1. A set of paths to existing images.
                2. A set of image IDs to download.
    """

    if image_paths is None:
        image_paths = set()
    missing = set()
    for record in records:
        image_id = record["orig_id"]
        image_path = directory / f"{image_id}.jpeg"
        if image_path.exists():
            image_paths.add(image_path)
        else:
            missing.add(image_id)

    return (image_paths, missing)


def get_image_url(
    image_id: int,
    source: sst.SourceMap,
    resolution: int = 2048,
    session: rq.Session = None,
) -> str:
    """
    Retrieve the URL for an image with the given ID.

    Args:
        source (sst.Source):
            The source map (cf. the SourceMap enum).

        image_id (int):
            The image ID.

        resolution (int):
            The resolution of the requested image (only valid for Mapillary for now).

        session (rq.Session, optional):
            An optional authenticated session to use
            for retrieving the image.

    Returns:
        str:
            The URL to query.
    """

    match source:
        case sst.SourceMap.Mapillary:
            url = (
                f"https://graph.mapillary.com/{image_id}?fields=thumb_{resolution}_url"
            )

            try:
                prq = rq.Request(
                    "GET", url, params={"access_token": conf.MAPILLARY_TOKEN}
                )
                res = session.send(prq.prepare())
                image_url = json.loads(res.content.decode("utf-8"))[
                    f"thumb_{resolution}_url"
                ]

                return image_url

            except Exception as e:
                return

        case sst.SourceMap.KartaView:
            url = f"https://api.openstreetcam.org/2.0/photo/?id={image_id}"
            try:
                # Send the request
                r = rq.get(url)
                # Parse the response
                data = r.json()["result"]["data"][0]
                image_url = data["fileurlProc"]
                return image_url
            except Exception as e:
                return

        case _:
            return


def download_image(
    image_id: int,
    directory: str | Path,
    source: sst.SourceMap,
    resolution: int = 2048,
    verbose: bool = True,
    session: rq.Session = None,
) -> Path:
    """
    Download a single image from Mapillary.

    Args:
        image_id (str):
            The image ID.

        directory (str | Path):
            The destination directory.

        source (sst.SourceMap):
            The source map.
            Limited to Mapillary or KartaView at the moment.

        resolution (int, optional):
            The resolution to request. Defaults to 2048.

        verbose (bool, optional):
            Print some output. Defaults to True.

        session (rq.Session, optional):
            An optional authenticated session to use
            for retrieving the image.

    Returns:
        Path:
            The path to the downloaded image file.
    """

    # Set up the image path
    image_path = directory / f"{image_id}.jpeg"

    # Download the image
    if not image_path.exists():

        if verbose:
            logger.info(f"Downloading image {image_id}.jpeg...")

        # Random sleep time so that we don't flood the servers.
        time.sleep(random.uniform(0.1, 1))

        # NOTE: Specifically in the case of Mapillary,
        # we have to send a request for that image
        # straight after getting the URL.
        # Collecting all the URLs in advance and requesting them
        # one by one outside the loop doesn't work.

        # Download the image
        # ==================================================
        match source:
            case sst.SourceMap.Mapillary:
                if session is None:
                    session = get_session(source)
                url = get_image_url(image_id, source, resolution, session)
                response = session.get(url)
            case sst.SourceMap.KartaView:
                url = get_image_url(image_id, source, resolution)
                response = rq.get(url)

        # Save the image if it has been downloaded successfully
        # ==================================================
        if response.status_code == 200 and response.content is not None:
            with open(image_path, "wb") as f:
                f.write(response.content)

    return image_path


def get_session(source: sst.SourceMap):
    """
    Get an authenticated session for the supplied source.

    Right now, we only need a session for working with Mapillary.

    Args:
        source (sst.SourceMap):
            A `requests` session.
    """

    match source:
        case sst.SourceMap.Mapillary:
            session = rq.Session()
            session.headers.update({"Authorization": f"OAuth {conf.MAPILLARY_TOKEN}"})
            return session

        case _:
            return


def download_images(
    df: pd.DataFrame,
    directory: str | Path,
    resolution: int = 2048,
    sample: bool = False,
    max_workers: int = None,
    verbose: bool = False,
) -> list[Path]:
    """
    Download a set of images concurrently.

    Args:
        df (pd.DataFrame):
            A dataframe containing image IDs.

        directory (str | Path):
            The destination directory.

        resolution (int, optional):
            The resolution to request. Defaults to 2048.

        sample (int, optional):
            Only download a sample set of images. Defaults to None.

        max_workers (int, optional):
            The number of workers (threads) to use. Defaults to None.

        verbose (bool, optional):
            Print some output. Defaults to False.

    Returns:
        list[Path]:
            A list of image paths.
    """

    # Filter records by source
    filtered = {}
    for source in sst.SourceMap:
        subset = df[df["source"].str.lower() == source.name.lower()]
        if len(subset) > 0:
            filtered[source] = subset

    # Set up the image directory
    directory = mkdir(directory)

    image_paths = set()
    for source, records in filtered.items():

        # Limit the records if only a sample is required
        if sample is not None:
            records = records[:sample]

        # Convert records to a dictionary
        records = records.to_dict("records")

        # Get the IDs of images that haven't been downloaded yet.
        (image_paths, missing) = get_missing_image_ids(records, directory, image_paths)

        # Download the images in parallel
        # ==================================================
        if len(missing) > 0:

            # Authenticated session for this source (if necessary)
            session = get_session(source)

            if max_workers is None:
                max_workers = os.cpu_count()
            with ThreadPoolExecutor(max_workers=max_workers) as tpe:

                logger.info(
                    f"Downloading {len(missing)} images from {source.name} into '{directory.name}'..."
                )

                # Submit the image IDs for processing
                futures = {
                    tpe.submit(
                        download_image,
                        image_id,
                        directory,
                        source,
                        resolution,
                        verbose,
                        session,
                    ): image_id
                    for image_id in missing
                }

                with tqdm(total=len(missing), desc="Download progress: ") as pbar:
                    for future in as_completed(futures):
                        try:
                            image_id = futures[future]
                            image_paths.add(future.result())
                            if verbose:
                                logger.info(f"Image {image_id} downloaded successuflly")
                        except Exception as exc:
                            logger.debug(f"Error downloading image {image_id}")
                        pbar.update(1)

    return image_paths
