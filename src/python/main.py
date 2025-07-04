# Load and clean data from the existing CSV file
        df = pd.read_csv('data/vgchartz-2024.csv')
# Save the plot as an image file so it can be viewed in Replit
        plt.savefig('src/assets/sales_prediction.png', dpi=300, bbox_inches='tight')
        print(f"\nPlot saved as 'src/assets/sales_prediction.png'")
# Load and clean data from the existing CSV file
        df = pd.read_csv('data/vgchartz-2024.csv')