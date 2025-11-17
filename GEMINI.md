# Project Overview

This project, `git_repo_manager`, contains a Python script (`git_repo_manager.py`) designed for managing GitHub repositories directly from the command line. It interacts with the GitHub API to perform various repository management tasks.

**Main Technologies:**
*   Python
*   `requests` library for HTTP requests
*   `argparse` for command-line argument parsing
*   `configparser` for reading configuration files

# Building and Running

This is a standalone Python script and does not require a separate build step.

## Dependencies

The script requires the `requests` Python library. You can install it using pip:
```bash
pip install requests
```

## Configuration

The script can obtain your GitHub Personal Access Token in a few ways (in order of precedence):
1.  From the `GITHUB_TOKEN` environment variable.
2.  From a configuration file located at `~/.rolecreate/config.ini`. The file should have a `[github]` section with a `token` key:
    ```ini
    [github]
    token = your_github_personal_access_token
    ```
    **Note:** The directory `~/.rolecreate` and the file `config.ini` will be created if they don't exist. The script also attempts to set appropriate permissions for the config file (read-only for the owner).
3.  By prompting you to enter the token if it's not found elsewhere.

The repository owner can be specified using the `--owner` flag. If not provided, the script attempts to retrieve it from your Git configuration (`git config user.name`).

## Usage

To run the script, you can execute it directly after making it executable:

```bash
./git_repo_manager.py --repos <repo1> [<repo2> ...] [--owner <owner_username_or_org>]
```

Alternatively, you can explicitly run it with Python:

```bash
python git_repo_manager.py --repos <repo1> [<repo2> ...] [--owner <owner_username_or_org>]
```

**Example:**
```bash
./delete_repos.py --repos my-old-project another-unused-repo --owner my-github-username
```

The script will ask for confirmation before deleting each repository.

# Development Conventions

*   **GitHub Token Management:** Prioritize using environment variables (`GITHUB_TOKEN`) or a dedicated configuration file (`~/.rolecreate/config.ini`) for storing your GitHub Personal Access Token securely.
*   **Error Handling:** The script includes basic error handling for GitHub API requests and provides informative messages for common issues like repository not found or insufficient permissions.
*   **Confirmation:** A confirmation prompt is included before any deletion to prevent accidental data loss.