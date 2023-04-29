import streamlit as st
import pandas as pd
import random
import requests
import hashlib
from dotenv import load_dotenv
import os


def kodeord():
    load_dotenv()
    apiKey = os.getenv("apiKey") 

    st.title("Tjek dit kodeord 🔑")

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

    send = False

    def checkPassword(password: str):
        md5 = hashlib.md5(password.encode('utf-8')).hexdigest()[0:10] 
        headers = {
            "authorization": f"basic {apiKey}" 
        }

        json_data = {
            "partialMD5": md5,
        }

        response = requests.post('https://api.enzoic.com/passwords', headers=headers, json=json_data)
        
        try:
            return response.json()
        except:
            return None


    if not send:
        st.subheader("Indtast dit kodeord nedenfor")

        st.text_input("Kodeord", key="password", type="password")
        if st.button("Tjek ✈️"):
            send = True


    if send:
        password = st.session_state.password
        passwordLength = len(password)

        response = checkPassword(password)
        if response:
            response = response.get("candidates")[0]
            inExposure = response.get("revealedInExposure")
            exposureCount = response.get("exposureCount")
            if inExposure:
                st.write("Dit kodeord er desværre med i et datalæk😥")
                st.write(f"Dit kodeord er blevet lækket {exposureCount} gange")
        elif response == None:
            st.write("Tillykke, dit kodeord er ikke med i et datalæk 🎉")


        st.subheader("Hvor lang tid tager det for dit kodeord at blive cracket?")

        df = pd.DataFrame(
            {
                "Antal karakterer": [x for x in range(4, 19)],
                "Tal": ["Øjeblikkeligt", "Øjeblikkeligt", "Øjeblikkeligt", "Øjeblikkeligt", "Øjeblikkeligt", "Øjeblikkeligt", "Øjeblikkeligt", "Øjeblikkeligt", "2 sek", "19 sek", "3 min", "32 min", "5 timer", "2 dage", "3 uger"],
                "Små bogstaver": ["Øjeblikkeligt", "Øjeblikkeligt", "Øjeblikkeligt", "Øjeblikkeligt", "Øjeblikkeligt", "10 sek", "4 min", "2 timer", "2 dage", "2 måneder", "4 år", "100 år", "3t år", "69t år", "2m år"],
                "Store & små bogstaver": ["Øjeblikkeligt", "Øjeblikkeligt", "Øjeblikkeligt", "2 sek",  "2 min", "1 time", "3 dage", "5 måneder", "24 år", "1t år", "64t år", "3m år", "173m år", "9mia år", "467mia år"],
                "Tal, store & små bogstaver": ["Øjeblikkeligt", "Øjeblikkeligt", "Øjeblikkeligt", "7 sek", "7 min", "7 timer", "3 uger", "3 år", "200 år", "12t år", "750t år", "46m år", "3mia år", "179mia år", "11 trilioner år"],
                "Tal, symboler, store & små bogstaver": ["Øjeblikkeligt", "Øjeblikkeligt", "Øjeblikkeligt", "31 sekunder", "39 min", "2 dage", "5 måneder", "34 år", "3t år", "202t år", "16m år", "1mia år", "92mia år", "7 trilioner år", "438 trilioner år"]
            }
        )

        hide_table_row_index = """
                    <style>
                    thead tr th:first-child {display:none}
                    tbody th {display:none}
                    </style>
                    """

        st.markdown(hide_table_row_index, unsafe_allow_html=True)

        def highlightLength(row):
            if row["Antal karakterer"] == passwordLength:
                return ['background-color:yellow'] * len(row)
            else:
                return ['background-color:white'] * len(row)

            # return ['background-color:red'] * len(
            #     row) if row["Antal karakterer"] == passwordLength else ['background-color:green'] * len(row)

        # df.style.apply(color_coding, axis=1)



        st.dataframe(df.style.apply(highlightLength, axis=1), use_container_width=True)
