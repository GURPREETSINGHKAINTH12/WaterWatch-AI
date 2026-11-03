import numpy as np, pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
FEATURES=["ph","turbidity","tds","conductivity","hardness"]
def train_anomaly_model(df):
    X=df[FEATURES].replace([np.inf,-np.inf],np.nan)
    pipe=Pipeline([("imputer",SimpleImputer(strategy="median")),
                   ("scaler",StandardScaler()),
                   ("model",IsolationForest(contamination="auto",random_state=42))])
    pipe.fit(X)
    return pipe
def train_demo_classifier(df):
    # Label is synthetic/demo only; never claim clinical or regulatory validity.
    X=df[FEATURES].replace([np.inf,-np.inf],np.nan)
    y=df["demo_reference_label"]
    pipe=Pipeline([("imputer",SimpleImputer(strategy="median")),
                   ("model",RandomForestClassifier(n_estimators=150,random_state=42))])
    pipe.fit(X,y)
    return pipe
def predict_anomaly(model, row):
    x=pd.DataFrame([{f:row.get(f,np.nan) for f in FEATURES}])
    pred=int(model.predict(x)[0])
    return {"is_anomaly": pred==-1, "score": float(model.decision_function(x)[0])}
