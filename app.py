import asyncio
import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from kodeordtjekker import kodeord
import pycountry
import pycountry_convert
import requests
import socket
import threading


tab1, tab2, tab3, tab4 = st.tabs(["IP data", "Port scanner", "Kodeord", "Om"])

# Get the user's IP address
response = requests.get('https://api.ipify.org')
public_ip_address = response.text

# Get the user's country based on their IP address
response = requests.get(f'https://ipapi.co/{public_ip_address}/country/')
country_code = response.text
data = {}


# Get the country name based on the country code
country_name = pycountry.countries.get(alpha_2=country_code).name

def scan_port(port):
   # Create a TCP socket object
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   sock.settimeout(0.01)

   result = sock.connect_ex(('77.233.241.187', 21))
   if result == 0:
      # If the connection was successful, grab the banner
      sock.send(b"GET / HTTP/1.1\r\n\r\n")
      try:
         banner = sock.recv(1024)
         banner = banner.decode()
         data[port] = banner
      except:
         print("error")
      # Append the banner to data dictionary with port number as key

   # Close the socket
   sock.close()


# Display the user's public IP, country flag, and user agent under tab1
with tab1:
   st.header("IP data")
   st.write(f"Public IP: {public_ip_address}")
   st.write(f"Country: {country_name}")
   st.write(f"User agent is: {streamlit_js_eval(js_expressions='window.navigator.userAgent', want_output = True, key = 'UA')}")
   st.image(f"https://flagsapi.com/{country_code}/flat/64.png", width=64)

with tab2:
   st.header("Port scanner")
   scan_ip = st.text_input("Angiv en ip adresse du vil scanne for åbne porte")

   open_ports = []


   if st.button("Kør"):
      # Set the target IP address and port range
      target_ip = scan_ip
      port_range = range(1, 100)

      # Scan each port in the range
      for port in port_range:
         scan_port(port)


      # Display the results
      print(f"Found the following information: {data}")


   
with tab3:
   st.header("Kodeord")

   kodeord()
   


with tab4:
   st.header("Om")

   st.text("""
   
   Dette er vores informatik eksamensprojekt.
   
   """)
