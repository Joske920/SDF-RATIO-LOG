import pandas as pd
import streamlit as st
import database as db
from datetime import datetime

st.set_page_config(
    page_title="SDF Lijm Ratio Registratie",
    page_icon="pencil",
    layout="centered",
    initial_sidebar_state="expanded", #"collapsed"
)

# --- HIDE STREAMLIT STYLE ---

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            input {
                font-size: 1rem !important;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("SDF Lijm ratio registratie")

user: int = 0
tarra_lijmgewicht: int = 200
tarra_hardergewicht: int = 200

if "userID" not in st.session_state:
    st.session_state["userID"] = user

if "brutto_lijmgewicht" not in st.session_state:
    st.session_state["brutto_lijmgewicht"] = 0
if "brutto_hardergewicht" not in st.session_state:
    st.session_state["brutto_hardergewicht"] = 0

if "tarra_lijmgewicht" not in st.session_state:
    st.session_state["tarra_lijmgewicht"] = tarra_lijmgewicht

if "tarra_hardergewicht" not in st.session_state:
    st.session_state["tarra_hardergewicht"] = tarra_hardergewicht

def updateLijm():
    st.session_state["netto_lijmgewicht"] = st.session_state["brutto_lijmgewicht"] - st.session_state["tarra_lijmgewicht"]

def updateHarder():
    st.session_state["netto_hardergewicht"] = st.session_state["brutto_hardergewicht"] - st.session_state["tarra_hardergewicht"]

def calc():
    return (0 if st.session_state["netto_lijmgewicht"] == 0 else ((st.session_state["netto_hardergewicht"] / st.session_state["netto_lijmgewicht"]) * 100))

def resetingave():
    st.session_state["brutto_lijmgewicht"] = 0
    updateLijm()
    st.session_state["brutto_hardergewicht"] = 0
    updateHarder()

def submit_data():
    if user > 0:
        dt_string = datetime.now().strftime("%Y%m%d_%H%M%S")
        db.insert_record(dt_string, user, st.session_state["netto_lijmgewicht"], st.session_state["netto_hardergewicht"], calc(), st.session_state["commentaar_veld"])
        resetingave()
        st.success("Informatie opgeslaan!")
    else:
        st.error("Vul je werknemers ID in aub")

def updateUser():
    global user
    user  = st.session_state["userID"]

st.sidebar.header("Settings:")
st.sidebar.selectbox(label="Omgeving", options=("Ingave", "Geschiedenis"), key="Omgevingskeuze")

if st.session_state["Omgevingskeuze"] == "Ingave":
    with st.container():
        st.write("Invul formulier")
        col1, col2 = st.columns(2)

        col1.number_input("Gewicht van Lijm: (brutto)", min_value=0, format="%i", key="brutto_lijmgewicht", on_change=updateLijm())
        col1.number_input("Gewicht van Lijmbeker: (tarra)", min_value=0, format="%i", key="tarra_lijmgewicht", on_change=updateLijm())

        col2.number_input("Gewicht van Harder: (brutto)", min_value=0, format="%i", key="brutto_hardergewicht", on_change=updateHarder())
        col2.number_input("Gewicht van Harderbeker: (tarra)", min_value=0, format="%i", key="tarra_hardergewicht", on_change=updateHarder())

        col1.number_input("Verrekend Lijm Gewicht: (Netto)", key="netto_lijmgewicht", disabled=True)
        col2.number_input("Verrekend Harder Gewicht: (Netto)", key="netto_hardergewicht", disabled=True)

        st.text("Ratio = ((Harder / Lijm) * 100).")
        st.text("toegelaten range = min:18 - max:24")

        st.number_input(label="Ratio:", value=calc(), disabled=True)

        st.text_area("Commentaar:", key="commentaar_veld")
    with st.container():
        col3, col4 = st.columns(2)

        col3.number_input("Werknemer Nr#", min_value=0, format="%i", key="userID", on_change=updateUser())
        col4.button(label="Registreer meting",on_click=submit_data, key="savetodb_enable")

if st.session_state["Omgevingskeuze"] == "Geschiedenis":
    df = pd.DataFrame(db.fetch_all_records())
    df = df.astype({'NettoHarder':int,'NettoLijm':int,'Ratio':float,'comment':str,'key':str,'user':int})
    df = df[::-1]
    st.download_button(label='Download CSV', data=df.to_csv(index=False, sep=";").encode('utf-8'), file_name='SDF_Ratio_Metingen.csv')
    st.dataframe(df)