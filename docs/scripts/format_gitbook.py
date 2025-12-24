from pathlib import Path
import shutil
import re

RST_ROOT = "docs/source"
MD_ROOT = "docs/_build/md"

INDEX_NAME = "index.md" # from sphinx-build output
README_NAME = "README.md" # gitbook specification
SUMMARY_NAME = "SUMMARY.md" # gitbook specification
SUMMARY_LINES = ["# Summary\n"] # gitbook specification

TOCTREE_RE = re.compile(r"^\s*\.\.\s+toctree::") # from sphinx specification for reStructured (rst) files
ENTRY_RE = re.compile(r"^\s+([^\s:][^\n]*)") # from sphinx specification for reStructured (rst) files

MD_ROOT_PATH = Path(MD_ROOT).resolve()
MD_ROOT_PATH.mkdir(parents=True, exist_ok=True)


def preprocess_for_gitbook():
    """
    Rearrange MD files into GitBook folder structure.
    Generates SUMMARY.md:
      - Outer README appears at same level as first folders
      - Preserves capitalization
    """
    rst_root = Path(RST_ROOT).resolve()

    tree = walk_toctree("index", rst_root)

    process_node("index", tree.get("index", tree), MD_ROOT_PATH)

    write_summary("index", tree.get("index", tree))
    summary_file = MD_ROOT_PATH / SUMMARY_NAME
    summary_file.write_text("\n".join(SUMMARY_LINES), encoding="utf-8")


def walk_toctree(start: str, rst_root: Path, visited=None):
    """Build tree of the file structure from toctrees.
    
    Parameters
    ----------
    start : str
        File name of the starting point of the toctree walk.
    rst_root : pathlib.Path
        Path to the folder with rst files. *.rst files to be in a flatten folder structure.
    visited : set 
        Names of files already visited.

    Returns
    -------
    dict
        Tree of the folder structure.
    """
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


def parse_toctree_entries(rst_path: Path):
    """Analyse rst file and get the sub-files identified under toctree.
    
    Parameters
    ----------
    rst_path : pathlib.Path
        Path to the file being analysed.  

    Returns
    -------
    list of str
        List of the file names identified in the toctree inside the rst file.  
    """
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


def process_node(node_name, node_subtree, parent_dir):
    """Move the sub-files of the node to a new folder.
    
    Parameters
    ----------
    node_name : str
        Name of the file.
    node_subtree : dict
        Sub-tree of folder structure from the current node (file).
    parent_dir : pathlib.Path
        Parent folder of the current file.  
    """
    target_dir = parent_dir / node_name if node_name != "index" else parent_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    # Main MD file
    src_md_candidates = [
        MD_ROOT_PATH / f"{node_name}.md",
        MD_ROOT_PATH / node_name / INDEX_NAME,
    ]
    src_md = next((f for f in src_md_candidates if f.exists()), None)
    if src_md:
        target_file = target_dir / (README_NAME if node_name != "index" else README_NAME)
        shutil.move(str(src_md), target_file)

    # Other MD files matching node_name.*
    for other_md in MD_ROOT_PATH.glob(f"{node_name}.*.md"):
        shutil.move(str(other_md), target_dir / other_md.name)

    # Recurse children
    for child, grandchildren in node_subtree.items():
        process_node(child, grandchildren, target_dir)

def write_summary(node_name, node_subtree, parent_path=Path(), depth=0):
    """Write summary file at each folder structure level.

    Parameters
    ----------
    node_name : str
        Name of the file.
    node_subtree : dict
        Sub-tree of folder structure from the current node (file).
    parent_dir : pathlib.Path
        Parent folder of the current file.  
    depth : int
        Depth on the folder structure.
    """
    indent = "  " * depth

    if node_name == "index": # root README file
        root_readme = MD_ROOT_PATH / README_NAME
        title = get_md_title(root_readme)

        SUMMARY_LINES.append(
            f"* [{title}](README.md)"
        )

        for child, grandchildren in node_subtree.items():
            write_summary(child, grandchildren, parent_path, depth)

        return

    else: # Normal nodes
        folder_path = parent_path / node_name
        readme_path = folder_path / README_NAME

        title = get_md_title(MD_ROOT_PATH / readme_path)

        SUMMARY_LINES.append(
            f"{indent}* [{title}]({readme_path.as_posix()})"
        )

        for child, grandchildren in node_subtree.items():
            write_summary(child, grandchildren, folder_path, depth + 1)


def get_md_title(md_path: Path):
    """Extract first H1 title from a markdown file.
    
    Parameters
    ----------
    md_path : pathlib.Path
        File path to the markdown file.

    Returns
    -------
    str
        H1 Header in the markdown file.
    """
    if not md_path.exists():
        return md_path.parent.name
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
        
    return md_path.parent.name
