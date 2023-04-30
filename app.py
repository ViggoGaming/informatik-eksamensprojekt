import asyncio
import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from kodeordtjekker import kodeord
import pycountry
import requests
import socket
from dotenv import load_dotenv
import os
import openai
import nmap
import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_data (
    public_ip TEXT PRIMARY KEY,
    user_agent TEXT,
    country TEXT,
    open_ports TEXT,
    descriptions TEXT,
    banners TEXT
)
""")
conn.commit()

tab1, tab2, tab3, tab4 = st.tabs(["IP data", "Port scanner", "Kodeord", "Om"])

# Get the user's IP address
response = requests.get('https://api.ipify.org')
public_ip_address = response.text
user_agent = None

# Get the user's country based on their IP address
response = requests.get(f'https://ipapi.co/{public_ip_address}/country/')
country_code = response.text

# Setup nmap
nmap = nmap.PortScanner()

# OpenAI api key
load_dotenv()
openai.api_key = os.getenv("openai_key")


# Get the country name based on the country code
country_name = pycountry.countries.get(alpha_2=country_code).name


def save_data_to_database(ip, user_agent, country, open_ports, descriptions, banners):
    cursor.execute("SELECT * FROM user_data WHERE public_ip=?", (ip,))
    existing_data = cursor.fetchone()

    if existing_data:
        cursor.execute("""
        UPDATE user_data SET
            user_agent=?,
            country=?,
            open_ports=?,
            descriptions=?,
            banners=?
        WHERE public_ip=?
        """, (user_agent, country, open_ports, descriptions, banners, ip))
    else:
        cursor.execute("""
        INSERT INTO user_data (
            public_ip, user_agent, country, open_ports, descriptions, banners
        ) VALUES (?, ?, ?, ?, ?, ?)
        """, (ip, user_agent, country, open_ports, descriptions, banners))

    conn.commit()


def load_data_from_database(ip):
    cursor.execute("SELECT * FROM user_data WHERE public_ip=?", (ip,))
    return cursor.fetchone()


def scan_open_ports(ip: str):
    nmap.scan(ip, arguments='-T5 --script=banner')

    data = {}
    try:
        for proto in nmap[ip].all_protocols():
            lport = nmap[ip][proto].keys()
            for port in lport:
                if nmap[ip][proto][port]['state'] == 'open':
                    service = nmap[ip][proto][port]['name']
                    banner = nmap[ip][proto][port].get(
                        'script', {}).get('banner', '')
                    data[port] = {'service': service, 'banner': banner}

        return data
    except:
        return None


def generate_description(network_datas):
    descriptions = []
    for port, data in network_datas.items():
        service = data['service']
        banner = data['banner']

        text_input = f"Provide a brief description in Danish for a person with no knowledge of networking and IT-security about the open ports found in their network, and what they can do better to secure it. Only return a single sentence. Data:\n Port: {port}\n Service: {service}\n Banner: {banner}\n"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=text_input,
            n=1,
            max_tokens=100
        )

        print(response)

        descriptions.append(response.choices[0].text.strip())

    return descriptions


# Display the user's public IP, country flag, and user agent under tab1
with tab1:
    st.header("IP data")
    st.write(f"Offentlig IP-adresse: {public_ip_address}")
    st.write(f"Land: {country_name}")
    user_agent = streamlit_js_eval(
        js_expressions='window.navigator.userAgent', want_output=True, key='UA')
    st.write(f"User agent: {user_agent}")
    st.image(f"https://flagsapi.com/{country_code}/flat/64.png", width=64)

with tab2:
    st.header("Port scanner")
    scan_ip = st.text_input(
        "Angiv din offentlige IP-adresse du vil scanne...", value=public_ip_address)

    if st.button("Kør"):
        scan_output = scan_open_ports(scan_ip)
        print(scan_output)
        print(type(scan_output))

        if scan_output:
            st.warning(
                f"Øv😥, følgende åbne porte, bannere og services blev fundet på dit netværk, der har IP-adressen: {scan_ip}")
            st.table(scan_output)

            descriptions = generate_description(scan_output)
            st.write("AI-genereret forbedringsmuligheder af dit netværk:")

            bullet_points = []
            for desc in descriptions:
                bullet_points.append(f"- {desc}")

            st.markdown("\n".join(bullet_points))

            save_data_to_database(public_ip_address, user_agent, country_name, str(scan_output), "\n".join(
                descriptions), "\n".join([data["banner"] for data in scan_output.values()]))

        else:
            st.success(
                "Tillykke 🎉. Der er ikke blevet fundet nogle åbne porte...")

    # Load and display data from the database when the application starts
    loaded_data = load_data_from_database(public_ip_address)

    if loaded_data:
        with st.expander("Tidligere scanninger"):
            ip, user_agent, country, open_ports, descriptions, banners = loaded_data
            st.write(f"Offentlig IP-adresse: {ip}")
            st.write(f"User agent: {user_agent}")
            st.write(f"Land: {country}")

            if open_ports:
                st.write("Åbne porte, bannere og services på: ")
                st.write(open_ports)
                st.write("AI-genereret forbedringsmuligheder af dit netværk:")
                st.write(descriptions)
                st.write("Bannere:")
                st.write(banners)
            else:
                st.write("Ingen åbne porte fundet i gammelt data...")


with tab3:
    st.header("Kodeord")

    kodeord()


with tab4:
    st.header("Om")
    st.header("Informatik B eksamensprojekt")
    st.markdown("Dette er vores Informatik B eksamensprojekt.")
    st.markdown("Udviklet af Rasmus 3.M & Victor 3.M")
    st.markdown("Produktets formål er at hjælpe almindelige brugere til at finde ud af, om der er eksisterer åbne porte på deres lokale netværk, som kan udgøre en sikkerhedstrussel. Skulle dette være tilfældet, laves en række simple AI-genererede beskrivelser af de åbne portes formål og der gives anbefalinger til, hvad man kan gøre for at sikre sig.")
    st.markdown("Produktet er et simpelt værktøj, som kan give et fingerpeg om netværkets sikkerhed. Man kan da finde ud af, om man bør tage handling og evt. kontakte nogle IT-professionelle, som kan hjælpe en.")
