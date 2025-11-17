#!/usr/bin/env python3

import requests
import argparse
import os
import sys
import getpass
import configparser
import stat
import subprocess

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".rolecreate")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.ini")

def get_github_token_from_config():
    """Reads the GitHub token from the configuration file."""
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        if 'github' in config and 'token' in config['github']:
            return config['github']['token']
    return None

def delete_github_repo(repo_owner, repo_name, token):
    """Deletes a GitHub repository."""
    API_URL = "https://api.github.com"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    delete_url = f"{API_URL}/repos/{repo_owner}/{repo_name}"
    
    try:
        r = requests.delete(delete_url, headers=headers)
        r.raise_for_status()
        print(f"Successfully deleted repository: {repo_owner}/{repo_name}")
    except requests.exceptions.RequestException as err:
        print(f"Error deleting repository {repo_owner}/{repo_name}: {err}")
        if r.status_code == 404:
            print("Repository not found. It might have already been deleted or the name/owner is incorrect.")
        elif r.status_code == 403:
            print("Forbidden. Check if your token has the 'delete_repo' scope.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Delete one or more GitHub repositories.")
    parser.add_argument("--repos", "-r", nargs='+', required=True, help="List of repository names to delete.")
    parser.add_argument("--owner", "-o", help="The GitHub username or organization that owns the repositories. If not provided, it will try to get it from git config user.name.")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        token = get_github_token_from_config()

    if not token:
        try:
            token = getpass.getpass("GitHub token not found. Please enter your GitHub personal access token: ")
        except getpass.GetPassWarning:
            print("Could not read password securely.")
            token = input("GitHub token not found. Please enter your GitHub personal access token: ")

    if not token:
        print("GitHub token not provided. Please set the GITHUB_TOKEN environment variable, provide it in ~/.rolecreate/config.ini, or enter the token when prompted.")
        sys.exit(1)

    repo_owner = args.owner
    if not repo_owner:
        try:
            repo_owner = subprocess.check_output(["git", "config", "user.name"]).strip().decode()
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Repository owner not provided and could not be found in git config. Please use the --owner flag or set it in your git config (git config --global user.name <username>).")
            sys.exit(1)

    print(f"Attempting to delete repositories for owner: {repo_owner}")
    for repo_name in args.repos:
        confirm = input(f"Are you sure you want to delete '{repo_owner}/{repo_name}'? This action cannot be undone. Type 'yes' to confirm: ")
        if confirm.lower() == 'yes':
            delete_github_repo(repo_owner, repo_name, token)
        else:
            print(f"Skipping deletion of {repo_owner}/{repo_name}.")

if __name__ == "__main__":
    main()
