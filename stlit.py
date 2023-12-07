import streamlit as st
import pandas as pd


def get_df():
    df = pd.read_csv("dataset/Motor_Vehicle_Collisions.csv")
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.lower()

    df = df.drop(columns=[
        'vehicle_type_code_5',
        'contributing_factor_vehicle_5',
        'vehicle_type_code_4',
        'contributing_factor_vehicle_4',
        'vehicle_type_code_3',
        'contributing_factor_vehicle_3',
        'off_street_name',
        'zip_code'
    ])

    df.drop('location', axis=1, inplace=True)

    df = df.dropna()

    df['crash_date'] = pd.to_datetime(df['crash_date'])

    return df


def get_date_df(df, date='2020/3/15'):
    return df[df["crash_date"] == date]


df = get_df()

st.title("HSE Project")
st.write("Dashboard for project")

st.dataframe(df.head())

d = st.date_input("Which day crashes you want to see", value=None)

if d:
    st.map(get_date_df(df, date=d.strftime("%Y/%m/%d")))
