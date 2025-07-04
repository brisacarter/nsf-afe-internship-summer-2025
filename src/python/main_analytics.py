def load_data():
    # Try different possible paths for the CSV file
    possible_paths = [
        'vgsales.csv',
        'data/vgsales.csv',
        '../vgsales.csv',
        '../../vgsales.csv',
        os.path.join(os.path.dirname(__file__), '../../vgsales.csv'),
        os.path.join(os.path.dirname(__file__), '../../../vgsales.csv')
    ]

    for file_path in possible_paths:
        if os.path.exists(file_path):
            try:
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
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                continue

    print("No data file found!")