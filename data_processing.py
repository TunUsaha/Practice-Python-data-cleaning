import pandas as pd
import matplotlib.pyplot as plt
import os


# Function for cleaning data
def clean_data(df, choice):
    # Remove rows with NaN values
    if choice == '1':
        df_cleaned = df.dropna()
    # Fill NaN values with the mean of the column
    elif choice == '2':
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        df_cleaned = df.copy()
        df_cleaned[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
    # Fill NaN values with the median of the column
    elif choice == '3':
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        df_cleaned = df.copy()
        df_cleaned[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())
    # Default to removing rows with NaN if an invalid choice is made
    else:
        df_cleaned = df.dropna()
    return df_cleaned


# Function for creating histograms of the numeric columns
def create_graph(df):
    num_columns = df.select_dtypes(include=['float64', 'int64']).columns
    # Create histograms for each numeric column
    df[num_columns].hist(figsize=(12, 10), color='skyblue', edgecolor='black', bins=15)

    # Set titles and labels for the graphs
    plt.suptitle('Data Distribution by Column', fontsize=16, fontweight='bold')
    for ax in plt.gcf().axes:
        ax.set_xlabel(ax.get_xlabel(), fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title(ax.get_title(), fontsize=14, fontweight='bold')
        ax.grid(False)  # Disable grid for a cleaner look

    # Save the plot to a file and return the file path
    graph_path = os.path.join('static', 'graph.png')
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(graph_path)
    plt.close()
    return graph_path
