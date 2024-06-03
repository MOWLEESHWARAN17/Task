import random
import numpy as np
import pandas as pd

# List of common names for generating the dataset
base_names = [
    "Ram Manohar Singh", "Vinod Kumar", "Jakir Hussain", "Syam Manohar Singh",
    "Vinit Kumar", "Javed Akhtar", "Amit Sharma", "Ravi Patel", "Rajesh Gupta",
    "Suresh Mehta", "Manoj Verma", "Anil Yadav", "Deepak Chauhan", "Nitin Bhardwaj",
    "Sunil Kapoor", "Mahesh Rathod", "Karan Singh", "Vikram Rathore", "Rakesh Rao",
    "Arun Joshi"
]

def generate_variation(name):
    variations = [
        lambda x: x.lower(),
        lambda x: x.upper(),
        lambda x: x.replace('a', '@').replace('o', '0').replace('i', '1').replace('e', '3'),
        lambda x: re.sub(r'(\w)\1+', r'\1', x),
        lambda x: re.sub(r'\b(\w)', lambda m: m.group().upper(), x)
    ]
    variation_func = random.choice(variations)
    return variation_func(name)

def generate_dataset(base_names, num_pairs=10000):
    names1 = []
    names2 = []
    labels = []
    
    # Generate matching pairs
    for _ in range(num_pairs // 2):
        name = random.choice(base_names)
        variation = generate_variation(name)
        names1.append(name)
        names2.append(variation)
        labels.append(1)
    
    # Generate non-matching pairs
    for _ in range(num_pairs // 2):
        name1 = random.choice(base_names)
        name2 = random.choice(base_names)
        while name1 == name2:
            name2 = random.choice(base_names)
        names1.append(name1)
        names2.append(name2)
        labels.append(0)
    
    return pd.DataFrame({
        'name1': names1,
        'name2': names2,
        'label': labels
    })

# Generate a large dataset
large_dataset = generate_dataset(base_names, num_pairs=100000)

# Save to CSV
large_dataset.to_csv('synthetic_name_matching_dataset.csv', index=False)

print("Dataset generated and saved to 'synthetic_name_matching_dataset.csv'.")
