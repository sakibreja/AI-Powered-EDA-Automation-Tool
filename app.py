'''import gradio as gr 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 
import ollama


def eda_analysis(file_path):
    df = pd.read_csv(file_path)
    
    for col in df.select_dtypes(include = ['number']).columns:
        df[col].fillna(df[col].median(), inplace = True)
        
    for col in df.select_dtypes(include = ['object']).columns:
        df[col].fillna(df[col].mode()[0], inplace = True)
        
    summary = df.describe(include='all').to_string()
    
    missing_values = df.isnull().sum().to_string()
    
    insights = generate_ai_insights(summary)     
    
    plot_paths = generate_visualizations(df)
    
    return f"\n Data Loaded Successfully \n\n Summary: \n {summary} \n\n Missing Values: \n {missing_values} \n\n LLM Insights: \n {insights} \n\n Plots: \n {plot_paths}"



def generate_ai_insights(df_summary):
    prompt = f"Analyze the dataset summary and provide insights:\n\n{df_summary}"
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

def generate_visualizations(df):
    plot_paths = []

    for col in df.select_dtypes(include = ['number']).columns:
        plt.figure(figsize=(6, 4))
        sns.histplot(df[col], bins = 30, kde=True, color = 'blue')
        plt.title(f"Distribution of {col}")
        path = f"{col}_distribution.png"
        plt.savefig(path)
        plot_paths.append(path)
        plt.close()

    #Corelation Heatmap
    numeric_df = df.select_dtypes(include = ['number'])
    if not numeric_df.empty:
        plt.figure(figsize = (8, 5))
        sns.heatmap(numeric_df.corr(), annot = True, cmap = 'coolwarm', fmt='.2f', linewidths = 0.5)
        plt.title("Correlation Heatmap")
        path = "Correlation_heatmap.png"
        plt.savefig(path)
        plot_paths.append(path)
        plt.close()

    return plot_paths

app = gr.Interface(fn=eda_analysis,
                    inputs = gr.File(type="filepath"),
                    outputs = [gr.Textbox(label = "EDA REPORT"), gr.Gallery(label="Data Visualization")],
                    title = "LLM POWERD EDA DATA ANLYZER APP",
                    description = "upload any dataset to view the EDA report and data visualizations."
)

app.launch(share=True)
'''
import gradio as gr 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 
import ollama
import os
from PIL import Image
import tempfile

def eda_analysis(file_path):
    try:
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Handle missing values
        for col in df.select_dtypes(include=['number']).columns:
            df[col].fillna(df[col].median(), inplace=True)
            
        for col in df.select_dtypes(include=['object']).columns:
            df[col].fillna(df[col].mode()[0], inplace=True)
        
        # Generate summary
        summary = df.describe(include='all').to_string()
        missing_values = df.isnull().sum().to_string()
        
        # Generate AI insights
        insights = generate_ai_insights(summary)     
        
        # Generate visualizations
        plot_images = generate_visualizations(df)
        
        # Create combined report
        report = f"Data Loaded Successfully\n\nSummary:\n{summary}\n\nMissing Values:\n{missing_values}\n\nLLM Insights:\n{insights}"
        
        return report, plot_images
        
    except Exception as e:
        return f"Error: {str(e)}", []

def generate_ai_insights(df_summary):
    try:
        prompt = f"Analyze the dataset summary and provide insights:\n\n{df_summary}"
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except Exception as e:
        return f"AI Insights Error: {str(e)}"

def generate_visualizations(df):
    plot_images = []
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Numerical distributions
        for col in df.select_dtypes(include=['number']).columns:
            plt.figure(figsize=(6, 4))
            sns.histplot(df[col], bins=30, kde=True, color='blue')
            plt.title(f"Distribution of {col}")
            temp_path = os.path.join(temp_dir, f"{col}_distribution.png")
            plt.savefig(temp_path)
            plot_images.append(temp_path)
            plt.close()

        # Correlation heatmap
        numeric_df = df.select_dtypes(include=['number'])
        if not numeric_df.empty:
            plt.figure(figsize=(8, 5))
            sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
            plt.title("Correlation Heatmap")
            temp_path = os.path.join(temp_dir, "correlation_heatmap.png")
            plt.savefig(temp_path)
            plot_images.append(temp_path)
            plt.close()
            
        return [Image.open(p) for p in plot_images]
    
    except Exception as e:
        print(f"Visualization Error: {str(e)}")
        return []

app = gr.Interface(
    fn=eda_analysis,
    inputs=gr.File(file_count="single", type="filepath"),
    outputs=[
        gr.Textbox(label="EDA Report"), 
        gr.Gallery(label="Data Visualizations")
    ],
    title="LLM-Powered EDA Data Analyzer App",
    description="Upload any dataset to view the EDA report and data visualizations."
)

app.launch(share=True)