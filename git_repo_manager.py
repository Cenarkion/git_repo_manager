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

def create_and_push_repo(repo_name, token):
    """Creates a private GitHub repository and pushes the current local repository to it."""
    repo_url = create_github_repo(repo_name, token)
    if not repo_url:
        print("Failed to get repository URL after creation.")
        sys.exit(1)

    try:
        print(f"Adding remote origin: {repo_url}")
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
        print("Pushing to GitHub...")
        subprocess.run(["git", "push", "-u", "origin", "master"], check=True)
        print(f"Successfully pushed to {repo_url}")
    except subprocess.CalledProcessError as e:
        print(f"Error during git operations: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Manage GitHub repositories (delete or create/push).")
    parser.add_argument("--repos", "-r", nargs='+', help="List of repository names to delete.")
    parser.add_argument("--owner", "-o", help="The GitHub username or organization that owns the repositories. If not provided, it will try to get it from git config user.name.")
    parser.add_argument("--create-and-push", "-c", metavar="REPO_NAME", help="Create a new private GitHub repository with the given name and push the current local repository to it.")
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

    if args.create_and_push:
        create_and_push_repo(args.create_and_push, token)
    elif args.repos:
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
    else:
        parser.print_help()
        sys.exit(1)

def create_github_repo(repo_name, token):
    """Creates a private GitHub repository."""
    API_URL = "https://api.github.com"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "name": repo_name,
        "private": True,
        "description": "A Python script to easily delete one or more GitHub repositories."
    }

    try:
        r = requests.post(f"{API_URL}/user/repos", headers=headers, json=data)
        r.raise_for_status()
        print(f"Successfully created private repository: {repo_name}")
        return r.json()["clone_url"]
    except requests.exceptions.RequestException as err:
        print(f"Error creating repository {repo_name}: {err}")
        if r.status_code == 422:
            print("Repository with this name already exists or invalid name.")
        sys.exit(1)

if __name__ == "__main__":
    main()
