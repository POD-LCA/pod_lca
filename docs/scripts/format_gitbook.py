from pathlib import Path
import shutil
import re

TOCTREE_RE = re.compile(r"^\s*\.\.\s+toctree::")
ENTRY_RE = re.compile(r"^\s+([^\s:][^\n]*)")


def parse_toctree_entries(rst_path: Path):
    entries = []
    in_toctree = False
    for line in rst_path.read_text(encoding="utf-8").splitlines():
        if TOCTREE_RE.match(line):
            in_toctree = True
            continue
        if in_toctree:
            if not line.strip():
                continue
            if not line.startswith(" "):
                in_toctree = False
                continue
            if line.strip().startswith(":"):
                continue
            m = ENTRY_RE.match(line)
            if m:
                entries.append(m.group(1).strip())
    return entries


def walk_toctree(start: str, rst_root: Path, visited=None):
    if visited is None:
        visited = set()
    tree = {}
    if start in visited:
        return tree
    visited.add(start)

    rst_file = rst_root / f"{start}.rst"
    if not rst_file.exists():
        return tree

    for entry in parse_toctree_entries(rst_file):
        tree[entry] = walk_toctree(entry, rst_root, visited)
    return tree


def gitbookify_structure_with_summary(
    rst_root: str, md_root: str, index_name="index.md", readme_name="README.md"
):
    """
    Rearrange MD files into GitBook folder structure.
    Generates SUMMARY.md:
      - Outer README appears at same level as first folders
      - Preserves capitalization
    """
    rst_root = Path(rst_root).resolve()
    md_root = Path(md_root).resolve()
    md_root.mkdir(parents=True, exist_ok=True)

    tree = walk_toctree("index", rst_root)

    # ----------------------------
    # 1. Rearrange MD files
    # ----------------------------
    def process_node(node_name, node_subtree, parent_dir):
        target_dir = parent_dir / node_name if node_name != "index" else parent_dir
        target_dir.mkdir(parents=True, exist_ok=True)

        # Main MD file
        src_md_candidates = [
            md_root / f"{node_name}.md",
            md_root / node_name / index_name,
        ]
        src_md = next((f for f in src_md_candidates if f.exists()), None)
        if src_md:
            target_file = target_dir / (readme_name if node_name != "index" else readme_name)
            shutil.move(str(src_md), target_file)

        # Other MD files matching node_name.*
        for other_md in md_root.glob(f"{node_name}.*.md"):
            shutil.move(str(other_md), target_dir / other_md.name)

        # Recurse children
        for child, grandchildren in node_subtree.items():
            process_node(child, grandchildren, target_dir)

    process_node("index", tree.get("index", tree), md_root)

    # ----------------------------
    # 2. Generate SUMMARY.md
    # ----------------------------
    summary_lines = ["# Summary\n"]

    def get_md_title(md_path: Path) -> str:
        """Extract first H1 title from a Markdown file."""
        if not md_path.exists():
            return md_path.parent.name
        for line in md_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
        return md_path.parent.name


    def write_summary(node_name, node_subtree, parent_path=Path(), depth=0):
        indent = "  " * depth

        if node_name == "index":
            # Root README as a top-level peer
            root_readme = md_root / "README.md"
            title = get_md_title(root_readme)

            summary_lines.append(
                f"* [{title}](README.md)"
            )

            # IMPORTANT:
            # Children stay at the SAME level
            for child, grandchildren in node_subtree.items():
                write_summary(child, grandchildren, parent_path, depth)

            return

        # Normal nodes
        folder_path = parent_path / node_name
        readme_path = folder_path / "README.md"

        title = get_md_title(md_root / readme_path)

        summary_lines.append(
            f"{indent}* [{title}]({readme_path.as_posix()})"
        )

        for child, grandchildren in node_subtree.items():
            write_summary(child, grandchildren, folder_path, depth + 1)



    write_summary("index", tree.get("index", tree))

    summary_file = md_root / "SUMMARY.md"
    summary_file.write_text("\n".join(summary_lines), encoding="utf-8")
