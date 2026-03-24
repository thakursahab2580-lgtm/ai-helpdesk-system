import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix


MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)


def load_data(path="dataset.csv"):
    df = pd.read_csv(path)
    return df


def train():
    print("Loading dataset...")
    df = load_data()

    X = df["text"]
    y = df["category"]

    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("Vectorizing text...")
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000
    )

    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    print("Training Logistic Regression model...")
    model = LogisticRegression(
        max_iter=1000,
        solver="lbfgs",
        multi_class="multinomial"
    )

    model.fit(X_train_tfidf, y_train)

    print("\nEvaluating model...")
    y_pred = model.predict(X_test_tfidf)

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    print("Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    labels = model.classes_
    print(pd.DataFrame(cm, index=labels, columns=labels))


    print("\nSaving model...")
    joblib.dump(model, os.path.join(MODEL_DIR, "classifier.pkl"))
    joblib.dump(vectorizer, os.path.join(MODEL_DIR, "vectorizer.pkl"))

    print("Model and vectorizer saved successfully.")


if __name__ == "__main__":
    train()
