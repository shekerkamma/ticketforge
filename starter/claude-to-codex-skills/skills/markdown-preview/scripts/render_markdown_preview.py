#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import http.server
import os
import socketserver
import subprocess
import sys
import threading
from pathlib import Path


def render_markdown(text: str) -> str:
    try:
        import markdown  # type: ignore

        return markdown.markdown(
            text,
            extensions=["fenced_code", "tables", "toc"],
        )
    except Exception:
        pass

    try:
        from cmarkgfm import github_flavored_markdown_to_html  # type: ignore

        return github_flavored_markdown_to_html(text)
    except Exception:
        pass

    try:
        import commonmark  # type: ignore

        return commonmark.commonmark(text)
    except Exception:
        pass

    return "<pre>{}</pre>".format(html.escape(text))


def maybe_render_marp(input_path: Path, output_path: Path) -> bool:
    if input_path.suffixes[-2:] != [".marp", ".md"]:
        return False

    marp = None
    for candidate in (["marp"], ["npx", "@marp-team/marp-cli"]):
        try:
            result = subprocess.run(
                [*candidate, "--version"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                marp = candidate
                break
        except Exception:
            continue

    if marp is None:
        return False

    cmd = [
        *marp,
        "--html",
        "--allow-local-files",
        "--output",
        str(output_path),
        str(input_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return result.returncode == 0 and output_path.exists()


def build_html(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    body {{
      margin: 40px auto;
      max-width: 860px;
      padding: 0 24px 64px;
      font: 18px/1.6 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: #1f2937;
      background: #f8fafc;
    }}
    main {{
      background: white;
      padding: 40px;
      border-radius: 16px;
      box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
    }}
    pre {{
      overflow-x: auto;
      background: #0f172a;
      color: #e2e8f0;
      padding: 16px;
      border-radius: 12px;
    }}
    code {{
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
    }}
    td, th {{
      border: 1px solid #cbd5e1;
      padding: 8px 10px;
      text-align: left;
    }}
    blockquote {{
      border-left: 4px solid #94a3b8;
      margin-left: 0;
      padding-left: 16px;
      color: #475569;
    }}
    img {{
      max-width: 100%;
      height: auto;
    }}
  </style>
</head>
<body>
  <main>
    {body}
  </main>
</body>
</html>
"""


def serve_directory(directory: Path, port: int) -> None:
    os.chdir(directory)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        print(f"serving http://127.0.0.1:{port}/")
        httpd.serve_forever()


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a markdown file to HTML preview.")
    parser.add_argument("input", help="Input markdown file")
    parser.add_argument("--output", help="Output HTML path")
    parser.add_argument("--serve", action="store_true", help="Serve the output directory locally")
    parser.add_argument("--port", type=int, default=8765, help="Port for --serve")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"missing input: {input_path}", file=sys.stderr)
        return 1

    if args.output:
        output_path = Path(args.output).resolve()
    else:
        suffix = ".html"
        output_path = input_path.with_suffix(suffix)
        if input_path.name.endswith(".marp.md"):
            output_path = input_path.with_name(input_path.name[:-3] + ".html")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not maybe_render_marp(input_path, output_path):
        text = input_path.read_text(encoding="utf-8")
        body = render_markdown(text)
        output_path.write_text(build_html(input_path.name, body), encoding="utf-8")

    print(output_path)

    if args.serve:
        server_dir = output_path.parent
        thread = threading.Thread(
            target=serve_directory,
            args=(server_dir, args.port),
            daemon=False,
        )
        thread.start()
        thread.join()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
