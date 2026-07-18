from flask import Blueprint, abort, render_template

from app.auth import login_required


curriculum = Blueprint("curriculum", __name__, url_prefix="/curriculum")


WEEKS = [
    {
        "number": 1,
        "title": "Python Foundations for Data Science",
        "summary": "Build the core Python skills used throughout the course: syntax, data types, control flow, and a first look at pandas.",
        "objectives": [
            "Understand Python syntax, variables, and data types",
            "Work with lists, dictionaries, and control flow",
            "Read and manipulate tabular data with pandas basics",
        ],
        "tasks": [
            "Case study: Employee Performance Analysis",
            "Complete the Week 1 lab",
            "Submit the Week 1 assignment",
        ],
    },
    {
        "number": 2,
        "title": "NumPy and Pandas",
        "summary": "Learn why NumPy and Pandas are core data science tools, and use them to load, inspect, and clean a real dataset.",
        "objectives": [
            "Explain why NumPy and Pandas are useful in data science",
            "Create and use NumPy arrays for numerical data",
            "Load a CSV into a Pandas DataFrame and inspect it",
            "Select columns, filter rows, handle missing values and duplicates",
            "Create new columns and summarize data with grouping",
        ],
        "tasks": [
            "Case study: Cleaning Employee Scores",
            "Complete the Week 2 lab",
            "Submit the Week 2 assignment",
        ],
    },
    {
        "number": 3,
        "title": "Data Cleaning and Exploratory Data Analysis",
        "summary": "Practice exploratory data analysis on a real dataset that will carry forward as the running example through Week 8.",
        "objectives": [
            "Understand the purpose of exploratory data analysis (EDA)",
            "Identify and fix common data quality problems (missing values, duplicates, inconsistent categories, wrong types)",
            "Ask and answer analytical questions using Pandas",
            "Write clear notes explaining each cleaning/analysis step",
        ],
        "tasks": [
            "Case study: Employee EDA (used through Week 8)",
            "Complete the Week 3 lab",
            "Submit the Week 3 assignment",
        ],
    },
    {
        "number": 4,
        "title": "Data Visualization with Matplotlib and Seaborn",
        "summary": "Turn the cleaned employee dataset into clear, honest visual reports using Matplotlib and Seaborn.",
        "objectives": [
            "Choose the right chart type for a given question",
            "Create bar charts, histograms, box plots, and scatter plots",
            "Use Matplotlib and Seaborn together",
            "Write clear, honest interpretations of charts",
        ],
        "tasks": [
            "Case study: Visual report on the Week 3 employee dataset",
            "Complete the Week 4 lab",
            "Submit the Week 4 assignment",
        ],
    },
    {
        "number": 5,
        "title": "Statistics Foundations",
        "summary": "Learn the statistical foundations needed to summarize data and compare groups honestly.",
        "objectives": [
            "Calculate descriptive statistics (mean, median, range, standard deviation)",
            "Compare groups using summary statistics",
            "Interpret correlation without confusing it with causation",
            "Write statistical findings in plain language",
        ],
        "tasks": [
            "Case study: Statistical analysis of the employee dataset",
            "Complete the Week 5 lab",
            "Submit the Week 5 assignment",
        ],
    },
    {
        "number": 6,
        "title": "Machine Learning: Regression",
        "summary": "Train and evaluate a first machine learning model, predicting a numeric outcome from the employee dataset.",
        "objectives": [
            "Understand features, targets, and train/test splits",
            "Train a LinearRegression model",
            "Evaluate with MAE, MSE, and R2",
        ],
        "tasks": [
            "Case study: Predicting employee score from attendance/salary",
            "Complete the Week 6 lab",
            "Submit the Week 6 assignment",
        ],
    },
    {
        "number": 7,
        "title": "Classification & Model Evaluation",
        "summary": "Move from predicting numbers to predicting categories, and compare models properly instead of picking one blindly.",
        "objectives": [
            "Train a classification model (DecisionTreeClassifier)",
            "Evaluate with accuracy, confusion matrix, and classification report",
            "Compare multiple models on the same data and interpret the differences",
        ],
        "tasks": [
            "Case study: Classifying high performers; Logistic Regression vs Decision Tree",
            "Complete the Week 7 lab",
            "Submit the Week 7 assignment",
        ],
    },
    {
        "number": 8,
        "title": "Capstone Project & Presentation",
        "summary": "Bring cleaning, EDA, visualization, statistics, and modeling together into one end-to-end project and present it.",
        "objectives": [
            "Combine cleaning, EDA, visualization, statistics, and (optionally) a model into one end-to-end project",
            "Present findings clearly: problem, dataset, cleaning, findings, conclusion",
        ],
        "tasks": [
            "Capstone: student's own project, or the running employee dataset",
            "Complete the Week 8 lab",
            "Submit the Week 8 assignment",
        ],
    },
]


@curriculum.route("/")
@login_required
def index():
    return render_template("curriculum/index.html", weeks=WEEKS)


@curriculum.route("/week/<int:week_number>")
@login_required
def week_detail(week_number):
    week = next((item for item in WEEKS if item["number"] == week_number), None)

    if week is None:
        abort(404)

    return render_template("curriculum/week.html", week=week)