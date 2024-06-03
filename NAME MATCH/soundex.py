import re
# Modified Soundex Function
def modified_soundex(name):
    soundex_dict = {
        '0': 'aeiouvyhw', 
        '1': 'kgqc', 
        '2': 'cj', 
        '3': 'td', 
        '4': 'jzx', 
        '5': 'm', 
        '6': 'pfbwv', 
        '7': 'l', 
        '8': 's', 
        '9': 'r', 
        '!': 'n'
    }
    
    name = re.sub(r'[aeiouvyhw]', '0', name)
    name = re.sub(r'[kgqc]', '1', name)
    name = re.sub(r'[cj]', '2', name)
    name = re.sub(r'[td]', '3', name)
    name = re.sub(r'[jzx]', '4', name)
    name = re.sub(r'[m]', '5', name)
    name = re.sub(r'[pfbwv]', '6', name)
    name = re.sub(r'[l]', '7', name)
    name = re.sub(r'[s]', '8', name)
    name = re.sub(r'[r]', '9', name)
    name = re.sub(r'[n]', '!', name)
    
    # Remove duplicate adjacent digits
    name = re.sub(r'(\d)\1+', r'\1', name)
    
    return name

def remove_common_soundex(soundex1, soundex2):
    common_parts = set(soundex1) & set(soundex2)
    soundex1 = [part for part in soundex1 if part not in common_parts]
    soundex2 = [part for part in soundex2 if part not in common_parts]
    return soundex1, soundex2

# Example usage:
name1 = "Ram Manohar Singh"
name2 = "Syam Manohar Singh"


# Generate Modified Soundex
soundex1 = modified_soundex(name1)
soundex2 = modified_soundex(name2)

# Remove Common Soundex Encodings
soundex1, soundex2 = remove_common_soundex(soundex1, soundex2)

print("Name 1 after processing:", name1)
print("Name 2 after processing:", name2)
print("Soundex 1:", soundex1)
print("Soundex 2:", soundex2)