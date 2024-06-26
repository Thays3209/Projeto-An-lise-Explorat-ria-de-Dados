# -*- coding: utf-8 -*-
"""Cópia de notebookc7411acd8e.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pTNxsDZ0cr_w_GG9x_OwBLJZH-ZVODI2
"""

# Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from scipy import stats

# Load the dataset
df = pd.read_csv("/content/sample_data/salaries (2).csv")

# Display the first few rows of the dataset
df.head()

# Summary statistics
df.describe()

# Distribution of numerical variables
num_cols = df.select_dtypes(include=['int64', 'float64']).columns
for col in num_cols:
    plt.figure(figsize=(8, 6))
    sns.histplot(df[col], kde=True)
    plt.title(f'Distribution of {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    plt.show()

# Relationship between categorical variables
cat_cols = df.select_dtypes(include=['object']).columns
for col in cat_cols:
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x=col, order=df[col].value_counts().index)
    plt.title(f'Count of {col}')
    plt.xticks(rotation=45)
    plt.show()

# Visualize the effect of employment_type on salary
plt.figure(figsize=(10, 6))
sns.boxplot(x='employment_type', y='salary_in_usd', data=df)
plt.title('Salary Variation by Employment Type')
plt.xlabel('Employment Type')
plt.ylabel('Salary (USD)')
plt.xticks(rotation=45)
plt.show()

# Visualize the effect of experience_level on salary
plt.figure(figsize=(10, 6))
sns.boxplot(x='experience_level', y='salary_in_usd', data=df)
plt.title('Salary Variation by Experience Level')
plt.xlabel('Experience Level')
plt.ylabel('Salary (USD)')
plt.xticks(rotation=45)
plt.show()

# Visualize the effect of employee_residence on salary
plt.figure(figsize=(10, 6))
sns.boxplot(x='employee_residence', y='salary_in_usd', data=df)
plt.title('Salary Variation by Employee Residence')
plt.xlabel('Employee Residence')
plt.ylabel('Salary (USD)')
plt.xticks(rotation=45)
plt.show()

# Feature Engineering
current_year = 2024  # Update with the current year
df['years_of_experience'] = current_year - df['work_year']

# Visualization of 'years_of_experience'
plt.figure(figsize=(8, 6))
sns.histplot(df['years_of_experience'], kde=True)
plt.title('Distribution of Years of Experience')
plt.xlabel('Years of Experience')
plt.ylabel('Frequency')
plt.show()

from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
job_title_matrix = vectorizer.fit_transform(df['job_title'])
job_title_df = pd.DataFrame(job_title_matrix.toarray(), columns=vectorizer.get_feature_names_out())
df = pd.concat([df, job_title_df], axis=1)

# Visualization of job title frequency
top_n = 10  # Define the number of top job titles to display
job_title_freq = job_title_df.sum().sort_values(ascending=False).head(top_n)

plt.figure(figsize=(10, 6))
sns.barplot(x=job_title_freq.values, y=job_title_freq.index, palette='viridis')
plt.title(f'Top {top_n} Most Frequent Job Titles')
plt.xlabel('Frequency')
plt.ylabel('Job Title')
plt.show()

# Handling Categorical Variables
df_encoded = pd.get_dummies(df, columns=['employment_type', 'experience_level', 'employee_residence'])
frequency_map = df['job_title'].value_counts(normalize=True)
df_encoded['job_title_freq_encoded'] = df['job_title'].map(frequency_map)

# Visualize the effect of job_title frequency encoding on salary
plt.figure(figsize=(10, 6))
sns.scatterplot(x='job_title_freq_encoded', y='salary_in_usd', data=df_encoded)
plt.title('Salary Variation by Job Title Frequency Encoding')
plt.xlabel('Job Title Frequency Encoding')
plt.ylabel('Salary (USD)')
plt.show()

# Outlier Detection and Treatment
z_scores = stats.zscore(df[num_cols])
abs_z_scores = np.abs(z_scores)
outlier_indices = np.where(abs_z_scores > 3)
outlier_rows = list(set(outlier_indices[0]))
df_no_outliers = df.drop(outlier_rows)

# Visualize the distribution of numerical variables before and after outlier removal
plt.figure(figsize=(12, 8))
for i, col in enumerate(num_cols):
    plt.subplot(2, 3, i+1)
    sns.histplot(df[col], kde=True, color='blue', alpha=0.5, label='Before Outlier Removal')
    sns.histplot(df_no_outliers[col], kde=True, color='red', alpha=0.5, label='After Outlier Removal')
    plt.title(f'Distribution of {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    plt.legend()
plt.tight_layout()
plt.show()

# Boxplot Matrix
# Visualize the distribution of numerical variables across different employment types
plt.figure(figsize=(12, 8))
for i, col in enumerate(num_cols):
    plt.subplot(2, 3, i+1)
    sns.boxplot(x='employment_type', y=col, data=df_no_outliers)
    plt.title(f'Boxplot of {col} by Employment Type')
    plt.xlabel('Employment Type')
    plt.ylabel(col)
plt.tight_layout()
plt.show()