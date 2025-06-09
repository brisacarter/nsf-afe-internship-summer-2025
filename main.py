
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def predict_future_sales():
    try:
        # Load and clean data from the existing CSV file
        df = pd.read_csv('vgsales.csv')
        print(f"Loaded {len(df)} records from vgsales.csv")
        
        # Clean the data - remove rows with missing Year or Global_Sales
        df = df.dropna(subset=['Year', 'Global_Sales'])
        
        # Convert Year to integer and filter out invalid years
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        df = df.dropna(subset=['Year'])
        df['Year'] = df['Year'].astype(int)
        
        # Filter out years that seem unrealistic (before 1970 or after current year)
        df = df[(df['Year'] >= 1970) & (df['Year'] <= 2020)]
        
        print(f"After cleaning: {len(df)} records")
        
        # Aggregate total global sales per year
        sales_by_year = df.groupby('Year')['Global_Sales'].sum().reset_index()
        sales_by_year = sales_by_year.sort_values('Year')
        
        print(f"Years covered: {sales_by_year['Year'].min()} to {sales_by_year['Year'].max()}")
        print(f"Total years: {len(sales_by_year)}")
        
        # Prepare features and labels for linear regression
        X = sales_by_year[['Year']]
        y = sales_by_year['Global_Sales']
        
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
        
        print(f"\nPredictions for the next 5 years:")
        for year, sales in zip(future_years['Year'], future_sales):
            print(f"{year}: {sales:.2f} million units")
        
        # Create the plot
        plt.figure(figsize=(14, 8))
        
        # Plot historical data
        plt.plot(sales_by_year['Year'], sales_by_year['Global_Sales'], 
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
        plt.title('Global Video Game Sales Prediction\n(Historical Data and 5-Year Forecast)', 
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
        print(f"\nPlot saved as 'sales_prediction.png'")
        
        # Display the plot
        plt.show()
        
        # Print summary statistics
        print(f"\nSummary Statistics:")
        print(f"Average historical sales per year: {sales_by_year['Global_Sales'].mean():.2f} million")
        print(f"Predicted average for next 5 years: {future_sales.mean():.2f} million")
        print(f"Trend: {'Increasing' if model.coef_[0] > 0 else 'Decreasing'} by {abs(model.coef_[0]):.2f} million units per year")
        
        return model, sales_by_year, future_years, future_sales
        
    except FileNotFoundError:
        print("Error: vgsales.csv file not found in the current directory.")
        return None, None, None, None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, None, None, None

# Run the prediction
if __name__ == "__main__":
    print("Video Game Sales Prediction Analysis")
    print("=" * 40)
    model, historical_data, future_years, predictions = predict_future_sales()
    
    if model is not None:
        print("\nAnalysis completed successfully!")
        print("Check the 'sales_prediction.png' file for the visualization.")
