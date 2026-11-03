import streamlit as st, pandas as pd, numpy as np, plotly.express as px, os
from src.translations import TEXT
from src.screening import screen_row, PARAMETERS
from src.modeling import train_anomaly_model, train_demo_classifier, predict_anomaly
from src.database import init_db, save_sample, get_history
st.set_page_config(page_title="WaterWatch AI",page_icon="💧",layout="wide")
lang=st.sidebar.selectbox("Language / भाषा",["English","Hindi"])
t=TEXT[lang]
st.title("💧 "+t["title"])
st.caption(t["subtitle"])
st.warning(t["caution"])
data_path=os.path.join(os.path.dirname(__file__),"data","demo_water_quality.csv")
demo=pd.read_csv(data_path)
@st.cache_resource
def models():
    return train_anomaly_model(demo), train_demo_classifier(demo)
anom_model, clf_model=models()
page=st.sidebar.radio(t["dashboard"],[t["manual"],t["upload"],t["history"]])
if page==t["manual"]:
    st.subheader(t["manual"])
    c1,c2,c3=st.columns(3)
    location=c1.text_input(t["location"],"Demo location")
    ph=c1.number_input("pH",0.0,14.0,7.1,0.1)
    turbidity=c2.number_input("Turbidity (NTU)",0.0,1000.0,2.0,0.1)
    tds=c2.number_input("TDS (mg/L)",0.0,10000.0,250.0,1.0)
    conductivity=c3.number_input("Conductivity (µS/cm)",0.0,10000.0,450.0,1.0)
    hardness=c3.number_input("Hardness (mg/L)",0.0,2000.0,120.0,1.0)
    row={"ph":ph,"turbidity":turbidity,"tds":tds,"conductivity":conductivity,"hardness":hardness}
    if st.button(t["analysis"],type="primary"):
        scr=screen_row(row); an=predict_anomaly(anom_model,row)
        st.session_state["latest_result"]={"location":location,"row":row,"screening":scr,"anomaly":an["is_anomaly"]}
    if "latest_result" in st.session_state:
        result=st.session_state["latest_result"]
        st.metric("Screening result",result["screening"]["status"])
        st.write("Flagged parameters:",", ".join(result["screening"]["flags"]) if result["screening"]["flags"] else "None")
        st.write("Anomaly detected:", "Yes" if result["anomaly"] else "No")
        st.caption("Anomaly score is model-relative, not a probability of unsafe water.")
        st.info("Next step: confirm sampling quality and consult an accredited laboratory if results are concerning.")
        if st.button(t["save"]):
            save_sample(result["location"],result["row"],result["screening"],result["anomaly"])
            st.success("Saved.")
elif page==t["upload"]:
    st.subheader(t["upload"])
    uploaded=st.file_uploader("CSV with columns: "+", ".join(PARAMETERS),type=["csv"])
    if uploaded:
        df=pd.read_csv(uploaded)
        missing=[x for x in PARAMETERS if x not in df.columns]
        if missing: st.error("Missing columns: "+", ".join(missing))
        else:
            st.dataframe(df.head(100),use_container_width=True)
            df["screening_status"]=df.apply(lambda r:screen_row(r)["status"],axis=1)
            df["anomaly"]=anom_model.predict(df[PARAMETERS].replace([np.inf,-np.inf],np.nan))
            st.metric("Rows analyzed",len(df))
            st.plotly_chart(px.histogram(df,x="screening_status",title="Screening results"),use_container_width=True)
            st.plotly_chart(px.scatter(df,x="ph",y="turbidity",color="screening_status",title="pH vs turbidity"),use_container_width=True)
            st.download_button("Download analyzed CSV",df.to_csv(index=False),file_name="waterwatch_analysis.csv")
else:
    st.subheader(t["history"])
    rows=get_history()
    if rows:
        st.dataframe(pd.DataFrame(rows,columns=["ID","Created","Location","Measurements","Screening","Anomaly"]),use_container_width=True)
    else: st.info("No saved samples yet.")
st.sidebar.markdown("---")
st.sidebar.caption("WaterWatch AI | Capstone prototype | SDG 6")
