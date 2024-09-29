from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os

class DataProcessor:
    def __init__(self, file):
        self.file = file
        self.df = pd.read_csv(file)

    def clean_data(self, choice):
        if choice == '1':
            return self.df.dropna()
        elif choice == '2':
            numeric_columns = self.df.select_dtypes(include=['float64', 'int64']).columns
            self.df[numeric_columns] = self.df[numeric_columns].fillna(self.df[numeric_columns].mean())
            return self.df
        elif choice == '3':
            numeric_columns = self.df.select_dtypes(include=['float64', 'int64']).columns
            self.df[numeric_columns] = self.df[numeric_columns].fillna(self.df[numeric_columns].median())
            return self.df
        else:
            return self.df.dropna()

    def create_graph(self):
        num_columns = self.df.select_dtypes(include=['float64', 'int64']).columns
        self.df[num_columns].hist(figsize=(12, 10), color='skyblue', edgecolor='black', bins=15)
        plt.suptitle('Data Distribution by Column', fontsize=16, fontweight='bold')
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        graph_path = os.path.join('static', 'graph.png')
        plt.savefig(graph_path)
        plt.close()
        return graph_path

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/tool', methods=['GET', 'POST'])  # รองรับ GET และ POST
def tool():
    if request.method == 'POST':
        file = request.files['file']
        choice = request.form['cleaning_method']
        if file:
            processor = DataProcessor(file)
            cleaned_data = processor.clean_data(choice)
            graph_path = processor.create_graph()
            return render_template('result.html', graph_path=graph_path, cleaned_data=cleaned_data.head().to_html())
    return render_template('tool.html')  # กรณี GET

if __name__ == '__main__':
    app.run(debug=True)
