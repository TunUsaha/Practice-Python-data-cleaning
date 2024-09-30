from flask import Flask, render_template, request, send_file
import os
from data_processing import (
    load_file,
    clean_data,
    create_graph,
    basic_analysis,
    transform_data,
    remove_outliers,
    create_box_plot
)

app = Flask(__name__)

# Create a directory for uploaded files if it doesn't exist
os.makedirs('uploads', exist_ok=True)


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
            # Save the file temporarily
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)  # Save the file to the server

            # Load the file based on its type
            df = load_file(file_path)

            # Transform the data (e.g., convert date columns)
            df = transform_data(df)

            # Clean the data based on the user's choice
            cleaned_data = clean_data(df, choice)

            # Remove outliers (optional)
            cleaned_data = remove_outliers(cleaned_data)

            # Generate and save the graph
            graph_path = create_graph(cleaned_data)

            # Perform basic data analysis
            analysis_results = basic_analysis(cleaned_data)

            # Create a box plot (optional)
            create_box_plot(cleaned_data)

            # Save the cleaned data to a CSV file for downloading
            cleaned_data_path = os.path.join('uploads', 'cleaned_data.csv')
            cleaned_data.to_csv(cleaned_data_path, index=False)

            # Render the results page with the graph and cleaned data table
            return render_template(
                'result.html',
                graph_path=graph_path,
                cleaned_data=cleaned_data.head().to_html(classes='cleaned-data-table'),
                stats=analysis_results['statistics'],
                correlation=analysis_results['correlation'],
                cleaned_data_filename='cleaned_data.csv'  # Pass the filename for download
            )

    return render_template('tool.html')  # GET request to display the form


# Route to download the cleaned data
@app.route('/download/<filename>', methods=['GET'])
def save_data(filename):
    # Define the path where the cleaned data is stored
    cleaned_data_path = os.path.join('uploads', filename)

    # Send the file to the client
    return send_file(cleaned_data_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
