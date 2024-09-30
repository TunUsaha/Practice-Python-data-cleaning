import pandas as pd
import matplotlib.pyplot as plt
import os


# Function to load file and support multiple file types
def load_file(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.csv':
        return pd.read_csv(file_path)
    elif file_extension == '.xlsx':
        return pd.read_excel(file_path)
    elif file_extension == '.json':
        return pd.read_json(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")


def clean_data(df, choice):
    # Create a copy to avoid modifying the original DataFrame
    df_cleaned = df.copy()

    # Identify numeric columns
    numeric_columns = df_cleaned.select_dtypes(include=['float64', 'int64']).columns.tolist()

    # Attempt to convert only numeric columns to numeric types
    for column in numeric_columns:
        df_cleaned[column] = pd.to_numeric(df_cleaned[column], errors='coerce')

    # Drop or fill NaN values for numeric columns only
    if choice == '1':
        df_cleaned = df_cleaned.dropna(subset=numeric_columns)  # Remove rows with NaN values in numeric columns
    elif choice == '2':
        df_cleaned[numeric_columns] = df_cleaned[numeric_columns].fillna(df_cleaned[numeric_columns].mean())
    elif choice == '3':
        df_cleaned[numeric_columns] = df_cleaned[numeric_columns].fillna(df_cleaned[numeric_columns].median())
    else:
        df_cleaned = df_cleaned.dropna(subset=numeric_columns)  # Default action

    return df_cleaned

# Function for creating histograms of the numeric columns
def create_graph(df):
    num_columns = df.select_dtypes(include=['float64', 'int64']).columns
    df[num_columns].hist(figsize=(12, 10), color='skyblue', edgecolor='black', bins=15)

    plt.suptitle('Data Distribution by Column', fontsize=16, fontweight='bold')
    for ax in plt.gcf().axes:
        ax.set_xlabel(ax.get_xlabel(), fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title(ax.get_title(), fontsize=14, fontweight='bold')
        ax.grid(False)  # Disable grid for a cleaner look

    graph_path = os.path.join('static', 'graph.png')
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(graph_path)
    plt.close()
    return graph_path

# Function for basic data analysis
def basic_analysis(df):
    stats = df.describe(include='all').to_dict()  # Include all data types for description
    numeric_df = df.select_dtypes(include=['float64', 'int64'])  # Only numeric columns for correlation
    correlation = numeric_df.corr().to_dict()  # Calculate correlations for numeric columns only
    return {'statistics': stats, 'correlation': correlation}

# Function for transforming data
def transform_data(df):
    for col in df.select_dtypes(include=['object']):
        try:
            df[col] = pd.to_datetime(df[col])
        except (ValueError, TypeError):
            continue  # Ignore columns that cannot be converted
    return df

# Function for removing outliers using IQR method
def remove_outliers(df):
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    Q1 = df[numeric_columns].quantile(0.25)
    Q3 = df[numeric_columns].quantile(0.75)
    IQR = Q3 - Q1

    # Remove outliers
    df_cleaned = df[~((df[numeric_columns] < (Q1 - 1.5 * IQR)) | (df[numeric_columns] > (Q3 + 1.5 * IQR))).any(axis=1)]
    return df_cleaned

# Function for creating box plot of numeric columns
def create_box_plot(df):
    num_columns = df.select_dtypes(include=['float64', 'int64']).columns
    df[num_columns].boxplot(figsize=(12, 10), grid=False)
    plt.title('Box Plot of Numeric Columns', fontsize=16, fontweight='bold')
    plt.savefig(os.path.join('static', 'box_plot.png'))
    plt.close()

# Function for saving data in specified format
def save_data(df, file_path, file_format='csv'):
    if file_format == 'csv':
        df.to_csv(file_path, index=False)
    elif file_format == 'excel':
        df.to_excel(file_path, index=False)
    elif file_format == 'json':
        df.to_json(file_path, orient='records', lines=True)
    else:
        raise ValueError(f"Unsupported file format: {file_format}")
