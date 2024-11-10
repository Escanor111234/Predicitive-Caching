import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from datetime import datetime

# Step 1: Load the CSV file
df = pd.read_csv(r"C:\Users\akash\OneDrive\Documents\coding\C++\file_access_log1.csv")

# Step 2: Convert 'Access Time' to datetime and extract useful features
df['Access Time'] = pd.to_datetime(df['Access Time'])
df['Hour'] = df['Access Time'].dt.hour  # Extract hour of access
df['DayOfWeek'] = df['Access Time'].dt.dayofweek  # Extract day of the week
df['DaysSinceAccess'] = (datetime.now() - df['Access Time']).dt.days  # Time since access

# Drop the original 'Access Time' and 'File Path' columns
df.drop(columns=["Access Time", "File Path"], inplace=True)

# Step 3: Separate features (X) and target (y)
X = df.drop(columns=["To Cache"])  # Features (Access Count, File Size, etc.)
y = df["To Cache"]  # Target (whether to cache or not)

# Step 4: Handle categorical data (File Extension) with one-hot encoding
# We will use a ColumnTransformer to encode the file extension
categorical_features = ["File Extension"]
numerical_features = ["Access Count", "File Size", "File Name Length", "Hour", "DayOfWeek", "DaysSinceAccess"]

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(), categorical_features)
    ], remainder='passthrough')

# Step 5: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 6: Create a Random Forest Classifier pipeline
clf = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Step 7: Train the model
clf.fit(X_train, y_train)

# Step 8: Make predictions on the test set
y_pred = clf.predict(X_test)

# Step 9: Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Print evaluation metrics
# print(f"Accuracy: {accuracy:.4f}")
# print(f"Precision: {precision:.4f}")
# print(f"Recall: {recall:.4f}")
# print(f"F1 Score: {f1:.4f}")
