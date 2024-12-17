def generate_diagram(path_counts, verbose=False):
    """
    Generate an ASCII tree diagram from folder and file commit counts.
    
    Args:
        path_counts (dict): Dictionary mapping paths (folders/files) to commit counts
        verbose (bool): If True, include files in the diagram. If False, only show folders
        
    Returns:
        str: ASCII tree diagram as a string
    """
    if not path_counts:
        return "root/"

    # Sort paths to ensure consistent ordering
    sorted_paths = sorted(path_counts.items(), key=lambda x: x[0])
    
    # Filter out files if not in verbose mode
    if not verbose:
        sorted_paths = [(path, count) for path, count in sorted_paths 
                       if '.' not in path.split('/')[-1]]
    
    tree_lines = ["root/"]
    last_parts = []
    
    for path, count in sorted_paths:
        parts = path.split('/')
        
        # Skip the path if it's a file and we're not in verbose mode
        if not verbose and '.' in parts[-1]:
            continue
            
        # Calculate common prefix length with last path
        common_prefix_len = 0
        for i, (curr, last) in enumerate(zip(parts, last_parts)):
            if curr != last:
                break
            common_prefix_len = i + 1
        
        # Add new branches
        for i, part in enumerate(parts[common_prefix_len:], common_prefix_len):
            prefix = "    " * i
            is_last = (i == len(parts) - 1)
            is_file = '.' in part
            
            if is_last:
                branch = "└── "
            else:
                branch = "├── "
                
            if is_file:
                tree_lines.append(f"{prefix}{branch}{part} ({count} commits)")
            else:
                tree_lines.append(f"{prefix}{branch}{part}/ ({count} commits)")
        
        last_parts = parts
    
    return "\n".join(tree_lines)
