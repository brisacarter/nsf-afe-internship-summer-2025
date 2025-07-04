Update data file paths and image save location
Replacing
<old_str>
# Try different possible file paths
        possible_files = ['vgchartz-2024.csv', 'vgsales.csv']
</old_str>
with
<new_str>
# Try different possible file paths
        possible_files = ['data/vgchartz-2024.csv', 'data/vgsales.csv']
</new_str>
Update data file paths and image save location
Replacing
<old_str>
# Try different possible file paths
        possible_files = ['vgchartz-2024.csv', 'vgsales.csv']
</old_str>
with
<new_str>
# Try different possible file paths
        possible_files = ['data/vgchartz-2024.csv', 'data/vgsales.csv']
</new_str>
Update image save path
Replacing
<old_str>
# Save the plot
        plt.savefig('sales_analysis.png', dpi=300, bbox_inches='tight')
        print("Plot saved as 'sales_analysis.png'")
</old_str>
with
<new_str>
# Save the plot
        plt.savefig('src/assets/sales_analysis.png', dpi=300, bbox_inches='tight')
        print("Plot saved as 'src/assets/sales_analysis.png'")
</new_str>