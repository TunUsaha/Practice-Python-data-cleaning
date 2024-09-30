from flask import Flask, render_template, request
import pandas as pd
import os
from data_processing import clean_data, create_graph  # Import the functions from data_processing.py

app = Flask(__name__)

# Route for the home page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Route for the tool page (to upload files and clean data)
@app.route('/tool', methods=['GET', 'POST'])
def tool():
    if request.method == 'POST':
        # Retrieve the file and cleaning method choice from the form
        file = request.files['file']
        choice = request.form['cleaning_method']
        if file:
            # Read the uploaded CSV file into a DataFrame
            df = pd.read_csv(file)
            # Clean the data based on the user's choice
            cleaned_data = clean_data(df, choice)
            # Generate and save the graph
            graph_path = create_graph(cleaned_data)
            # Render the results page with the graph and cleaned data table
            return render_template('result.html', graph_path=graph_path, cleaned_data=cleaned_data.head().to_html())
    return render_template('tool.html')  # GET request to display the form

if __name__ == '__main__':
    app.run(debug=True)
