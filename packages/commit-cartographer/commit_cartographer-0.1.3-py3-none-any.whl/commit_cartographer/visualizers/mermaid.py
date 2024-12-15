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

def generate_diagram(folder_counts):
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
