#!/usr/bin/env python
"""Search, extract, and sync Fubon TradeAPI llms docs."""

from __future__ import annotations

import argparse
import re
import ssl
import sys
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = {
    "index": ROOT / "llms.txt",
    "full": ROOT / "llms-full.txt",
}
DOC_URLS = {
    "index": "https://www.fbs.com.tw/TradeAPI/llms.txt",
    "full": "https://www.fbs.com.tw/TradeAPI/llms-full.txt",
}


def fetch_doc(name: str, timeout: float = 20.0) -> str:
    request = urllib.request.Request(
        DOC_URLS[name],
        headers={"User-Agent": "fubon-trade-api-skill/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset)
    except Exception as exc:  # noqa: BLE001 - urllib wraps TLS failures by Python version.
        if "CERTIFICATE_VERIFY_FAILED" not in str(exc):
            raise
        print(
            f"Warning: TLS verification failed for {DOC_URLS[name]}; retrying this public docs request without certificate verification. {exc}",
            file=sys.stderr,
        )
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset)


def read_doc(name: str, online: bool = False) -> str:
    if online:
        try:
            return fetch_doc(name)
        except Exception as exc:  # noqa: BLE001 - fallback should preserve offline usability.
            print(f"Warning: online fetch failed for {name}; using local cache. {exc}", file=sys.stderr)
    path = DOCS[name]
    return path.read_text(encoding="utf-8")


def line_offsets(text: str) -> list[int]:
    offsets = [0]
    for match in re.finditer(r"\n", text):
        offsets.append(match.end())
    return offsets


def offset_to_line(offsets: list[int], offset: int) -> int:
    lo, hi = 0, len(offsets)
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if offsets[mid] <= offset:
            lo = mid
        else:
            hi = mid
    return lo + 1


def normalize(value: str) -> str:
    return re.sub(r"[\s_\-\\`*#\[\]():]+", "", value).lower()


def command_search(args: argparse.Namespace) -> int:
    query = " ".join(args.query).strip()
    if not query:
        raise SystemExit("search query is required")

    terms = [term for term in re.split(r"\s+", query) if term]
    text = read_doc(args.doc, online=args.online)
    lines = text.splitlines()
    matches: list[tuple[int, str]] = []

    for index, line in enumerate(lines, start=1):
        window_start = max(0, index - args.context - 1)
        window_end = min(len(lines), index + args.context)
        window = "\n".join(lines[window_start:window_end])
        haystack = normalize(window)
        if all(normalize(term) in haystack for term in terms):
            matches.append((index, line))
            if len(matches) >= args.limit:
                break

    source = "online" if args.online else args.doc
    for line_no, line in matches:
        start = max(1, line_no - args.context)
        end = min(len(lines), line_no + args.context)
        print(f"--- {source}:{line_no} ---")
        for current in range(start, end + 1):
            prefix = ">" if current == line_no else " "
            print(f"{prefix}{current}: {lines[current - 1]}")

    if not matches:
        print("No matches.")
    else:
        print(f"\n{len(matches)} match(es), first line {matches[0][0]}.")
    return 0


def command_section(args: argparse.Namespace) -> int:
    title = " ".join(args.title).strip()
    if not title:
        raise SystemExit("section title or keyword is required")

    text = read_doc("full", online=args.online)
    headings = list(re.finditer(r"^(#{2,6})\s+(.+)$", text, re.MULTILINE))
    title_norm = normalize(title)
    chosen = None

    for idx, heading in enumerate(headings):
        heading_text = normalize(heading.group(2))
        if title_norm in heading_text or heading_text in title_norm:
            chosen = (idx, heading)
            break

    if chosen is None:
        keyword = re.search(re.escape(title), text, re.IGNORECASE)
        if not keyword:
            compact_text = normalize(text)
            compact_index = compact_text.find(title_norm)
            keyword = None
            if compact_index >= 0:
                keyword = re.search(re.escape(title.split()[0]), text, re.IGNORECASE)
        if not keyword:
            print("No section or keyword match.")
            return 1
        start = max(0, keyword.start() - args.chars // 2)
        end = min(len(text), keyword.end() + args.chars // 2)
        print(text[start:end])
        return 0

    idx, heading = chosen
    level = len(heading.group(1))
    end = len(text)
    for next_heading in headings[idx + 1 :]:
        if len(next_heading.group(1)) <= level:
            end = next_heading.start()
            break

    section = text[heading.start() : end].strip()
    if len(section) > args.chars:
        section = section[: args.chars].rstrip() + "\n\n[truncated]"
    print(section)
    return 0


def command_lines(args: argparse.Namespace) -> int:
    if args.start < 1:
        raise SystemExit("start line must be >= 1")
    if args.end < args.start:
        raise SystemExit("end line must be >= start line")

    text = read_doc(args.doc, online=args.online)
    lines = text.splitlines()
    start = min(args.start, len(lines))
    end = min(args.end, len(lines))

    for current in range(start, end + 1):
        print(f"{current}: {lines[current - 1]}")
    return 0


def command_sync(args: argparse.Namespace) -> int:
    for name, path in DOCS.items():
        text = fetch_doc(name, timeout=args.timeout)
        path.write_text(text, encoding="utf-8", newline="\n")
        print(f"Updated {path.name} from {DOC_URLS[name]} ({len(text.splitlines())} lines).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search", help="search llms docs by keyword")
    search.add_argument("query", nargs="+")
    search.add_argument("--doc", choices=DOCS.keys(), default="full")
    search.add_argument("--online", action="store_true", help="try official online docs first, then local cache")
    search.add_argument("--limit", type=int, default=20)
    search.add_argument("--context", type=int, default=4)
    search.set_defaults(func=command_search)

    section = subparsers.add_parser("section", help="extract a markdown section from llms-full.txt")
    section.add_argument("title", nargs="+")
    section.add_argument("--online", action="store_true", help="try official online docs first, then local cache")
    section.add_argument("--chars", type=int, default=12000)
    section.set_defaults(func=command_section)

    lines = subparsers.add_parser("lines", help="print a line range from a bundled doc")
    lines.add_argument("start", type=int)
    lines.add_argument("end", type=int)
    lines.add_argument("--doc", choices=DOCS.keys(), default="full")
    lines.add_argument("--online", action="store_true", help="try official online docs first, then local cache")
    lines.set_defaults(func=command_lines)

    sync = subparsers.add_parser("sync", help="download official llms docs into the local cache")
    sync.add_argument("--timeout", type=float, default=30.0)
    sync.set_defaults(func=command_sync)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())



