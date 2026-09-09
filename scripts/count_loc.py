#!/usr/bin/env python3
"""
Automated Meaningful Lines of Code (LOC) Counter for AI FinTech Platform.
Adheres strictly to the solo-developer project standard:
- Counts only authentic code, comments, and structure in source files
- Strictly ignores build directories, dependencies, binary files, virtualenvs, and generated artifacts
- Breaks down metrics by component (Frontend, Backend, AI Engines, Database, Tests, Docs)
"""

import os
import sys
from pathlib import Path

# Directories to strictly exclude from counting
EXCLUDED_DIRS = {
    "node_modules",
    ".venv",
    "venv",
    "env",
    "dist",
    "build",
    "__pycache__",
    ".git",
    ".github",
    ".pytest_cache",
    ".coverage",
    "htmlcov",
    ".idea",
    ".vscode",
    ".system_generated",
    "postgres_data",
    "redis_data",
}

# Recognized source file extensions
SOURCE_EXTENSIONS = {
    ".py": "Python",
    ".ts": "TypeScript",
    ".tsx": "TypeScript React",
    ".js": "JavaScript",
    ".jsx": "JavaScript React",
    ".css": "CSS",
    ".html": "HTML",
    ".sql": "SQL",
    ".json": "JSON",
    ".md": "Markdown",
    ".yml": "YAML",
    ".yaml": "YAML",
    ".toml": "TOML",
}


def is_excluded(path: Path) -> bool:
    for part in path.parts:
        if part in EXCLUDED_DIRS or part.startswith("."):
            if part not in {".env.example"}:
                return True
    return False


def count_file(filepath: Path) -> dict:
    total_lines = 0
    blank_lines = 0
    comment_lines = 0
    code_lines = 0

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                total_lines += 1
                stripped = line.strip()
                if not stripped:
                    blank_lines += 1
                elif stripped.startswith(("#", "//", "/*", "*", "<!--")):
                    comment_lines += 1
                else:
                    code_lines += 1
    except Exception:
        pass

    return {
        "total": total_lines,
        "blank": blank_lines,
        "comment": comment_lines,
        "code": code_lines,
    }


def main():
    root_dir = Path(__file__).resolve().parent.parent
    stats = {}
    lang_stats = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Mutate dirnames to skip excluded dirs during traversal
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS and not d.startswith(".")]

        current_path = Path(dirpath)
        if is_excluded(current_path):
            continue

        # Determine component category
        rel_path = current_path.relative_to(root_dir)
        top_component = rel_path.parts[0] if rel_path.parts else "root"

        if top_component not in stats:
            stats[top_component] = {"files": 0, "total": 0, "blank": 0, "comment": 0, "code": 0}

        for fname in filenames:
            fpath = current_path / fname
            ext = fpath.suffix.lower()

            if ext in SOURCE_EXTENSIONS:
                f_stats = count_file(fpath)
                stats[top_component]["files"] += 1
                stats[top_component]["total"] += f_stats["total"]
                stats[top_component]["blank"] += f_stats["blank"]
                stats[top_component]["comment"] += f_stats["comment"]
                stats[top_component]["code"] += f_stats["code"]

                lang = SOURCE_EXTENSIONS[ext]
                if lang not in lang_stats:
                    lang_stats[lang] = {"files": 0, "lines": 0}
                lang_stats[lang]["files"] += 1
                lang_stats[lang]["lines"] += f_stats["total"]

    print("=" * 80)
    print(" AI FinTech Personal Finance & Risk Platform - Meaningful LOC Report")
    print("=" * 80)
    print(f"{'Component':<20} | {'Files':<8} | {'Code':<10} | {'Comments':<10} | {'Blank':<8} | {'Total':<10}")
    print("-" * 80)

    grand_total = {"files": 0, "code": 0, "comment": 0, "blank": 0, "total": 0}
    for comp, data in sorted(stats.items()):
        print(f"{comp:<20} | {data['files']:<8} | {data['code']:<10} | {data['comment']:<10} | {data['blank']:<8} | {data['total']:<10}")
        grand_total["files"] += data["files"]
        grand_total["code"] += data["code"]
        grand_total["comment"] += data["comment"]
        grand_total["blank"] += data["blank"]
        grand_total["total"] += data["total"]

    print("=" * 80)
    print(f"{'GRAND TOTAL':<20} | {grand_total['files']:<8} | {grand_total['code']:<10} | {grand_total['comment']:<10} | {grand_total['blank']:<8} | {grand_total['total']:<10}")
    print("=" * 80)

    print("\nBreakdown by Language:")
    for lang, data in sorted(lang_stats.items(), key=lambda x: x[1]["lines"], reverse=True):
        print(f"  - {lang:<20}: {data['lines']:>8} lines across {data['files']:>4} files")

    print("\nTarget: 500,000+ meaningful lines of code across all modules.")


if __name__ == "__main__":
    main()
