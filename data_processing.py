import pandas as pd
from sklearn.preprocessing import StandardScaler


def load_data(file_path):
    """Load data from a CSV file."""
    data = pd.read_csv(file_path)
    return data


def inspect_data(data):
    """Inspect data and print basic information."""
    print("Data Overview:")
    print(data.head())
    print("\nColumn Names:")
    print(data.columns)
    print("\nData Info:")
    print(data.info())
    print("\nMissing Values:")
    print(data.isnull().sum())



def handle_missing_values(data):
    """Handle missing values by dropping rows or filling them."""
    # Drop rows with missing values
    data_cleaned = data.dropna()
    # Alternatively, fill missing values with median
    # data_cleaned = data.fillna(data.median())
    return data_cleaned


def standardize_data(data, numeric_columns):
    """Standardize numerical columns."""
    scaler = StandardScaler()
    data[numeric_columns] = scaler.fit_transform(data[numeric_columns])
    return data


def save_data(data, file_path):
    """Save processed data to a CSV file."""
    data.to_csv(file_path, index=False)
    print(f"Processed data saved to {file_path}")


def main():
    # Step 1: Load data
    data = load_data('student-dataset.csv')

    # Step 2: Inspect data
    inspect_data(data)

    # Step 3: Handle missing values
    data_cleaned = handle_missing_values(data)

    # Step 4: Print the cleaned data to check if it is empty
    print("Cleaned Data Overview:")
    print(data_cleaned.head())
    print("Cleaned Data Info:")
    print(data_cleaned.info())

    # Check if the data is empty
    if data_cleaned.empty:
        print("No data available after cleaning.")
        return  # Exit the main function if the data is empty

    # Step 5: Standardize numerical columns
    numeric_columns = ['age', 'english.grade', 'math.grade', 'sciences.grade', 'language.grade', 'portfolio.rating',
                       'coverletter.rating', 'refletter.rating']
    data_standardized = standardize_data(data_cleaned, numeric_columns)

    # Step 6: Save the cleaned data
    save_data(data_standardized, 'cleaned_student_dataset.csv')


if __name__ == "__main__":
    main()


