import os
import re
import requests
import argparse
import logging
import json
from time import sleep

# logs
logging.basicConfig(
    filename="file_rename.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# season+episode syntax; likely show name match
season_episode_pattern = re.compile(r"(S\d{2}E\d{2})")
show_name_pattern = re.compile(r"(.+?)(?:\s*[_.-]*)S\d{2}E\d{2}")

# cache API results;
api_cache = {}

def sanitize_filename(filename):
    # nix unsupported characters, clean up spaces
    sanitized = filename.replace(":", " - ").replace('"', "''").replace("?", "")
    while "  " in sanitized:
        sanitized = sanitized.replace("  ", " ")
    return sanitized.strip()

def get_episode_metadata(show_name, season, episode):
    # more cache to avoid duplicate API requests
    cache_key = f"{show_name}_S{season}E{episode}"
    if cache_key in api_cache:
        return api_cache[cache_key]

    try:
        # query api.tvmaze.com for episode information ### ADD BACKUP API OPTIONS IN FUTURE ###
        url = f"https://api.tvmaze.com/singlesearch/shows?q={show_name}&embed=episodes"
        response = requests.get(url)
        response.raise_for_status()
        show_data = response.json()
        for ep in show_data["_embedded"]["episodes"]:
            if ep["season"] == int(season) and ep["number"] == int(episode):
                metadata = (ep["name"], ep["airdate"], ep["runtime"])
                api_cache[cache_key] = metadata
                return metadata
    except Exception as e:
        logging.error(f"Error fetching episode metadata: {e}") # this can be made much better
    return None, None, None

def write_backup_file(folder_path, backup_data):
    backup_file_path = os.path.join(folder_path, "rename_backup.json")
    try:
        with open(backup_file_path, "w") as backup_file:
            json.dump(backup_data, backup_file, indent=4)
        logging.info(f"Backup file created: {backup_file_path}")
    except Exception as e:
        logging.error(f"Error writing backup file: {e}")

def rename_files(folder_path, show_name, output_format, dry_run):
    parent_dir_name = os.path.basename(os.path.dirname(folder_path))
    backup_data = {}  # dict; store original, renamed filenames

    for file_name in os.listdir(folder_path):
        # gloss over directories, process only files
        if not os.path.isfile(os.path.join(folder_path, file_name)):
            continue

        # look for season+episode syntax. 
        # will always work for S01E02-type naming.
        season_episode_match = season_episode_pattern.search(file_name)
        if season_episode_match:
            season_episode = season_episode_match.group(1)
            season = season_episode[1:3]
            episode = season_episode[4:6]

            # detects showname from filename OR fallback to parent directory
            show_name_match = show_name_pattern.search(file_name)
            detected_show_name = show_name_match.group(1).strip() if show_name_match else show_name or parent_dir_name

            # get episode metadata
            episode_name, air_date, runtime = get_episode_metadata(detected_show_name, season, episode)
            if not episode_name:
                episode_name = "[Unknown Episode]"
                logging.warning(f"Episode name not found for {file_name}. Using placeholder.")

            # ...format output filename
            file_ext = os.path.splitext(file_name)[1]
            formatted_name = output_format.format(
                season_episode=season_episode,
                episode_name=episode_name,
                air_date=air_date or "Unknown Date",
                runtime=f"{runtime} min" if runtime else "Unknown Runtime",
            )
            sanitized_file_name = sanitize_filename(f"{formatted_name}{file_ext}")

            # dry-run or rename files. Stable, but prior iterations are why write_backup_file exists
            if dry_run:
                print(f"[Dry-Run] Would rename: {file_name} -> {sanitized_file_name}")
                logging.info(f"[Dry-Run] Would rename: {file_name} -> {sanitized_file_name}")
            else:
                try:
                    os.rename(
                        os.path.join(folder_path, file_name),
                        os.path.join(folder_path, sanitized_file_name),
                    )
                    backup_data[file_name] = sanitized_file_name  # Record the change
                    logging.info(f"Renamed: {file_name} -> {sanitized_file_name}")
                    print(f"Renamed: {file_name} -> {sanitized_file_name}")
                except Exception as e:
                    logging.error(f"Error renaming file {file_name}: {e}")
                    print(f"Error renaming {file_name}: {e}")

    # write backup data to file
    if not dry_run:
        write_backup_file(folder_path, backup_data)

def process_subfolders(base_path, show_name, output_format, dry_run):
    # iterate over all (should be n) subdirectories in the base (should be parent) folder
    for subfolder in os.listdir(base_path):
        subfolder_path = os.path.join(base_path, subfolder)
        if os.path.isdir(subfolder_path):
            print(f"Processing subfolder: {subfolder_path}")
            logging.info(f"Processing subfolder: {subfolder_path}")
            rename_files(subfolder_path, show_name, output_format, dry_run)

def main():
    # set up argparse
    parser = argparse.ArgumentParser(description="Rename files based on season/episode syntax.")
    parser.add_argument("--i", action="store_true", help="Prompt for input directory instead of using default.")
    parser.add_argument("--show", type=str, help="Specify the show name explicitly.")
    parser.add_argument("--format", type=str, default="{season_episode} - {episode_name}", 
                        help="Customize output format using placeholders.")
    parser.add_argument("--dry", action="store_true", help="Preview changes without renaming files.")
    args = parser.parse_args()

    # determine folder path
    if args.i:
        base_path = input("Enter the base directory path: ").strip()
        if not os.path.isdir(base_path):
            print("Invalid directory. Please try again.")
            logging.error(f"Invalid directory entered: {base_path}")
            return
    else:
        base_path = os.getcwd()  # Default to current working directory

    print(f"Running in base directory: {base_path}")
    logging.info(f"Starting renaming process in base directory: {base_path}")

    # process subfolders
    process_subfolders(base_path, args.show, args.format, args.dry)

if __name__ == "__main__":
    main()
