import pandas as pd
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import joblib

manifest = pd.read_csv("data/processed/manifest.csv")

texts = []
labels = []

for _, row in manifest.iterrows():
    ocr_path = Path(row["ocr_path"])

    if not ocr_path.exists():
        continue

    text = ocr_path.read_text(errors="ignore")
    texts.append(text)
    labels.append(row["doc_type"])

X_train, X_test, y_train, y_test = train_test_split(
    texts,
    labels,
    test_size=0.2,
    random_state=42,
    stratify=labels,
)

model = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
    ("clf", LogisticRegression(max_iter=1000)),
])

model.fit(X_train, y_train)

preds = model.predict(X_test)

print(classification_report(y_test, preds))
print(confusion_matrix(y_test, preds))

Path("models").mkdir(exist_ok=True)
joblib.dump(model, "models/text_baseline_classifier.joblib")

print("Saved model to models/text_baseline_classifier.joblib")