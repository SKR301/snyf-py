import pandas as pd

IP_datalist = pd.read_csv('ip_data/data_cc.csv')

# check IP in the data_cc file and return country code
def getCountryCodeFromIP(ip):
    ip = ip.split('.')
    return IP_datalist.query(f'ip_start0 <= {ip[0]} & ip_start1 <= {ip[1]} & ip_start2 <= {ip[2]} & ip_start3 <= {ip[3]} & ip_end0 >= {ip[0]} & ip_end1 >= {ip[1]} & ip_end2 >= {ip[2]} & ip_end3 >= {ip[3]}')['country_code'].values[0]
