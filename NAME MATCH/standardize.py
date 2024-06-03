import re

def standardize_names(name):
    # Replace e by I (इ, ई)
    name = name.replace('e', 'i').replace('E', 'I')
    
    # Replace adjacent similar characters by single character
    name = re.sub(r'(.)\1+', r'\1', name)
    
    # Replace Unigrams
    name = name.replace('v', 'w').replace('V', 'W')
    name = name.replace('j', 'z').replace('J', 'Z')
    name = name.replace('q', 'k').replace('Q', 'K')
    
    # Replace bigrams
    name = name.replace('ph', 'f').replace('Ph', 'F')
    name = name.replace('th', 't').replace('Th', 'T')
    name = name.replace('dh', 'd').replace('Dh', 'D')
    name = name.replace('sh', 's').replace('Sh', 'S')
    name = name.replace('ck', 'k').replace('Ck', 'K')
    name = name.replace('gh', 'g').replace('Gh', 'G')
    name = name.replace('kh', 'k').replace('Kh', 'K')
    name = name.replace('ch', 'c').replace('Ch', 'C')
    
    # Replace (ह)
    name = name.replace('ah', 'h').replace('Ah', 'H')
    
    # Remove 'a' if previous char is not i, o, u (consonant + a = consonant)
    name = re.sub(r'(?<![iou])a', '', name)
    
    return name.strip()  # Strip leading and trailing spaces

# Example usage:
name1 = "raaghaav"
name2 = "vinod"
standardized_name1 = standardize_names(name1)
standardized_name2 = standardize_names(name2)
print("Standardized Name 1:", standardized_name1)
print("Standardized Name 2:", standardized_name2)
