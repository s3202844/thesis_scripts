import ast
import matplotlib.pyplot as plt

# It seems the file contains two lists represented as strings. 
# I'll use the ast.literal_eval to safely evaluate the string as a Python expression
# and extract the two arrays.

# Extracting the arrays from the file contents
contents = open('experiment_10_subtract/aggregation.txt', 'r')
contents = contents.readlines()
arrays = [ast.literal_eval(line.strip()) for line in contents]

# Verifying the extracted data
arrays[0][:5], arrays[1][:5]  # Displaying the first few elements of each array for confirmation

# Unpacking the two arrays from the new file
new_first_array, new_second_array = arrays[0], arrays[1]

import numpy as np

# Correcting the error and generating x-coordinates evenly spaced between 5 and 100
x_coords = np.linspace(5, 100, 20)

# Adjusting the legend to include separate entries for each problem with corresponding colors and line type '-'
specific_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

# Creating a new figure and axis for the plot
fig, ax1 = plt.subplots()

# Creating a second y-axis for the second array
ax2 = ax1.twinx()

# Plotting the lines for each problem using the specified colors
for i in range(len(new_first_array)):
    label = f'Problem {i + 1}'
    ax1.plot(x_coords, new_first_array[i], linestyle='-', marker='o', color=specific_colors[i], label=label)
    ax2.plot(x_coords, new_second_array[i], linestyle='--', marker='x', color=specific_colors[i])

# Setting labels and tick parameters for the first y-axis
ax1.set_xlabel('Translation Limit')
ax1.set_ylabel('Number of Features Rejected by K-S Test', color='black')
ax1.tick_params(axis='y', labelcolor='black')

# Setting labels and tick parameters for the second y-axis
ax2.set_ylabel("Earth Mover's Distance", color='black')
ax2.tick_params(axis='y', labelcolor='black')

# Adding a title with bold 'x'
plt.title(r'Translation on $\bf{x}$')

# Creating legend elements for each problem with corresponding color and line type '-'
legend_elements = [plt.Line2D([0], [0], color=specific_colors[i], lw=2, linestyle='-', label=f'Problem {i+1}') for i in range(5)]
# Adding legend elements for K-S Test and Earth Mover's Distance
legend_elements.extend([
    plt.Line2D([0], [0], color='gray', lw=2, linestyle='-', marker='o', label='K-S Test'),
    plt.Line2D([0], [0], color='gray', lw=2, linestyle='--', label="Earth Mover's Distance")
])

fig.legend(handles=legend_elements, loc='upper right')

# Showing the plot with the adjusted legend
plt.savefig("aggregation_x_translation.png")
