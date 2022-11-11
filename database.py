import os
#import streamlit as st  # pip install streamlit
from deta import Deta  # pip install deta
from dotenv import load_dotenv #pip install python-dotenv

# Load the environment variables
load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY")
#DETA_KEY = st.secrets["DETA_KEY"]

# Initialize with a project key
deta = Deta(DETA_KEY)

# This is how to create/connect a database
db = deta.Base("SDF_Lijm_Ratio_Reg")


def insert_record(key_datetime, gebruiker, lijm, harder, ratio, commentaar):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"key": key_datetime, "user": gebruiker, "NettoLijm": lijm, "NettoHarder": harder, "Ratio": ratio, "comment": commentaar})


def fetch_all_records():
    """Returns a dict of all periods"""
    res = db.fetch()
    return res.items


def get_record(period):
    """If not found, the function will return None"""
    return db.get(period)

