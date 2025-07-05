# NSF-AFE Internship Summer 2025
#Author: Brisa Carter


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
from sklearn.linear_model import LinearRegression
import sys

def predict_future_sales(year_range='25'):
    try:
        # Load and clean data from the existing CSV file
        df = pd.read_csv('vgchartz-2024.csv')
        print(f"Loaded {len(df)} records from vgchartz-2024.csv")
        
        # Clean the data - remove rows with missing release_date or total_sales
        df = df.dropna(subset=['release_date', 'total_sales'])
        
        # Extract year from release_date
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
        df = df.dropna(subset=['release_date'])
        df['Year'] = df['release_date'].dt.year
        
        # Determine year range based on parameter
        if year_range == '44':
            start_year = 1980
            year_desc = "past 44 years (1980-2024)"
        elif year_range == '22':
            start_year = 2002
            year_desc = "past 22 years (2002-2024)"
        else:  # default to 8 years
            start_year = 2017
            year_desc = "past 8 years (2017-2024)"
        
        # Filter for selected year range
        df = df[(df['Year'] >= start_year) & (df['Year'] <= 2024)]
        
        print(f"After filtering to {year_desc}: {len(df)} records")
        
        # Convert total_sales to numeric
        df['total_sales'] = pd.to_numeric(df['total_sales'], errors='coerce')
        df = df.dropna(subset=['total_sales'])
        
        print(f"After cleaning: {len(df)} records")
        
        # Aggregate total global sales per year
        sales_by_year = df.groupby('Year')['total_sales'].sum().reset_index()
        sales_by_year = sales_by_year.sort_values('Year')
        
        print(f"Years covered: {sales_by_year['Year'].min()} to {sales_by_year['Year'].max()}")
        print(f"Total years: {len(sales_by_year)}")
        
        # Prepare features and labels for linear regression
        X = sales_by_year[['Year']]
        y = sales_by_year['total_sales']
        
        # Fit linear regression model
        model = LinearRegression()
        model.fit(X, y)
        
        # Get model performance info
        score = model.score(X, y)
        print(f"Model R-squared score: {score:.4f}")
        
        # Predict next 5 years
        last_year = sales_by_year['Year'].max()
        future_years = pd.DataFrame({'Year': range(last_year + 1, last_year + 6)})
        future_sales = model.predict(future_years)
        
        print("\nPredictions for the next 5 years:")
        for year, sales in zip(future_years['Year'], future_sales):
            print(f"{year}: {sales:.2f} million units")
        
        # Create the plot
        plt.figure(figsize=(14, 8))
        
        # Plot historical data
        plt.plot(sales_by_year['Year'], sales_by_year['total_sales'], 
                marker='o', linewidth=2, markersize=4, label='Historical Sales', color='blue')
        
        # Plot predicted data
        plt.plot(future_years['Year'], future_sales, 
                marker='x', linewidth=2, markersize=8, linestyle='--', color='red', label='Predicted Sales')
        
        # Add trend line for the entire period
        all_years = pd.concat([sales_by_year[['Year']], future_years])
        all_predictions = model.predict(all_years)
        plt.plot(all_years['Year'], all_predictions, 
                linestyle=':', alpha=0.7, color='green', label='Trend Line')
        
        # Customize the plot
        plt.title(f'Global Video Game Sales Prediction ({start_year}-2024)\n(Historical Data and 5-Year Forecast)', 
                 fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Year', fontsize=12, fontweight='bold')
        plt.ylabel('Global Sales (millions of units)', fontsize=12, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        
        # Add some styling
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        
        # Set x-axis to show more years for context
        plt.xlim(sales_by_year['Year'].min() - 1, future_years['Year'].max() + 1)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        
        # Add annotation for the prediction start
        plt.axvline(x=last_year + 0.5, color='gray', linestyle='--', alpha=0.5)
        plt.text(last_year + 0.5, plt.ylim()[1] * 0.9, 'Predictions Start', 
                rotation=90, ha='right', va='top', alpha=0.7)
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save the plot as an image file so it can be viewed in Replit
        plt.savefig('sales_prediction.png', dpi=300, bbox_inches='tight')
        print("\nPlot saved as 'sales_prediction.png'")
        
        # Don't display plot in web interface - just save it
        plt.close()  # Close the figure to free memory
        
        # Print summary statistics
        print("\nSummary Statistics:")
        print(f"Average historical sales per year: {sales_by_year['total_sales'].mean():.2f} million")
        print(f"Predicted average for next 5 years: {future_sales.mean():.2f} million")
        print(f"Trend: {'Increasing' if model.coef_[0] > 0 else 'Decreasing'} by {abs(model.coef_[0]):.2f} million units per year")
        
        # Additional analysis with console breakdown
        print("\nTop 10 Consoles by Total Sales:")
        console_sales = df.groupby('console')['total_sales'].sum().sort_values(ascending=False).head(10)
        for console, sales in console_sales.items():
            print(f"{console}: {sales:.2f} million")
        
        print("\nTop 10 Publishers by Total Sales:")
        publisher_sales = df.groupby('publisher')['total_sales'].sum().sort_values(ascending=False).head(10)
        for publisher, sales in publisher_sales.items():
            print(f"{publisher}: {sales:.2f} million")
        
        return model, sales_by_year, future_years, future_sales
        
    except FileNotFoundError:
        print("Error: vgchartz-2024.csv file not found in the current directory.")
        return None, None, None, None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, None, None, None

# Run the prediction
if __name__ == "__main__":
    year_range = '8'  # default
    
    if len(sys.argv) > 1:
        year_range = sys.argv[1]
    
    year_desc = {
        '44': '1980-2024',
        '22': '2002-2024',
        '8': '2017-2024'
    }.get(year_range, '2017-2024')
    
    print(f"Video Game Sales Prediction Analysis ({year_desc})")
    print("=" * 40)
    model, historical_data, future_years, predictions = predict_future_sales(year_range)
    
    if model is not None:
        print("\nAnalysis completed successfully!")
        print("Check the 'sales_prediction.png' file for the visualization.")
