#!/usr/bin/env python3

import os
import re

def is_valid_tree_structure(text):
    """Validate if the input text follows the tree structure format."""
    if not text.strip():
        return False
    
    lines = text.splitlines()
    
    # Check if there's at least a root directory
    if not lines[0].strip().endswith('/'):
        return False
    
    # Define valid tree characters
    tree_chars = {'│', '├', '└', '─'}
    
    # Check each line for valid format
    for i, line in enumerate(lines[1:], 1):
        stripped = line.lstrip()
        if not stripped:  # Skip empty lines
            continue
            
        # Check if line starts with valid tree characters or spaces
        leading_chars = set(line[:len(line) - len(stripped)])
        invalid_chars = leading_chars - tree_chars - {' '}
        if invalid_chars:
            return False
        
        # Check if the line has at least one non-tree character (file/folder name)
        content = line.lstrip(' │├└─')
        if not content:
            return False
            
        # Check for valid tree structure pattern
        if not re.match(r'^[\s│├└─]*[^\s│├└─]', line):
            return False
    
    return True

def count_depth(line):
    """Count the depth of a line based on tree characters."""
    space_count = 0
    for char in line:
        if char == ' ':
            space_count += 1
        elif char in ['│', '├', '└']:
            space_count += 1
        elif char == '─':
            continue
        else:
            break
    return space_count // 2

def create_structure(tree_text):
    """Create directory structure from tree output."""
    lines = [line.rstrip() for line in tree_text.splitlines() if line.strip()]
    
    # Get root directory
    root = lines[0].rstrip('/')
    
    # Create root if it doesn't exist
    if not os.path.exists(root):
        os.makedirs(root)
        print(f"Created directory: {root}")

    # Keep track of the current path components
    paths = {-1: []}  # depth -> path components
    last_depth = -1
    
    for line in lines[1:]:
        # Get depth and name
        depth = count_depth(line)
        name = line.lstrip(' │├└─').rstrip()
        is_dir = name.endswith('/')
        
        if is_dir:
            name = name.rstrip('/')
        
        # Update paths dictionary for this depth
        if depth <= last_depth:
            # Remove deeper paths when we go up or stay at same level
            for d in list(paths.keys()):
                if d >= depth:
                    paths.pop(d)
        
        # Get current path components
        current_path_components = []
        for d in range(depth):
            if d in paths:
                current_path_components.extend(paths[d])
        
        # Create full path
        full_path = os.path.join(root, *current_path_components, name)
        
        try:
            if is_dir:
                # Create directory
                os.makedirs(full_path, exist_ok=True)
                print(f"Created directory: {full_path}")
                # Store this directory name for this depth
                paths[depth] = [name]
            else:
                # Create file
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w') as f:
                    pass
                print(f"Created file: {full_path}")
        except Exception as e:
            print(f"Error creating {full_path}: {str(e)}")
        
        last_depth = depth

def main():
    print("Tree2File - Create directory structures from tree output")
    print("Please paste your tree structure below.")
    print("Enter an empty line twice to finish input:")
    print("-" * 50)
    
    # Collect input lines until user enters an empty line twice
    lines = []
    empty_line_count = 0
    
    while empty_line_count < 2:
        try:
            line = input()
            if not line.strip():
                empty_line_count += 1
            else:
                empty_line_count = 0
                lines.append(line)
        except EOFError:
            break
    
    tree_structure = '\n'.join(lines)
    
    if not tree_structure.strip():
        print("\nError: No input provided.")
        return
    
    if not is_valid_tree_structure(tree_structure):
        print("\nError: Invalid tree structure format.")
        print("Make sure:")
        print("- The first line is a root directory ending with '/'")
        print("- Each line uses proper tree characters (│, ├, └, ─)")
        print("- Each line contains a valid file or directory name")
        return
    
    try:
        create_structure(tree_structure)
        print("\nDirectory structure created successfully!")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()