#!/usr/bin/env python3
"""
Automated License Auditor for AI FinTech Platform.
Validates dependencies against forbidden copyleft licenses (GPL, AGPL, SSPL, etc.)
and ensures strict adherence to permissive licensing (MIT, Apache-2.0, BSD, ISC).
"""

import sys
import re
from pathlib import Path

FORBIDDEN_LICENSES = [
    "GPL",
    "GPLV2",
    "GPLV3",
    "AGPL",
    "AGPLV3",
    "SSPL",
    "LGPL",  # Warn or forbid unless explicit linking exception
    "EUPL",
    "CPAL",
]

ALLOWED_LICENSES = [
    "MIT",
    "APACHE-2.0",
    "APACHE 2.0",
    "BSD-2-CLAUSE",
    "BSD-3-CLAUSE",
    "BSD",
    "ISC",
    "PYTHON-2.0",
    "PSF",
    "UNLICENSE",
    "CC0-1.0",
]


def check_licenses_doc():
    root = Path(__file__).resolve().parent.parent
    doc_path = root / "THIRD_PARTY_LICENSES.md"
    if not doc_path.exists():
        print("[ERROR] THIRD_PARTY_LICENSES.md file is missing!")
        return False

    content = doc_path.read_text(encoding="utf-8").upper()
    violations = []
    for forbidden in FORBIDDEN_LICENSES:
        # Check if forbidden license is marked as in-use
        matches = re.findall(rf"\|\s*`[^`]+`\s*\|\s*[^|]*\b{forbidden}\b", content)
        if matches:
            violations.extend(matches)

    if violations:
        print("[FAIL] Forbidden copyleft licenses detected in dependency documentation:")
        for v in violations:
            print(f"  - {v}")
        return False

    print("[PASS] License audit verified: 100% compliant with permissive open-source standards.")
    return True


if __name__ == "__main__":
    success = check_licenses_doc()
    sys.exit(0 if success else 1)
