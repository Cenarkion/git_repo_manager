# git_repo_manager

A Python script for managing GitHub repositories directly from the command line. This tool interacts with the GitHub API to perform various repository management tasks, offering a convenient way to manage your GitHub projects.

## Features

*   **Batch Deletion:** Delete multiple repositories with a single command.
*   **Flexible Token Management:** Supports GitHub Personal Access Tokens via environment variables, a configuration file, or direct prompt.
*   **Owner Detection:** Automatically attempts to detect the repository owner from Git configuration if not explicitly provided.
*   **Confirmation Prompt:** Requires explicit confirmation before deleting each repository to prevent accidental data loss.
*   **Error Handling:** Provides informative messages for common issues like repository not found or insufficient permissions.

## Installation

This is a standalone Python script. You only need to install its dependencies.

### Prerequisites

*   Python 3.x
*   `pip` (Python package installer)

### Dependencies

The script requires the `requests` Python library. Install it using pip:

```bash
pip install requests
```

## Configuration

The script needs a GitHub Personal Access Token with the `delete_repo` scope to authenticate with the GitHub API. It looks for the token in the following order of precedence:

1.  **`GITHUB_TOKEN` Environment Variable:**
    Set the `GITHUB_TOKEN` environment variable:
    ```bash
    export GITHUB_TOKEN="your_github_personal_access_token"
    ```
    (For persistent setting, add this line to your shell's profile file, e.g., `~/.bashrc`, `~/.zshrc`).

2.  **Configuration File (`~/.rolecreate/config.ini`):**
    Create a directory `~/.rolecreate` and a file `config.ini` inside it. The file should have a `[github]` section with a `token` key:
    ```ini
    # ~/.rolecreate/config.ini
    [github]
    token = your_github_personal_access_token
    ```
    The script will attempt to set appropriate permissions for this file (read-only for the owner) if it creates it.

3.  **Prompt:**
    If the token is not found in the environment variable or the configuration file, the script will prompt you to enter it securely.

### Repository Owner

The repository owner can be specified using the `--owner` flag. If not provided, the script attempts to retrieve it from your Git configuration (`git config user.name`). To set your Git username globally:

```bash
git config --global user.name "YourGitHubUsername"
```

## Usage

To run the script, you can execute it directly after making it executable:

```bash
chmod +x git_repo_manager.py
./git_repo_manager.py --repos <repo1> [<repo2> ...] [--owner <owner_username_or_org>]
```

Alternatively, you can explicitly run it with Python:

```bash
python git_repo_manager.py --repos <repo1> [<repo2> ...] [--owner <owner_username_or_org>]
```

### Examples

Delete a single repository owned by your configured Git username:

```bash
./git_repo_manager.py --repos my-old-project
```

Delete multiple repositories for a specific owner:

```bash
./delete_repos.py --repos my-old-project another-unused-repo --owner my-github-username
```

Delete a repository belonging to an organization:

```bash
python delete_repos.py --repos legacy-app --owner MyOrg
```

**Important:** The script will ask for confirmation before deleting each repository. Type `yes` to proceed with the deletion.
