def generate_diagram(folder_counts):
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
