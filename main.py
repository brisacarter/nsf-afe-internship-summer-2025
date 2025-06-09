import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def predict_future_sales(file_path):
    # Load and clean data
    df = pd.read_csv(file_path)
    df = df.dropna(subset=['Year', 'Global_Sales'])
    df['Year'] = df['Year'].astype(int)

    # Aggregate total global sales per year
    sales_by_year = df.groupby('Year')['Global_Sales'].sum().reset_index()

    # Prepare features and labels
    X = sales_by_year[['Year']]
    y = sales_by_year['Global_Sales']

    # Fit linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict next 5 years
    last_year = sales_by_year['Year'].max()
    future_years = pd.DataFrame({'Year': range(last_year + 1, last_year + 6)})
    future_sales = model.predict(future_years)

    # Plot historical and predicted data
    plt.figure(figsize=(12, 6))
    plt.plot(sales_by_year['Year'], sales_by_year['Global_Sales'], marker='o', label='Historical Sales')
    plt.plot(future_years['Year'], future_sales, marker='x', linestyle='--', color='red', label='Predicted Sales')
    plt.title('Global Video Game Sales Prediction')
    plt.xlabel('Year')
    plt.ylabel('Global Sales (in millions)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Ask user for CSV path
if __name__ == "__main__":
    path = input("Enter the full path to your CSV file: ")
    predict_future_sales(path)
