import numpy as np

# Load the .npz file
data = np.load('/home/lde/yuhang/ITSC/utilities/evo_results/error_array.npz')

# Access the contents of the file
# The .npz file acts like a dictionary
# You can use the keys to access the arrays stored in the file

# Print the keys
print(data.keys())

# Access a specific array by key
array1 = data['array1_key']
array2 = data['array2_key']

# Use the loaded arrays as needed
# For example, print the shape of array1
print(array1.shape)

# Close the .npz file after you're done
data.close()