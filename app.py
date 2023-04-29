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

tab1, tab2, tab3, tab4 = st.tabs(["IP data", "Port scanner", "Kodeord", "Om"])

# Get the user's IP address
response = requests.get('https://api.ipify.org')
public_ip_address = response.text

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

def scan_open_ports(ip: str):
    nmap.scan(ip, arguments='-T5 --script=banner')

    data = {}

    for proto in nmap[ip].all_protocols():
        lport = nmap[ip][proto].keys()
        for port in lport:
            if nmap[ip][proto][port]['state'] == 'open':
                service = nmap[ip][proto][port]['name']
                banner = nmap[ip][proto][port].get('script', {}).get('banner', 'No banner')
                data[port] = {'service': service, 'banner': banner}

    print(f"Open ports and banners on {ip}: {data}")

    return data

def generate_description(ip, network_datas):
    descriptions = []
    for port, data in network_datas.items():
        service = data['service']
        banner = data['banner']
        #text_input = f"Beskriv kort følgende netværksoplysninger for en person uden viden om netværk og IT-sikkerhed, og fokusér på, hvad personen kan gøre bedre med netværket:\n\nIP: {ip}\nPort: {port}\nService: {service}\nBanner: {banner}\n"
        
        text_input = f"Provide a brief description in Danish for a person with no knowledge of networking and IT-security about the open ports found in their network, and what they can do better to secure it. Only return a single bullet point. Open ports data:\n Port: {port}\n Service: {service}\n Banner: {banner}\n"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt = text_input,
            n=1,
            max_tokens=100
        )  

        print(response)

        descriptions.append(response.choices[0].text.strip())

    return descriptions


# Display the user's public IP, country flag, and user agent under tab1
with tab1:
   st.header("IP data")
   st.write(f"Public IP: {public_ip_address}")
   st.write(f"Country: {country_name}")
   st.write(f"User agent is: {streamlit_js_eval(js_expressions='window.navigator.userAgent', want_output = True, key = 'UA')}")
   st.image(f"https://flagsapi.com/{country_code}/flat/64.png", width=64)

with tab2:
   st.header("Port scanner")
   scan_ip = st.text_input("Angiv en ip adresse du vil scanne for åbne porte", value=public_ip_address)

   if st.button("Kør"):
      print("Kør knappen aktiveret")
      # Set the target IP address and port range

      scan_output = scan_open_ports(scan_ip)

      if scan_output:
         st.write("Open ports, services, and banners on", scan_ip)
         #st.write(scan_output)
         st.table(scan_output)

         descriptions = generate_description(scan_ip, scan_output)
         st.write("Beskrivelse af dit netværk:")

         bullet_points = []
         for desc in descriptions:
            bullet_points.append(f"- {desc}")

         st.markdown("\n".join(bullet_points))
         
      else:
         st.warning("No open ports found.")



   
with tab3:
   st.header("Kodeord")

   kodeord()
   


with tab4:
   st.header("Om")

   st.text("""
   
   Dette er vores informatik eksamensprojekt.
   
   """)
