import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

pd.set_option('future.no_silent_downcasting', True)

def load_and_clean_data(file_path):
    """Loads and cleans the data from a CSV file."""
    data = pd.read_csv(file_path)

    data = data.dropna().drop_duplicates()
    
    data.drop(["Unnamed: 0"], axis=1, inplace=True, errors='ignore')
    
    # Replace categorical values with numerical codes
    data = data.replace(to_replace=['0=Blood Donor', '0s=suspect Blood Donor', '1=Hepatitis', '2=Fibrosis', '3=Cirrhosis'],
                        value=[0, 1, 2, 3, 4]).infer_objects(copy=False)
    data = data.replace(to_replace=['m', 'f'], value=[0, 1]).infer_objects(copy=False)
    
    # Fill missing values with the mean for specific columns
    columns_to_fill = ['ALB', 'ALP', 'CHOL', 'PROT', 'ALT']

    for col in columns_to_fill:
        if col in data.columns:
            data[col] = data[col].fillna(data[col].mean())
    
    return data

def split_and_scale_data(data, target_column, drop_columns, test_size):
    """Splits the data into training and testing sets and scales the features."""    
    X = data.drop(columns=[target_column] + drop_columns, axis=1, errors='ignore')

    y = data[target_column]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=0, stratify=y)
    
    # Check if the training set has more than one class
    if len(y_train.unique()) < 2:
        raise ValueError("The training data needs to have at least two classes.")
    
    # Standardize the features
    scaler = StandardScaler()

    X_train = scaler.fit_transform(X_train)
    
    X_test = scaler.transform(X_test)
    
    return X_train, X_test, y_train, y_test
