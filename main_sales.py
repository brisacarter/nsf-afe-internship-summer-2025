import pandas as pd
import matplotlib.pyplot as plt

def visualize_sales_by_genre(file_path):
    try:
        # Load the CSV data
        df = pd.read_csv(file_path)

        # Group by Genre and sum Global_Sales
        genre_sales = df.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False)

        # Plotting
        plt.figure(figsize=(12, 6))
        genre_sales.plot(kind='bar')
        plt.title('Total Global Sales by Genre')
        plt.xlabel('Genre')
        plt.ylabel('Global Sales (in millions)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")

# Ask user for CSV path
if __name__ == "__main__":
    path = input("Enter the full path to your CSV file: ")
    visualize_sales_by_genre(path)
