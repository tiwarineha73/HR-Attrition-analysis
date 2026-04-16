"""
ml_model.py — Train and cache an attrition prediction model (Random Forest).
Includes SHAP-style feature importance and prediction probability output.
"""

import pandas as pd
import numpy as np
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report, roc_auc_score,
    accuracy_score, confusion_matrix,
)


FEATURE_COLS = [
    "Age", "DailyRate", "DistanceFromHome", "Education",
    "EnvironmentSatisfaction", "HourlyRate", "JobInvolvement",
    "JobLevel", "JobSatisfaction", "MonthlyIncome", "MonthlyRate",
    "NumCompaniesWorked", "PercentSalaryHike", "PerformanceRating",
    "RelationshipSatisfaction", "StockOptionLevel", "TotalWorkingYears",
    "TrainingTimesLastYear", "WorkLifeBalance", "YearsAtCompany",
    "YearsInCurrentRole", "YearsSinceLastPromotion", "YearsWithCurrManager",
    # Encoded categoricals
    "BusinessTravel_enc", "Department_enc", "EducationField_enc",
    "Gender_enc", "JobRole_enc", "MaritalStatus_enc", "OverTime_enc",
]

CATEGORICAL_COLS = {
    "BusinessTravel": ["Non-Travel", "Travel_Rarely", "Travel_Frequently"],
    "Department": ["Human Resources", "Research & Development", "Sales"],
    "EducationField": ["Human Resources", "Life Sciences", "Marketing",
                       "Medical", "Other", "Technical Degree"],
    "Gender": ["Female", "Male"],
    "JobRole": ["Healthcare Representative", "Human Resources", "Laboratory Technician",
                "Manager", "Manufacturing Director", "Research Director",
                "Research Scientist", "Sales Executive", "Sales Representative"],
    "MaritalStatus": ["Divorced", "Married", "Single"],
    "OverTime": ["No", "Yes"],
}


def _encode(df: pd.DataFrame) -> pd.DataFrame:
    """Ordinal-encode categorical columns."""
    df = df.copy()
    encoders = {}
    for col, categories in CATEGORICAL_COLS.items():
        le = LabelEncoder()
        le.fit(categories)
        df[f"{col}_enc"] = le.transform(df[col].astype(str))
        encoders[col] = le
    return df, encoders


@st.cache_resource
def train_model(df: pd.DataFrame):
    """Train RF model on the full dataset, return model + metrics."""
    df_enc, encoders = _encode(df)

    X = df_enc[FEATURE_COLS]
    y = df_enc["AttritionFlag"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        min_samples_leaf=4,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred) * 100, 1),
        "roc_auc": round(roc_auc_score(y_test, y_prob) * 100, 1),
        "report": classification_report(y_test, y_pred, output_dict=True),
        "conf_matrix": confusion_matrix(y_test, y_pred),
        "feature_importance": pd.Series(
            model.feature_importances_, index=FEATURE_COLS
        ).sort_values(ascending=False),
    }

    return model, encoders, metrics


def predict_employee(model, encoders, input_dict: dict) -> dict:
    """
    Take a dict of raw employee attributes, encode, predict.
    Returns {'label': str, 'probability': float, 'risk_level': str}
    """
    row = pd.DataFrame([input_dict])

    # Encode categoricals
    for col, le in encoders.items():
        val = row[col].iloc[0]
        if val not in le.classes_:
            val = le.classes_[0]
        row[f"{col}_enc"] = le.transform([val])[0]

    X = row[FEATURE_COLS]
    prob = model.predict_proba(X)[0][1]
    label = "Will Leave" if prob >= 0.5 else "Will Stay"

    if prob >= 0.70:
        risk = "High Risk"
    elif prob >= 0.45:
        risk = "Medium Risk"
    else:
        risk = "Low Risk"

    return {"label": label, "probability": round(prob * 100, 1), "risk_level": risk}
