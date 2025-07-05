# NSF-ATE Internship Summer 2025
#Author: Brisa Carter

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import os

def visualize_sales_analysis(year_range='25'):
    try:
        # Try different possible file paths
        possible_files = ['../../data/raw/vgchartz-2024.csv', '../../data/raw/vgsales.csv']
        df = None
        used_file = None
        
        for file_path in possible_files:
            if os.path.exists(file_path):
                print(f"Loading data from {file_path}...")
                df = pd.read_csv(file_path)
                used_file = file_path
                break
        
        if df is None:
            print("Error: No CSV file found. Please ensure ../../data/raw/vgchartz-2024.csv or ../../data/raw/vgsales.csv exists.")
            return
        
        print(f"Loaded {len(df)} records from {used_file}")
        
        # Determine year range based on parameter
        if year_range == '44':
            start_year = 1980
            year_desc = "past 44 years (1980-2024)"
        else:  # default to 8 years
            start_year = 2017
            year_desc = "past 8 years (2017-2024)"
        
        # Filter for selected year range
        if 'Year' in df.columns:
            df = df[df['Year'] >= start_year]
        elif 'release_date' in df.columns:
            df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
            df = df.dropna(subset=['release_date'])
            df['Year'] = df['release_date'].dt.year
            df = df[df['Year'] >= start_year]
        
        print(f"After filtering to {year_desc}: {len(df)} records")
        
        # Check available columns and adapt accordingly
        available_cols = df.columns.tolist()
        
        # Determine the correct column names based on what's available
        if 'Genre' in available_cols:
            genre_col = 'Genre'
        elif 'genre' in available_cols:
            genre_col = 'genre'
        else:
            print("No genre column found")
            return
            
        if 'Global_Sales' in available_cols:
            sales_col = 'Global_Sales'
        elif 'total_sales' in available_cols:
            sales_col = 'total_sales'
        elif 'global_sales' in available_cols:
            sales_col = 'global_sales'
        else:
            print("No sales column found")
            return
        
        # Clean the data efficiently
        df = df.dropna(subset=[genre_col, sales_col])
        df[sales_col] = pd.to_numeric(df[sales_col], errors='coerce')
        df = df.dropna(subset=[sales_col])
        
        print(f"After cleaning: {len(df)} records")
        
        # Group by Genre and sum sales
        genre_sales = df.groupby(genre_col)[sales_col].sum().sort_values(ascending=False)
        
        print("\nTop 10 Genres by Global Sales:")
        for genre, sales in genre_sales.head(10).items():
            print(f"{genre}: {sales:.2f} million")
        
        # Create visualization
        plt.figure(figsize=(14, 8))
        
        # Plot top 10 genres
        top_genres = genre_sales.head(10)
        colors = plt.cm.Set3(range(len(top_genres)))
        
        bars = plt.bar(top_genres.index, top_genres.values, color=colors)
        
        # Customize the plot
        plt.title('Top 10 Genres by Global Sales (1999-2024)', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Genre', fontsize=12, fontweight='bold')
        plt.ylabel('Global Sales (millions)', fontsize=12, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels on bars
        for bar, value in zip(bars, top_genres.values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{value:.1f}M', ha='center', va='bottom', fontweight='bold')
        
        plt.grid(True, alpha=0.3, axis='y')
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        
        plt.tight_layout()
        
        # Save the plot
        plt.savefig('../../public/analysis/sales_analysis.png', dpi=300, bbox_inches='tight')
        print("Plot saved as '../../public/analysis/sales_analysis.png'")
        
        # Additional analysis
        print("\nSummary Statistics:")
        print(f"Total genres analyzed: {len(genre_sales)}")
        print(f"Total global sales: {genre_sales.sum():.2f} million")
        print(f"Average sales per genre: {genre_sales.mean():.2f} million")
        
        # Platform analysis if available
        if 'Platform' in available_cols or 'platform' in available_cols or 'console' in available_cols:
            platform_col = next((col for col in ['Platform', 'platform', 'console'] if col in available_cols), None)
            if platform_col:
                platform_sales = df.groupby(platform_col)[sales_col].sum().sort_values(ascending=False)
                print("\nTop 10 Platforms by Global Sales:")
                for platform, sales in platform_sales.head(10).items():
                    print(f"{platform}: {sales:.2f} million")
        
        # Publisher analysis if available
        if 'Publisher' in available_cols or 'publisher' in available_cols:
            publisher_col = next((col for col in ['Publisher', 'publisher'] if col in available_cols), None)
            if publisher_col:
                publisher_sales = df.groupby(publisher_col)[sales_col].sum().sort_values(ascending=False)
                print("\nTop 10 Publishers by Global Sales:")
                for publisher, sales in publisher_sales.head(10).items():
                    print(f"{publisher}: {sales:.2f} million")
        
        plt.close()  # Close the figure to free memory
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Video Game Sales Analysis by Genre")
    print("=" * 40)
    visualize_sales_analysis()
