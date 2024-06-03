def remove_common_part(name1, name2):
    # Split names into parts
    parts1 = name1.split()
    parts2 = name2.split()
    
    # Find common parts
    common_parts = set(parts1) & set(parts2)
    
    # Remove common parts from each name
    name1 = ' '.join([part for part in parts1 if part not in common_parts])
    name2 = ' '.join([part for part in parts2 if part not in common_parts])
    
    return name1.strip(), name2.strip()

# Example usage:
name1 = "Ram Manohar Singh"
name2 = "Syam Manohar Singh"
name1, name2 = remove_common_part(name1, name2)
print("Name 1 after common part removal:", name1)
print("Name 2 after common part removal:", name2)
