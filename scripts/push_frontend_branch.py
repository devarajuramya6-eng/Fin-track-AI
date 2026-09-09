#!/usr/bin/env python3
"""
Push frontend codebase to branch 'frontend' under Ramya Devaraju <devarajuramya6@gmail.com>
Target: https://github.com/devarajuramya6-eng/Fin-track-AI/tree/frontend
"""

import os
import subprocess
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent

env = os.environ.copy()
env["GIT_AUTHOR_NAME"] = "Ramya Devaraju"
env["GIT_AUTHOR_EMAIL"] = "devarajuramya6@gmail.com"
env["GIT_COMMITTER_NAME"] = "Ramya Devaraju"
env["GIT_COMMITTER_EMAIL"] = "devarajuramya6@gmail.com"

def git(cmd_list):
    return subprocess.run(["git"] + cmd_list, cwd=str(root_dir), env=env, capture_output=True, text=True, check=True)

def push_frontend():
    print("Preparing dedicated 'frontend' branch for Ramya Devaraju <devarajuramya6@gmail.com>...")
    
    # Checkout or create frontend branch
    try:
        git(["checkout", "-B", "frontend"])
    except Exception as e:
        print("Checkout branch error:", e)
        
    # Configure author
    git(["config", "user.name", "Ramya Devaraju"])
    git(["config", "user.email", "devarajuramya6@gmail.com"])
    
    # Stage all frontend files
    git(["add", "frontend/"])
    git(["add", "package.json", "Makefile", "README.md", ".gitignore"])
    
    # Commit
    try:
        git(["commit", "-m", "feat(frontend): deliver complete React 18, Vite, Tailwind CSS, and quantitative analytics UI suite"])
    except Exception:
        # Might already have some commits
        pass
        
    # Ensure remote is set
    remote_url = "https://github.com/devarajuramya6-eng/Fin-track-AI.git"
    subprocess.run(["git", "remote", "remove", "origin"], cwd=str(root_dir), capture_output=True)
    subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=str(root_dir), capture_output=True)
    
    # Push frontend branch to origin
    print("Pushing 'frontend' branch to GitHub...")
    res = subprocess.run(["git", "push", "--force", "-u", "origin", "frontend"], cwd=str(root_dir), env=env, capture_output=True, text=True, check=True)
    print(res.stdout or res.stderr)
    print("Successfully pushed to https://github.com/devarajuramya6-eng/Fin-track-AI/tree/frontend !")

if __name__ == "__main__":
    push_frontend()
