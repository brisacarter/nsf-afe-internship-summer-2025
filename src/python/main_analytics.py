
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sys
import os

def load_data():
    """Load the video game sales data"""
    try:
        # Try different possible file paths
        possible_files = ['data/vgchartz-2024.csv', 'data/vgsales.csv']
        
        for file_path in possible_files:
            if os.path.exists(file_path):
                print(f"Loading data from {file_path}")
                df = pd.read_csv(file_path)
                print(f"Data loaded successfully. Shape: {df.shape}")
                print(f"Columns: {list(df.columns)}")
                
                # Handle different column name variations
                if 'Global_Sales' not in df.columns and 'Global Sales' in df.columns:
                    df['Global_Sales'] = df['Global Sales']
                if 'Global_Sales' not in df.columns and 'GlobalSales' in df.columns:
                    df['Global_Sales'] = df['GlobalSales']
                
                return df
        
        print("No data file found!")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def filter_data_by_year(df, year_range):
    """Filter data based on year range"""
    if 'Year' not in df.columns:
        print("Year column not found in data")
        return df
    
    # Convert year range to integer
    years = int(year_range)
    current_year = 2024
    start_year = current_year - years + 1
    
    print(f"Filtering data from {start_year} to {current_year}")
    
    # Filter data
    filtered_df = df[(df['Year'] >= start_year) & (df['Year'] <= current_year)]
    print(f"Filtered data shape: {filtered_df.shape}")
    
    return filtered_df

def analyze_by_genre(df, year_range='25'):
    """Analyze sales by genre"""
    print(f"\n=== GENRE ANALYSIS (Past {year_range} Years) ===")
    
    # Filter data by year range
    df_filtered = filter_data_by_year(df, year_range)
    
    if df_filtered.empty:
        print("No data available for the specified year range")
        return
    
    # Group by genre and sum global sales
    genre_sales = df_filtered.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False)
    
    print("\nTop Genres by Global Sales:")
    for genre, sales in genre_sales.head(10).items():
        print(f"{genre}: ${sales:.2f}M")
    
    # Create visualization
    plt.figure(figsize=(12, 8))
    colors = plt.cm.Set3(np.linspace(0, 1, len(genre_sales)))
    bars = plt.bar(genre_sales.index, genre_sales.values, color=colors)
    
    plt.title(f'Video Game Sales by Genre (Past {year_range} Years)\nTotal Sales in Millions USD', fontsize=16, fontweight='bold')
    plt.xlabel('Genre', fontsize=12)
    plt.ylabel('Global Sales (Millions USD)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    # Add value labels on bars
    for bar, value in zip(bars, genre_sales.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'${value:.1f}M', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.grid(axis='y', alpha=0.3)
    plt.savefig('src/assets/genre_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\nGenre analysis chart saved as 'src/assets/genre_analysis.png'")

def analyze_by_platform(df, year_range='25'):
    """Analyze sales by platform"""
    print(f"\n=== PLATFORM ANALYSIS (Past {year_range} Years) ===")
    
    # Filter data by year range
    df_filtered = filter_data_by_year(df, year_range)
    
    if df_filtered.empty:
        print("No data available for the specified year range")
        return
    
    # Group by platform and sum global sales
    platform_sales = df_filtered.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=False)
    
    print("\nTop Platforms by Global Sales:")
    for platform, sales in platform_sales.head(15).items():
        print(f"{platform}: ${sales:.2f}M")
    
    # Create visualization
    plt.figure(figsize=(15, 10))
    colors = plt.cm.viridis(np.linspace(0, 1, len(platform_sales.head(15))))
    bars = plt.bar(platform_sales.head(15).index, platform_sales.head(15).values, color=colors)
    
    plt.title(f'Video Game Sales by Platform (Past {year_range} Years)\nTop 15 Platforms - Total Sales in Millions USD', fontsize=16, fontweight='bold')
    plt.xlabel('Platform', fontsize=12)
    plt.ylabel('Global Sales (Millions USD)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    # Add value labels on bars
    for bar, value in zip(bars, platform_sales.head(15).values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'${value:.1f}M', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    plt.tight_layout()
    plt.grid(axis='y', alpha=0.3)
    plt.savefig('src/assets/platform_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\nPlatform analysis chart saved as 'src/assets/platform_analysis.png'")

def analyze_by_publisher(df, year_range='25'):
    """Analyze sales by publisher"""
    print(f"\n=== PUBLISHER ANALYSIS (Past {year_range} Years) ===")
    
    # Filter data by year range
    df_filtered = filter_data_by_year(df, year_range)
    
    if df_filtered.empty:
        print("No data available for the specified year range")
        return
    
    # Group by publisher and sum global sales
    publisher_sales = df_filtered.groupby('Publisher')['Global_Sales'].sum().sort_values(ascending=False)
    
    print("\nTop Publishers by Global Sales:")
    for publisher, sales in publisher_sales.head(15).items():
        print(f"{publisher}: ${sales:.2f}M")
    
    # Create visualization
    plt.figure(figsize=(15, 10))
    colors = plt.cm.plasma(np.linspace(0, 1, len(publisher_sales.head(15))))
    bars = plt.bar(publisher_sales.head(15).index, publisher_sales.head(15).values, color=colors)
    
    plt.title(f'Video Game Sales by Publisher (Past {year_range} Years)\nTop 15 Publishers - Total Sales in Millions USD', fontsize=16, fontweight='bold')
    plt.xlabel('Publisher', fontsize=12)
    plt.ylabel('Global Sales (Millions USD)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    # Add value labels on bars
    for bar, value in zip(bars, publisher_sales.head(15).values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'${value:.1f}M', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    plt.tight_layout()
    plt.grid(axis='y', alpha=0.3)
    plt.savefig('src/assets/publisher_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\nPublisher analysis chart saved as 'src/assets/publisher_analysis.png'")

def create_summary_analysis(df, year_range='25'):
    """Create a comprehensive summary analysis"""
    print(f"\n=== COMPREHENSIVE SUMMARY ANALYSIS (Past {year_range} Years) ===")
    
    # Filter data by year range
    df_filtered = filter_data_by_year(df, year_range)
    
    if df_filtered.empty:
        print("No data available for the specified year range")
        return
    
    # Calculate summary statistics
    total_sales = df_filtered['Global_Sales'].sum()
    avg_sales = df_filtered['Global_Sales'].mean()
    total_games = len(df_filtered)
    
    print(f"Total Global Sales: ${total_sales:.2f}M")
    print(f"Average Sales per Game: ${avg_sales:.2f}M")
    print(f"Total Number of Games: {total_games}")
    
    # Create a comprehensive summary plot
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 15))
    fig.suptitle(f'Video Game Sales Summary Analysis (Past {year_range} Years)', fontsize=20, fontweight='bold')
    
    # 1. Top Genres
    genre_sales = df_filtered.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False).head(8)
    colors1 = plt.cm.Set3(np.linspace(0, 1, len(genre_sales)))
    bars1 = ax1.bar(genre_sales.index, genre_sales.values, color=colors1)
    ax1.set_title('Top 8 Genres by Sales', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Genre')
    ax1.set_ylabel('Global Sales (Millions USD)')
    ax1.tick_params(axis='x', rotation=45)
    for bar, value in zip(bars1, genre_sales.values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'${value:.1f}M', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # 2. Top Platforms
    platform_sales = df_filtered.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=False).head(10)
    colors2 = plt.cm.viridis(np.linspace(0, 1, len(platform_sales)))
    bars2 = ax2.bar(platform_sales.index, platform_sales.values, color=colors2)
    ax2.set_title('Top 10 Platforms by Sales', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Platform')
    ax2.set_ylabel('Global Sales (Millions USD)')
    ax2.tick_params(axis='x', rotation=45)
    for bar, value in zip(bars2, platform_sales.values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'${value:.1f}M', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # 3. Top Publishers
    publisher_sales = df_filtered.groupby('Publisher')['Global_Sales'].sum().sort_values(ascending=False).head(10)
    colors3 = plt.cm.plasma(np.linspace(0, 1, len(publisher_sales)))
    bars3 = ax3.bar(publisher_sales.index, publisher_sales.values, color=colors3)
    ax3.set_title('Top 10 Publishers by Sales', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Publisher')
    ax3.set_ylabel('Global Sales (Millions USD)')
    ax3.tick_params(axis='x', rotation=45)
    for bar, value in zip(bars3, publisher_sales.values):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'${value:.1f}M', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # 4. Sales Distribution
    ax4.hist(df_filtered['Global_Sales'], bins=50, color='skyblue', alpha=0.7, edgecolor='black')
    ax4.set_title('Distribution of Game Sales', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Global Sales (Millions USD)')
    ax4.set_ylabel('Number of Games')
    ax4.axvline(avg_sales, color='red', linestyle='--', linewidth=2, label=f'Average: ${avg_sales:.2f}M')
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig('src/assets/all_analysis_summary.png', dpi=300, bbox_inches='tight', 
                facecolor='#f8f9fa', edgecolor='none')
    plt.close()
    
    print(f"\nComprehensive summary analysis saved as 'src/assets/all_analysis_summary.png'")

def main():
    """Main function to run the analysis"""
    # Get command line arguments
    if len(sys.argv) > 1:
        analysis_type = sys.argv[1]
    else:
        analysis_type = 'genre'
    
    if len(sys.argv) > 2:
        year_range = sys.argv[2]
    else:
        year_range = '25'
    
    print(f"Running {analysis_type} analysis for the past {year_range} years...")
    
    # Load data
    df = load_data()
    if df is None:
        print("Failed to load data. Exiting.")
        return
    
    # Set matplotlib style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Run specific analysis based on type
    if analysis_type == 'genre':
        analyze_by_genre(df, year_range)
    elif analysis_type == 'platform':
        analyze_by_platform(df, year_range)
    elif analysis_type == 'publisher':
        analyze_by_publisher(df, year_range)
    elif analysis_type == 'summary':
        create_summary_analysis(df, year_range)
    else:
        print(f"Unknown analysis type: {analysis_type}")
        print("Available types: genre, platform, publisher, summary")

if __name__ == "__main__":
    main()
