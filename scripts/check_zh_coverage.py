#!/usr/bin/env python3
"""
Check translation coverage for zh_CN locale.
Fails if coverage is below the specified threshold.

Usage:
    python scripts/check_zh_coverage.py [--threshold 95]
"""

import argparse
import sys
from pathlib import Path


def check_coverage(locale_dir: Path, threshold: float) -> tuple[int, int, float]:
    """
    Check translation coverage for all .po files.
    
    Returns:
        (translated_count, total_count, coverage_percentage)
    """
    total_translated = 0
    total_msgids = 0
    
    po_files = sorted(locale_dir.rglob('*.po'))
    
    for po_file in po_files:
        with open(po_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        i = 0
        while i < len(lines):
            if lines[i].startswith('msgid "') and lines[i].strip() != 'msgid ""':
                # Get msgid
                msgid = lines[i][7:-2] if lines[i].endswith('"\n') else ""
                j = i + 1
                while j < len(lines) and lines[j].startswith('"'):
                    msgid += lines[j][1:-2] if lines[j].endswith('"\n') else ""
                    j += 1
                
                # Get msgstr
                if j < len(lines) and lines[j].startswith('msgstr "'):
                    msgstr = lines[j][8:-2] if lines[j].endswith('"\n') else ""
                    k = j + 1
                    while k < len(lines) and lines[k].startswith('"'):
                        msgstr += lines[k][1:-2] if lines[k].endswith('"\n') else ""
                        k += 1
                    
                    if msgid.strip():
                        total_msgids += 1
                        if msgstr.strip():
                            total_translated += 1
                    
                    i = k
                    continue
            i += 1
    
    coverage = (total_translated / total_msgids * 100) if total_msgids > 0 else 0
    return total_translated, total_msgids, coverage


def main():
    parser = argparse.ArgumentParser(
        description='Check translation coverage for zh_CN locale'
    )
    parser.add_argument(
        '--threshold',
        type=float,
        default=95.0,
        help='Minimum coverage percentage required (default: 95.0)'
    )
    parser.add_argument(
        '--locale-dir',
        type=str,
        default='locale/zh_CN/LC_MESSAGES',
        help='Path to locale directory (default: locale/zh_CN/LC_MESSAGES)'
    )
    args = parser.parse_args()
    
    # Find workspace root
    script_dir = Path(__file__).parent
    workspace_root = script_dir.parent
    locale_dir = workspace_root / args.locale_dir
    
    if not locale_dir.exists():
        print(f"ERROR: Locale directory not found: {locale_dir}")
        sys.exit(1)
    
    translated, total, coverage = check_coverage(locale_dir, args.threshold)
    
    print(f"Translation Coverage Report")
    print(f"===========================")
    print(f"Locale: zh_CN")
    print(f"Total msgids: {total}")
    print(f"Translated: {translated}")
    print(f"Coverage: {coverage:.1f}%")
    print(f"Threshold: {args.threshold}%")
    print()
    
    if coverage >= args.threshold:
        print(f"✓ PASS: Coverage {coverage:.1f}% >= {args.threshold}%")
        sys.exit(0)
    else:
        print(f"✗ FAIL: Coverage {coverage:.1f}% < {args.threshold}%")
        sys.exit(1)


if __name__ == '__main__':
    main()
