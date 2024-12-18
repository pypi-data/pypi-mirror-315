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

def generate_diagram(path_counts, verbose=False):
    """
    Generate a Mermaid flowchart diagram from folder and file commit counts.
    Maximum depth of 4 levels from root, using a 10-step color gradient.
    
    Args:
        path_counts (dict): Dictionary mapping paths (folders/files) to commit counts
        verbose (bool): If True, include files in the diagram. If False, only show folders
        
    Returns:
        str: Mermaid flowchart diagram as a string
    """
    if not path_counts:
        return "flowchart LR\n    root_node[/root\\]"
        
    total_commits = sum(path_counts.values())
    min_count = min(path_counts.values())
    max_count = max(path_counts.values())
    
    # Generate 10-step gradient colors
    gradient_colors = generate_gradient_colors(10)
    
    mermaid = ["flowchart LR"]
    
    # Add root node with trapezoid shape
    mermaid.append("    root_node[/root\\]")
    mermaid.append("    style root_node fill:#ffffff,stroke:#333,stroke-width:2px")
    
    # Process paths up to 4 levels deep
    for path, count in path_counts.items():
        # Skip paths deeper than 4 levels
        if path.count('/') > 3:
            continue
            
        # Skip files if not in verbose mode
        if not verbose and '.' in path.split('/')[-1]:
            continue
        
        # Map commit count to gradient color
        if total_commits > 0:
            normalized_count = (count - min_count) / (max_count - min_count)
            color_index = int(normalized_count * (len(gradient_colors) - 1))
            color = gradient_colors[color_index]
        else:
            color = '#ffffff'
        
        parts = path.split('/')
        node_name = f"node_{path.replace('/', '_').replace('.', '_')}"
        
        # Handle top-level paths and subpaths
        if '/' not in path:  # Top-level path
            parent_name = "root_node"
            path_label = path
        else:  # Subpath
            parent_name = f"node_{'/'.join(parts[:-1]).replace('/', '_')}"
            path_label = parts[-1]
        
        # Use different shapes for files and folders
        is_file = '.' in parts[-1]
        if is_file:
            # Use rectangle shape for files
            mermaid.append(f"    {parent_name} --> {node_name}[{path_label}]")
        else:
            # Use folder shape (trapezoid) for directories
            mermaid.append(f"    {parent_name} --> {node_name}[/{path_label}\\]")
        
        mermaid.append(f"    style {node_name} fill:{color},stroke:#333,stroke-width:2px")
    
    return "\n".join(mermaid)
