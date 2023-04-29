import nmap

nmap = nmap.PortScanner()
asd = nmap.scan("80.210.69.217", arguments='-T5 --script=banner')
print(asd)

