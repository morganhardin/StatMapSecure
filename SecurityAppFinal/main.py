from flask import Flask
from flask import render_template
import subprocess
import re
from datetime import datetime

ip = []

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/scan.html')
def scan():
    return render_template('scan.html')

@app.route('/track.html')
def track():
    return render_template('track.html')

@app.route('/scan_netstat.html')
def scan_results():
    f = open('log_netstat.txt', 'w')
    cmd = ['netstat', '-a']
    subprocess.run(cmd, stdout = f)

    output = []
    lines = open("log_netstat.txt", "r").readlines()
    for line in lines:
        if re.search(r"(\b\d{1,3}\.){3}(\d{1,3})\b(\.\w*){1}", line):
            output.append(re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line))
    
    final = []
    [final.append(x) for x in output if x not in final]

    file = open('ip_log.txt','w')
    for i in final:
        for x in i:
            file.write(x+"\n")

    file = open('track_netstatlog.txt','a')
    today = datetime.today()
    format = '%m-%d-%Y'
    today_date = today.strftime("Date: " + format + "\n")
    file.write(today_date)
    for i in final:
        for x in i:
            file.write(x+"\n")
    file.write('\n')

    return render_template('scan_netstat.html', output = final)

@app.route('/scan_nmap.html')
def scan_nmap():
    nmap = []
    lines = open("ip_log.txt", "r").readlines()
    for line in lines:
        nmap.append(re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line))

    f = open('log_nmap.txt', 'w')
    for i in nmap:
        for x in i:
            cmd = ['nmap', x]
            subprocess.run(cmd, stdout = f)

    output = []
    lines = open("log_nmap.txt", "r").readlines()
    for line in lines:
        if re.search(r"((\d+)\/(\w*)((\s)*(\w*(.)*)))", line):
            output.append(re.findall(r'((\d+)\/(\w*)((\s)*(\w*(.)*)))', line))

    final = []
    for i in output:
        final.append(i[0])

    file = open('port_log.txt','w')
    for i in final:
        file.write(i[0] + '\n')
       
    ports = []
    with open("port_log.txt", "r") as file:
        lines = file.readlines()
        ports.append(lines)

    file = open('track_nmaplog.txt','a')
    today = datetime.today()
    format = '%m-%d-%Y'
    today_date = today.strftime("Date: " + format + "\n")
    file.write(today_date)
    for i in ports:
        for x in i:
            file.write(x)
    file.write('\n')

    return render_template('scan_nmap.html', ports = ports, output = nmap)

@app.route('/track_all.html')
def track_all():
    netstat = []
    with open("track_netstatlog.txt", "r") as file:
        lines = file.readlines()
        netstat.append(lines)

    nmap = []
    with open("track_nmaplog.txt", "r") as file:
        lines = file.readlines()
        nmap.append(lines)

    return render_template('track_all.html', netstat = netstat, nmap = nmap)

if __name__ == '__main__':
    app.run(debug = True)