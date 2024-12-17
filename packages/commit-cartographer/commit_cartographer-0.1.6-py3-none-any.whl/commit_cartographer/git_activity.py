import git
from collections import defaultdict
import sys
import os
import click

def get_folder_commit_counts(repo_path):
    """
    Get commit counts for each folder in the repository,
    but only for files that currently exist.
    
    Args:
        repo_path (str): Path to the Git repository
        
    Returns:
        dict: Dictionary mapping folder paths to commit counts
    """
    try:
        repo = git.Repo(repo_path)
    except git.InvalidGitRepositoryError:
        print(f"Error: {repo_path} is not a valid Git repository", file=sys.stderr)
        return {}

    # Get current folder structure
    current_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            # Skip .git folder
            if '.git' in root:
                continue
            # Get path relative to repo root
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, repo_path)
            current_files.append(rel_path)

    folder_counts = defaultdict(int)
    
    # Get all commits
    for commit in repo.iter_commits():
        for file in commit.stats.files.keys():
            # Only count commits for files that currently exist
            if file in current_files:
                # Count the file itself
                folder_counts[file] += 1
                
                # Split the path and increment count for each parent folder
                parts = file.split('/')
                for i in range(len(parts) - 1):
                    folder = '/'.join(parts[:i+1])
                    if folder:  # Skip empty strings
                        folder_counts[folder] += 1
    
    return dict(folder_counts)

def generate_gradient_colors(num_steps):
    """
    Generate a list of colors for a gradient.
    
    Args:
        num_steps (int): Number of steps in the gradient
        
    Returns:
        list: List of hex color codes
    """
    colors = []
    for i in range(num_steps):
        # Calculate the color based on the step
        r = int(255 * (i / (num_steps - 1)))
        g = int(255 * (1 - (i / (num_steps - 1))))
        b = 255  # Keep blue constant
        colors.append(f'#{r:02x}{g:02x}{b:02x}')
    return colors

def generate_mermaid(folder_counts):
    """
    Generate a Mermaid flowchart diagram from folder commit counts.
    Maximum depth of 4 levels from root, using a 10-step color gradient.
    
    Args:
        folder_counts (dict): Dictionary mapping folder paths to commit counts
        
    Returns:
        str: Mermaid flowchart diagram as a string
    """
    if not folder_counts:
        return "flowchart LR\n    root_node[/root\\]"
        
    total_commits = sum(folder_counts.values())
    min_count = min(folder_counts.values())
    max_count = max(folder_counts.values())
    
    # Generate 10-step gradient colors
    gradient_colors = generate_gradient_colors(10)
    
    mermaid = ["flowchart LR"]
    
    # Add root node with trapezoid shape
    mermaid.append("    root_node[/root\\]")
    mermaid.append("    style root_node fill:#ffffff,stroke:#333,stroke-width:2px")
    
    # Process folder paths up to 4 levels deep
    for folder, count in folder_counts.items():
        # Skip folders deeper than 4 levels
        if folder.count('/') > 3:
            continue
        
        # Map commit count to gradient color
        if total_commits > 0:
            normalized_count = (count - min_count) / (max_count - min_count)
            color_index = int(normalized_count * (len(gradient_colors) - 1))
            color = gradient_colors[color_index]
        else:
            color = '#ffffff'
        
        parts = folder.split('/')
        node_name = f"node_{folder.replace('/', '_')}"
        
        # Handle top-level folders and subfolders
        if '/' not in folder:  # Top-level folder
            parent_name = "root_node"
            folder_label = folder
        else:  # Subfolder
            parent_name = f"node_{'/'.join(parts[:-1]).replace('/', '_')}"
            folder_label = parts[-1]
        
        # Use folder shape for nodes
        mermaid.append(f"    {parent_name} --> {node_name}[/{folder_label}\\]")
        mermaid.append(f"    style {node_name} fill:{color},stroke:#333,stroke-width:2px")
    
    return "\n".join(mermaid)

def generate_tree(folder_counts):
    """
    Generate an ASCII tree diagram from folder commit counts.
    
    Args:
        folder_counts (dict): Dictionary mapping folder paths to commit counts
        
    Returns:
        str: ASCII tree diagram as a string
    """
    if not folder_counts:
        return "root/"

    # Sort folders to ensure consistent ordering
    sorted_paths = sorted(folder_counts.items(), key=lambda x: x[0])
    
    tree_lines = ["root/"]
    last_parts = []
    
    for path, count in sorted_paths:
        parts = path.split('/')
        current_depth = len(parts)
        
        # Calculate the prefix based on depth and relationship to siblings
        for i, part in enumerate(parts):
            if i >= len(last_parts) or parts[i] != last_parts[i]:
                # New branch
                prefix = "    " * i + "├── " if i < current_depth - 1 else "    " * i + "└── "
                tree_lines.append(f"{prefix}{part}/ ({count} commits)")
                
        last_parts = parts
    
    return "\n".join(tree_lines)

@click.command()
@click.option(
    '-p', '--path',
    default='.',
    help='Path to the Git repository (default: current directory)',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True)
)
@click.option(
    '-o', '--output',
    default='git_activity.md',
    help='Output markdown file path (default: git_activity.md)',
    type=click.Path(dir_okay=False, writable=True)
)
@click.option(
    '--max-depth',
    default=4,
    help='Maximum folder depth to display (default: 4)',
    type=int
)
@click.option(
    '--style',
    type=click.Choice(['mermaid', 'tree']),
    default='mermaid',
    help='Output style (default: mermaid)'
)
def main(path, output, max_depth, style):
    """Generate a diagram showing Git repository folder activity."""
    try:
        counts = get_folder_commit_counts(path)
        
        with open(output, 'w') as f:
            f.write("# Git Repository Activity Diagram\n\n")
            
            if style == 'mermaid':
                diagram = generate_mermaid(counts)
                f.write("```mermaid\n")
                f.write(diagram)
                f.write("\n```\n")
            else:  # tree style
                tree = generate_tree(counts)
                f.write("```\n")
                f.write(tree)
                f.write("\n```\n")
            
        click.echo(f"Diagram has been written to {output}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    main()