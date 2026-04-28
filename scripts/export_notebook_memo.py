#!/usr/bin/env python3
"""Export a Jupyter notebook into a Jekyll research memo.

This keeps the notebook as the source of truth while publishing a curated,
static markdown version with embedded chart images for the site.
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import re
from pathlib import Path


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def clean_heading_numbers(text: str) -> str:
    return re.sub(r"^(#+)\s+\d+(?:\.\d+)*\.?\s*", r"\1 ", text, flags=re.MULTILINE)


def should_skip_markdown(text: str) -> bool:
    stripped = text.strip()
    return stripped in {"# Import libraries", "---\n\n# Import libraries"}


def build_front_matter(args: argparse.Namespace, notebook_name: str) -> str:
    lines = [
        "---",
        "layout: page",
        f'title: "{args.title}"',
        f"date: {args.date}",
        f"description: >",
        f"  {args.description}",
        f'project_tags: "{args.tags}"',
        f'summary: "{args.summary}"',
        f'notebook_source: "/{notebook_name}"',
        f'asset_dir: "/assets/img/projects/{args.slug}"',
        "---",
        "",
    ]
    return "\n".join(lines)


def render_intro(args: argparse.Namespace, notebook_name: str) -> str:
    download_name = args.download or f"{notebook_name.removesuffix('.ipynb')}.zip"
    download_href = f"/notebooks/{download_name.replace(' ', '%20')}"
    return "\n".join(
        [
            '<div class="qr-memo-meta">',
            '  <p class="qr-memo-meta__eyebrow">Research Memo</p>',
            f"  <p>{html.escape(args.summary)}</p>",
            '  <div class="qr-memo-meta__actions">',
            f'    <a class="qr-btn qr-btn--primary" href="{download_href}">Download Notebook</a>',
            "  </div>",
            "</div>",
            "",
        ]
    )


def export_notebook(args: argparse.Namespace) -> None:
    notebook_path = Path(args.notebook).resolve()
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    repo_root = Path(args.repo_root).resolve()
    output_md = repo_root / "_projects" / f"{args.date}-{args.slug}.md"
    output_img_dir = repo_root / "assets" / "img" / "projects" / args.slug
    output_img_dir.mkdir(parents=True, exist_ok=True)

    parts = [
        build_front_matter(args, notebook_path.name),
        render_intro(args, notebook_path.name),
    ]

    image_index = 1
    for cell in notebook.get("cells", []):
        cell_type = cell.get("cell_type")
        if cell_type == "markdown":
            text = "".join(cell.get("source", []))
            text = clean_heading_numbers(text).strip()
            if text and not should_skip_markdown(text):
                parts.append(text)
                parts.append("")
            continue

        if cell_type != "code":
            continue

        for output in cell.get("outputs", []):
            data = output.get("data", {})
            image_b64 = data.get("image/png")
            if not image_b64:
                continue

            image_name = f"figure-{image_index:02d}.png"
            image_path = output_img_dir / image_name
            image_path.write_bytes(base64.b64decode(image_b64))

            parts.extend(
                [
                    '<figure class="qr-figure">',
                    f'  <img src="{{{{ "/assets/img/projects/{args.slug}/{image_name}" | relative_url }}}}" alt="{html.escape(args.title)} figure {image_index}">',
                    f"  <figcaption>Figure {image_index}. Exported directly from the notebook output.</figcaption>",
                    "</figure>",
                    "",
                ]
            )
            image_index += 1

    output_md.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")

    print(f"Wrote markdown: {output_md}")
    print(f"Wrote images:   {output_img_dir}")
    print(f"Images saved:   {image_index - 1}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--notebook", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--tags", required=True)
    parser.add_argument("--download")
    args = parser.parse_args()
    export_notebook(args)


if __name__ == "__main__":
    main()
