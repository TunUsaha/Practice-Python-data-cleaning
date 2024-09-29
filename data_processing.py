import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def clean_data(data):
    # Drop the `ethnic.group` column
    data.drop(columns=['ethnic.group'], inplace=True)

    # Fill missing values in numeric columns with their median
    for column in data.select_dtypes(include=[np.number]).columns:
        data[column] = data[column].fillna(data[column].median())

    return data


def plot_correlation_heatmap(data):
    # Select only numeric columns for correlation matrix
    correlation_matrix = data.select_dtypes(include=[np.number]).corr()

    # Set up the matplotlib figure
    plt.figure(figsize=(10, 8))

    # Create a heatmap with annotations
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True)

    # Add titles and labels
    plt.title('Correlation Heatmap', fontsize=18)
    plt.show()


# Main function
def main():
    # Load data
    data = pd.read_csv('student-dataset.csv')

    # Show initial data overview
    print("Data Overview:")
    print(data.head())
    print("\nColumn Names:")
    print(data.columns)
    print("\nData Info:")
    print(data.info())
    print("\nMissing Values:")
    print(data.isnull().sum())

    # Clean data
    data_cleaned = clean_data(data)

    # Show cleaned data overview
    print("\nCleaned Data Overview:")
    print(data_cleaned.head())
    print("\nCleaned Data Info:")
    print(data_cleaned.info())

    # Save cleaned data
    data_cleaned.to_csv('cleaned_student_dataset.csv', index=False)
    print("Processed data saved to cleaned_student_dataset.csv")

    # Descriptive statistics
    print("\nDescriptive Statistics:")
    print(data_cleaned.describe())

    # Plot correlation heatmap
    plot_correlation_heatmap(data_cleaned)


if __name__ == "__main__":
    main()
