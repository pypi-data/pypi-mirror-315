from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

def train_logistic_regression(X_train, y_train):
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model

def train_knn(X_train, y_train):
    model = KNeighborsClassifier()
    model.fit(X_train, y_train)
    return model

def train_svc(X_train, y_train, C=1.0, gamma='scale'):
    model = SVC(C=C, gamma=gamma, probability=True)

    model.fit(X_train, y_train)

    return model

def train_decision_tree(X_train, y_train, **kwargs):
    model = DecisionTreeClassifier(**kwargs)

    model.fit(X_train, y_train)

    return model

def train_random_forest(X_train, y_train, **kwargs):
    model = RandomForestClassifier(**kwargs)

    model.fit(X_train, y_train)

    return model

def train_gradient_boosting(X_train, y_train, **kwargs):
    model = GradientBoostingClassifier(**kwargs)

    model.fit(X_train, y_train)
    
    return model
