This script queries TVMaze's API and auto-renames supported files, helping you structure media files in a human-readable format. It'll automatically retrieve accurate episode information and can effortlessly process multiple subdirectories. 

It'll also create a backup file for cowards.

Files containing information like _"S01E01"_ 

**or named things like:** 
_"Showname.S01E01.Uploader.Group.Site.mp4"
"Showname.S01E01.Episodename.Site.mp4"_

**Become:**

"S01E01 - The Beginning.mp4" and 
"S02E02 - Two's a Crowd.mp4", respectively.

It can be ran from a parent directory, ShowName, containing folders for Seasons 1-10. 
From here, it'll process subfolders automatically. If none are present, it'll process _only the files in its base folder._

**Features**

   * Metadata Retrieval: Automatically fetches episode titles, air dates, and runtimes from the TVmaze API.
   * Filename Sanitization: Replaces unsupported characters like :, ", ?, etc., to create Windows-compatible filenames.
   * Recursive Processing: Processes all subdirectories (e.g., for each season) in the base directory automatically.
   * Backup Support: Creates a rename_backup.json file in each directory to store the original filenames for easy rollback.
   * Caching: Optimizes API calls by storing and reusing metadata for repeated requests.

**Supported Flags**

   * --i: Prompts for an input directory path, overriding the script’s default behavior of using its current location.
   * --show: Allows the user to explicitly specify the show name, useful if filenames do not contain the show name.
   * --format: Customizes the output format using placeholders such as:
      * {season_episode}: The "S01E01"-style identifier.
       * {episode_name}: The episode title (e.g., "Pilot").
       * {air_date}: The episode's air date.
       * {runtime}: The episode runtime in minutes.
   * --dry: Enables a dry-run mode to preview changes without actually renaming the files.
   * --recursive: Scans and processes all subdirectories (e.g., one for each season) in the base directory.
