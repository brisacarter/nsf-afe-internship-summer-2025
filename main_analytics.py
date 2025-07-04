
# Author: Brisa Carter

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import numpy as np
import sys
import os
from collections import Counter

def load_and_clean_data(year_range='25'):
    """Load and clean the video game sales data"""
    try:
        # Try different possible file paths
        possible_files = ['vgchartz-2024.csv', 'vgsales.csv']
        df = None
        used_file = None
        
        for file_path in possible_files:
            if os.path.exists(file_path):
                print(f"Loading data from {file_path}...")
                df = pd.read_csv(file_path)
                used_file = file_path
                break
        
        if df is None:
            raise FileNotFoundError("No CSV file found. Please ensure vgchartz-2024.csv or vgsales.csv exists.")
        
        print(f"Loaded {len(df)} records from {used_file}")
        
        # Determine year range based on parameter
        if year_range == '44':
            start_year = 1980
            year_desc = "past 44 years (1980-2024)"
        else:  # default to 5 years
            start_year = 2019
            year_desc = "past 5 years (2019-2024)"
        
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
        print(f"Available columns: {available_cols}")
        
        return df, available_cols
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None

def analyze_sales_by_genre(df, available_cols):
    """Analyze video game sales by genre"""
    print("\n" + "="*50)
    print("SALES BY GENRE ANALYSIS")
    print("="*50)
    
    # Determine the correct column names
    genre_col = next((col for col in ['Genre', 'genre'] if col in available_cols), None)
    sales_col = next((col for col in ['Global_Sales', 'total_sales', 'global_sales'] if col in available_cols), None)
    
    if not genre_col or not sales_col:
        print("Required columns not found for genre analysis")
        return
    
    # Clean the data
    df_clean = df.dropna(subset=[genre_col, sales_col])
    df_clean[sales_col] = pd.to_numeric(df_clean[sales_col], errors='coerce')
    df_clean = df_clean.dropna(subset=[sales_col])
    
    # Group by Genre and sum sales
    genre_sales = df_clean.groupby(genre_col)[sales_col].sum().sort_values(ascending=False)
    
    print(f"\nTop 10 Genres by Global Sales:")
    for i, (genre, sales) in enumerate(genre_sales.head(10).items(), 1):
        print(f"{i:2d}. {genre:20s}: {sales:8.2f} million")
    
    # Create visualization
    plt.figure(figsize=(12, 8))
    top_genres = genre_sales.head(10)
    colors = plt.cm.Set3(range(len(top_genres)))
    
    bars = plt.bar(top_genres.index, top_genres.values, color=colors)
    
    plt.title('Top 10 Video Game Genres by Global Sales', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Genre', fontsize=12, fontweight='bold')
    plt.ylabel('Global Sales (millions)', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    
    # Add value labels on bars
    for bar, value in zip(bars, top_genres.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(top_genres.values)*0.01,
                f'{value:.1f}M', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.grid(True, alpha=0.3, axis='y')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.tight_layout()
    
    plt.savefig('genre_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\nGenre Analysis Summary:")
    print(f"Total genres analyzed: {len(genre_sales)}")
    print(f"Total global sales: {genre_sales.sum():.2f} million")
    print(f"Average sales per genre: {genre_sales.mean():.2f} million")



def analyze_platform_performance(df, available_cols):
    """Analyze sales by gaming platform/console"""
    print("\n" + "="*50)
    print("PLATFORM PERFORMANCE ANALYSIS")
    print("="*50)
    
    # Determine platform and sales columns
    platform_col = next((col for col in ['Platform', 'platform', 'console'] if col in available_cols), None)
    sales_col = next((col for col in ['Global_Sales', 'total_sales', 'global_sales'] if col in available_cols), None)
    
    if not platform_col or not sales_col:
        print("Required columns not found for platform analysis")
        return
    
    # Clean the data
    df_clean = df.dropna(subset=[platform_col, sales_col])
    df_clean[sales_col] = pd.to_numeric(df_clean[sales_col], errors='coerce')
    df_clean = df_clean.dropna(subset=[sales_col])
    
    # Group by platform
    platform_sales = df_clean.groupby(platform_col)[sales_col].sum().sort_values(ascending=False)
    platform_counts = df_clean.groupby(platform_col).size().sort_values(ascending=False)
    
    print(f"\nTop 15 Platforms by Global Sales:")
    for i, (platform, sales) in enumerate(platform_sales.head(15).items(), 1):
        games_count = platform_counts[platform]
        avg_sales = sales / games_count
        print(f"{i:2d}. {platform:8s}: {sales:8.2f}M total | {games_count:4d} games | {avg_sales:.2f}M avg")
    
    # Create visualization
    plt.figure(figsize=(14, 10))
    
    # Top platforms by total sales
    plt.subplot(2, 2, 1)
    top_platforms = platform_sales.head(12)
    bars = plt.bar(range(len(top_platforms)), top_platforms.values, color=plt.cm.tab20(range(len(top_platforms))))
    plt.title('Top 12 Platforms by Total Sales', fontsize=12, fontweight='bold')
    plt.xlabel('Platform', fontsize=10)
    plt.ylabel('Total Sales (millions)', fontsize=10)
    plt.xticks(range(len(top_platforms)), top_platforms.index, rotation=45, ha='right')
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, top_platforms.values)):
        plt.text(i, value + max(top_platforms.values)*0.01, f'{value:.0f}M', 
                ha='center', va='bottom', fontsize=8)
    
    # Top platforms by game count
    plt.subplot(2, 2, 2)
    top_counts = platform_counts.head(12)
    bars = plt.bar(range(len(top_counts)), top_counts.values, color=plt.cm.tab20c(range(len(top_counts))))
    plt.title('Top 12 Platforms by Game Count', fontsize=12, fontweight='bold')
    plt.xlabel('Platform', fontsize=10)
    plt.ylabel('Number of Games', fontsize=10)
    plt.xticks(range(len(top_counts)), top_counts.index, rotation=45, ha='right')
    
    # Average sales per game
    plt.subplot(2, 2, 3)
    avg_sales_per_platform = (platform_sales / platform_counts).sort_values(ascending=False).head(12)
    bars = plt.bar(range(len(avg_sales_per_platform)), avg_sales_per_platform.values, 
                  color=plt.cm.Pastel1(range(len(avg_sales_per_platform))))
    plt.title('Top 12 Platforms by Average Sales per Game', fontsize=12, fontweight='bold')
    plt.xlabel('Platform', fontsize=10)
    plt.ylabel('Average Sales (millions)', fontsize=10)
    plt.xticks(range(len(avg_sales_per_platform)), avg_sales_per_platform.index, rotation=45, ha='right')
    
    # Platform market share (top 10)
    plt.subplot(2, 2, 4)
    top_10_platforms = platform_sales.head(10)
    plt.pie(top_10_platforms.values, labels=top_10_platforms.index, autopct='%1.1f%%',
           colors=plt.cm.tab20(range(len(top_10_platforms))))
    plt.title('Market Share - Top 10 Platforms', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('platform_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\nPlatform Analysis Summary:")
    print(f"Total platforms analyzed: {len(platform_sales)}")
    print(f"Most successful platform: {platform_sales.index[0]} ({platform_sales.iloc[0]:.2f}M)")
    print(f"Platform with most games: {platform_counts.index[0]} ({platform_counts.iloc[0]} games)")

def analyze_publisher_rankings(df, available_cols):
    """Analyze top publishers by sales performance"""
    print("\n" + "="*50)
    print("PUBLISHER RANKINGS ANALYSIS")
    print("="*50)
    
    # Determine publisher and sales columns
    publisher_col = next((col for col in ['Publisher', 'publisher'] if col in available_cols), None)
    sales_col = next((col for col in ['Global_Sales', 'total_sales', 'global_sales'] if col in available_cols), None)
    
    if not publisher_col or not sales_col:
        print("Required columns not found for publisher analysis")
        return
    
    # Clean the data
    df_clean = df.dropna(subset=[publisher_col, sales_col])
    df_clean[sales_col] = pd.to_numeric(df_clean[sales_col], errors='coerce')
    df_clean = df_clean.dropna(subset=[sales_col])
    
    # Group by publisher
    publisher_sales = df_clean.groupby(publisher_col)[sales_col].sum().sort_values(ascending=False)
    publisher_counts = df_clean.groupby(publisher_col).size().sort_values(ascending=False)
    
    print(f"\nTop 20 Publishers by Global Sales:")
    for i, (publisher, sales) in enumerate(publisher_sales.head(20).items(), 1):
        games_count = publisher_counts[publisher]
        avg_sales = sales / games_count
        print(f"{i:2d}. {publisher:25s}: {sales:8.2f}M | {games_count:4d} games | {avg_sales:.2f}M avg")
    
    # Create visualization
    plt.figure(figsize=(16, 10))
    
    # Top publishers by total sales
    plt.subplot(2, 2, 1)
    top_publishers = publisher_sales.head(15)
    bars = plt.bar(range(len(top_publishers)), top_publishers.values, 
                  color=plt.cm.tab20(range(len(top_publishers))))
    plt.title('Top 15 Publishers by Total Sales', fontsize=12, fontweight='bold')
    plt.xlabel('Publisher', fontsize=10)
    plt.ylabel('Total Sales (millions)', fontsize=10)
    plt.xticks(range(len(top_publishers)), 
              [name[:15] + '...' if len(name) > 15 else name for name in top_publishers.index], 
              rotation=45, ha='right')
    
    # Publishers by game count
    plt.subplot(2, 2, 2)
    top_counts = publisher_counts.head(15)
    bars = plt.bar(range(len(top_counts)), top_counts.values, 
                  color=plt.cm.tab20c(range(len(top_counts))))
    plt.title('Top 15 Publishers by Game Count', fontsize=12, fontweight='bold')
    plt.xlabel('Publisher', fontsize=10)
    plt.ylabel('Number of Games', fontsize=10)
    plt.xticks(range(len(top_counts)), 
              [name[:15] + '...' if len(name) > 15 else name for name in top_counts.index], 
              rotation=45, ha='right')
    
    # Average sales per game
    plt.subplot(2, 2, 3)
    avg_sales_per_publisher = (publisher_sales / publisher_counts).sort_values(ascending=False)
    # Filter publishers with at least 5 games for meaningful average
    qualified_publishers = avg_sales_per_publisher[publisher_counts >= 5].head(15)
    bars = plt.bar(range(len(qualified_publishers)), qualified_publishers.values, 
                  color=plt.cm.Pastel1(range(len(qualified_publishers))))
    plt.title('Top 15 Publishers by Avg Sales/Game (5+ games)', fontsize=12, fontweight='bold')
    plt.xlabel('Publisher', fontsize=10)
    plt.ylabel('Average Sales (millions)', fontsize=10)
    plt.xticks(range(len(qualified_publishers)), 
              [name[:15] + '...' if len(name) > 15 else name for name in qualified_publishers.index], 
              rotation=45, ha='right')
    
    # Market share pie chart
    plt.subplot(2, 2, 4)
    top_10_publishers = publisher_sales.head(10)
    others_sales = publisher_sales.iloc[10:].sum()
    
    # Add "Others" category
    pie_data = list(top_10_publishers.values) + [others_sales]
    pie_labels = list(top_10_publishers.index) + ['Others']
    
    plt.pie(pie_data, labels=[label[:12] + '...' if len(label) > 12 else label for label in pie_labels], 
           autopct='%1.1f%%', colors=plt.cm.tab20(range(len(pie_data))))
    plt.title('Publisher Market Share', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('publisher_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\nPublisher Analysis Summary:")
    print(f"Total publishers analyzed: {len(publisher_sales)}")
    print(f"Top publisher: {publisher_sales.index[0]} ({publisher_sales.iloc[0]:.2f}M total sales)")
    print(f"Most prolific publisher: {publisher_counts.index[0]} ({publisher_counts.iloc[0]} games)")



def run_all_analysis_with_range(year_range='5'):
    """Run all analysis types with specified year range"""
    year_desc = {
        '44': '1980-2024',
        '5': '2019-2024'
    }.get(year_range, '2019-2024')
    
    print(f"VIDEO GAME SALES COMPREHENSIVE ANALYSIS ({year_desc})")
    print("=" * 60)
    
    # Load data
    df, available_cols = load_and_clean_data(year_range)
    if df is None:
        return
    
    print(f"Dataset loaded successfully with {len(df)} records")
    print(f"Columns available: {', '.join(available_cols)}")
    
    # Run all analyses
    analyze_sales_by_genre(df, available_cols)
    analyze_platform_performance(df, available_cols)
    analyze_publisher_rankings(df, available_cols)

def run_all_analysis():
    """Run all analysis types with default 5-year range"""
    run_all_analysis_with_range('5')
    
    # Create a combined summary visualization
    plt.figure(figsize=(16, 10))
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Montserrat', 'Arial', 'DejaVu Sans']
    
    # Set background color to match app
    fig = plt.gcf()
    fig.patch.set_facecolor('#f8f9fa')
    
    # Main content with app-style colors
    main_text = ('Comprehensive Video Game Sales Analysis Complete!\n\n' +
                'Individual analysis charts have been generated:\n' +
                '• Genre Analysis: genre_analysis.png\n' +
                '• Regional Breakdown: regional_analysis.png\n' +
                '• Platform Performance: platform_analysis.png\n' +
                '• Publisher Rankings: publisher_analysis.png\n' +
                '• Historical Trends: historical_analysis.png\n\n' +
                'Check each individual chart for detailed insights.')
    
    plt.text(0.5, 0.5, main_text,
             fontsize=16, ha='center', va='center', 
             color='#333333', fontweight='normal', linespacing=1.6,
             bbox=dict(boxstyle="round,pad=30", facecolor="#e3e3e3", 
                      edgecolor="#455d7a", linewidth=2))
    
    plt.axis('off')
    
    # Title with app colors
    plt.title('Video Game Sales Analysis Summary (1999-2024)', 
              fontsize=24, fontweight='bold', pad=30, 
              color='#455d7a', fontfamily='sans-serif')
    
    # Add subtle branding footer
    plt.figtext(0.5, 0.05, 'By Brisa Carter | Powered by Python & Machine Learning', 
                fontsize=12, ha='center', va='bottom', 
                color='#666666', style='italic')
    
    plt.savefig('all_analysis_summary.png', dpi=300, bbox_inches='tight', 
                facecolor='#f8f9fa', edgecolor='none')
    plt.close()
    
    print("\n" + "="*60)
    print("COMPREHENSIVE ANALYSIS COMPLETE!")
    print("="*60)
    print("All individual analysis charts have been generated.")

if __name__ == "__main__":
    year_range = '5'  # default
    analysis_type = 'all'  # default
    
    if len(sys.argv) > 1:
        analysis_type = sys.argv[1].lower()
    
    if len(sys.argv) > 2:
        year_range = sys.argv[2]
    
    # Load data once with specified year range
    df, available_cols = load_and_clean_data(year_range)
    if df is None:
        sys.exit(1)
    
    if analysis_type == 'genre':
        analyze_sales_by_genre(df, available_cols)
    elif analysis_type == 'platform':
        analyze_platform_performance(df, available_cols)
    elif analysis_type == 'publisher':
        analyze_publisher_rankings(df, available_cols)
    elif analysis_type == 'all':
        run_all_analysis_with_range(year_range)
    else:
        print(f"Unknown analysis type: {analysis_type}")
        print("Available types: genre, platform, publisher, all")
