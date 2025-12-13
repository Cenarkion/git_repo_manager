# git_repo_manager

A Python script for managing GitHub repositories directly from the command line. This tool interacts with the GitHub API to create, and delete repositories, offering a convenient way to manage your GitHub projects without leaving the terminal.

## Features

*   **Create Repositories:**
    *   Create a new GitHub repository and get instructions to push an existing local repo.
    *   Initialize a `git` repository in the current directory, create a remote GitHub repo, and push the content in one go.
    *   Create public or private repositories (private is the default).
*   **Batch Deletion:** Delete multiple repositories with a single command.
*   **Flexible Token Management:** Supports GitHub Personal Access Tokens via environment variables, a configuration file, or direct prompt.
*   **Owner Detection:** Automatically attempts to detect the repository owner from your global Git configuration.
*   **Confirmation Prompt:** Requires explicit confirmation before deleting each repository to prevent accidental data loss.
*   **Error Handling:** Provides informative messages for common issues like repository not found or insufficient permissions.

## Installation

This is a standalone Python script. You only need to install its dependencies.

### Prerequisites

*   Python 3.x
*   `pip` (Python package installer)
*   `git` must be installed and in your PATH.

### Dependencies

The script requires the `requests` Python library. Install it using pip:

```bash
pip install requests
```

## Configuration

### GitHub Personal Access Token

The script needs a GitHub Personal Access Token to authenticate with the GitHub API. The token requires the following scopes:
*   **`repo`**: For creating and managing repositories.
*   **`delete_repo`**: For deleting repositories.

The script looks for the token in the following order of precedence:

1.  **`GITHUB_TOKEN` Environment Variable:**
    Set the `GITHUB_TOKEN` environment variable:
    ```bash
    export GITHUB_TOKEN="your_github_personal_access_token"
    ```
    *(For a persistent setting, add this line to your shell's profile file, e.g., `~/.bashrc`, `~/.zshrc`).*

2.  **Configuration File (`~/.git_repo_manager/config.ini`):**
    If the script doesn't find the environment variable, it will look for a `config.ini` file in the `~/.git_repo_manager` directory. If you agree, the script can create this for you.
    ```ini
    # ~/.git_repo_manager/config.ini
    [github]
    token = your_github_personal_access_token
    ```

3.  **Prompt:**
    If the token is not found in the other locations, the script will prompt you to enter it securely and ask if you want to save it to the configuration file for future use.

### Repository Owner

The repository owner can be specified using the `--owner` (`-O`) flag. If not provided, the script attempts to retrieve it from your Git configuration (`git config user.name`). To set your Git username globally:

```bash
git config --global user.name "YourGitHubUsername"
```

## Usage

First, make the script executable:
```bash
chmod +x git_repo_manager
```

The script supports three main actions: deleting repositories, creating a remote for an existing local repository, and initializing a new repository from the current directory.

---

### Deleting Repositories

Use the `--repos` (`-R`) flag to specify one or more repositories to delete.

**Examples:**

*   Delete a single repository owned by your configured Git username:
    ```bash
    ./git_repo_manager --repos my-old-project
    ```

*   Delete multiple repositories for a specific owner:
    ```bash
    ./git_repo_manager -R my-old-project another-unused-repo -O my-github-username
    ```
*   Delete a repository belonging to an organization:
    ```bash
    ./git_repo_manager --repos legacy-app --owner MyOrg
    ```

**Important:** The script will ask for confirmation before deleting each repository.

---

### Creating a New Repository

The script offers two ways to create repositories. By default, repositories are created as **private**. Use the `--public` (`-P`) flag to make them public.

#### 1. Create Remote for an Existing Local Repo

If you have an existing local Git repository, use `--create-and-push` (`-C`) to create a remote GitHub repository for it.

**Example:**

```bash
# Creates a new private repository named "my-local-app" on GitHub
./git_repo_manager --create-and-push my-local-app

# Creates a new public repository for an organization
./git_repo_manager -C my-awesome-lib -O MyOrg -P
```
The script will provide you with the `git remote add` and `git push` commands to run.

#### 2. Initialize and Push from Current Directory

Use `--init-and-push` (`-I`) to initialize a Git repository in the current directory, create a new remote repository, and push all contents.

This is useful for turning a local project folder into a new GitHub repository in one step. If the directory contains no files, a `README.md` will be created automatically.

**Example:**

```bash
# Navigate to your project directory
cd my-new-project

# Initialize, create, and push
./git_repo_manager --init-and-push my-new-project --owner my-github-username

# Initialize and push as a public repository
./git_repo_manager -I my-public-project -P
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
