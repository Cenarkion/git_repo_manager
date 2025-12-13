# Project Overview

This project, `git_repo_manager`, contains a Python script for managing GitHub repositories directly from the command line. It interacts with the GitHub API to create and delete repositories.

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

The script needs a GitHub Personal Access Token. The token requires the `repo` scope (for creating repositories) and `delete_repo` scope (for deleting them). The script obtains the token in the following order:

1.  From the `GITHUB_TOKEN` environment variable.
2.  From a configuration file located at `~/.git_repo_manager/config.ini`.
3.  By prompting you to enter the token if it's not found elsewhere.

The repository owner can be specified using the `--owner` (`-O`) flag. If not provided, it defaults to your Git username.

## Usage

Make the script executable:
```bash
chmod +x git_repo_manager
```

### Create a Repository

Create a remote for an existing local repository:
```bash
./git_repo_manager --create-and-push <repo-name>
```

Initialize the current directory and push it to a new repository:
```bash
./git_repo_manager --init-and-push <repo-name>
```
*Use the `--public` (`-P`) flag to create a public repository (default is private).*

### Delete Repositories

```bash
./git_repo_manager --repos <repo1> [<repo2> ...] [--owner <owner>]
```

**Example:**
```bash
./git_repo_manager --repos my-old-project another-repo --owner my-github-username
```

The script will ask for confirmation before deleting each repository.

# Development Conventions

*   **GitHub Token Management:** Prioritize using environment variables (`GITHUB_TOKEN`) or a dedicated configuration file for secure token storage.
*   **Error Handling:** The script includes error handling for API requests and provides informative messages.
*   **Confirmation:** A confirmation prompt is included before any deletion to prevent accidental data loss.