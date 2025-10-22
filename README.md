📊 RFM Analysis and K-Means Clustering Notebook

This Jupyter Notebook documents the complete analytical process for the E-commerce Customer Segmentation Dashboard. It serves as the technical backbone for the live Streamlit application, detailing the methodology used to transform raw transaction data into actionable customer segments.

🚀 Project Overview

The goal of this analysis was to move beyond simple cohort analysis and use unsupervised machine learning to group customers based on their purchasing behavior.

Methodology Pipeline:

    Data Cleaning & Preprocessing: Handling missing values, filtering out returns, and addressing invalid entries.

    RFM Feature Engineering: Calculating the Recency, Frequency, and Monetary value for each unique customer ID.

    Data Scaling: Applying Log Transformation and Standard Scaling to ensure the RFM features are normally distributed and weighted equally for the K-Means algorithm.

    Optimal Cluster Determination: Using the Elbow Method to confirm the optimal number of clusters (k=3).

    K-Means Clustering: Applying the K-Means algorithm to assign a unique cluster label to every customer.

    Segment Profiling: Interpreting the clusters based on their mean RFM scores and assigning the final business names: Best Customers, Growing Customers, and Hibernating Customers.

🛠️ Technical Stack

    Core Languages: Python 3.x

    Data Manipulation: Pandas, NumPy

    Machine Learning: Scikit-learn (KMeans, StandardScaler)

    Visualization: Matplotlib, Seaborn

🔗 Repository Contents

File Name	Description
01_RFM_Analysis_and_KMeans_Clustering.ipynb	This Notebook: Contains the step-by-step code, calculations, and visualizations for the entire analysis process.
rfm_customer_segments.csv	The final output data: A table containing every customer with their calculated RFM scores and their assigned Cluster_Label.
rfm_cluster_summary.csv	The summarized metrics used for the final dashboard, including the mean RFM scores for each cluster.
