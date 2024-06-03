import re

def clean_names(name):
    # Remove numeric words and special characters
    cleaned_name = re.sub(r'\d+', '', name)  # Remove numeric words
    cleaned_name = re.sub(r'[^\w\s]', '', cleaned_name)  # Remove special characters except spaces
    
    # Convert all characters to lowercase
    cleaned_name = cleaned_name.lower()
    
    # Stop-word Removal
    stopwords = ['smt', 'shri', 'mr', 'dr', 'ms']  # Define stop-words
    for word in stopwords:
        cleaned_name = cleaned_name.replace(word, '')
    
    # Common word removal
    common_words = ['bhai', 'bhau', 'bhoi', 'bai', 'kumar', 'kumr', 'kmr', 
                    'ben', 'dei', 'devi', 'debi', 'kumaar']  # Define common words
    for word in common_words:
        cleaned_name = cleaned_name.replace(word, '')
    
    # Common suffix removal from word
    common_suffixes = ['saheb', 'kumar', 'kumaar', 'bhai', 'bhau', 'bai', 'ben', 'bai', 'sab']  # Define common suffixes
    for suffix in common_suffixes:
        cleaned_name = cleaned_name.replace(suffix, '')
    
    return cleaned_name.strip()  # Strip leading and trailing spaces

# Example usage:
name1 = "Dr. Ravi Kumar Singh"
name2 = "Shri Mohanbhai Patel"
cleaned_name1 = clean_names(name1)
cleaned_name2 = clean_names(name2)
print("Cleaned Name 1:", cleaned_name1)
print("Cleaned Name 2:", cleaned_name2)
