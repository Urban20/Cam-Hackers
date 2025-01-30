import requests, re 
from colorama import init,Fore
from requests.structures import CaseInsensitiveDict
import os
from platform import system
from time import sleep

init()

match system():
    
    case 'Windows':
        comando = 'cls'
    case _:
        comando = 'clear'

url = "http://www.insecam.org/en/jsoncountries/"

headers = CaseInsensitiveDict()
headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
headers["Cache-Control"] = "max-age=0"
headers["Connection"] = "keep-alive"
headers["Host"] = "www.insecam.org"
headers["Upgrade-Insecure-Requests"] = "1"
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"



ejecucion = True
contenido = ''

logo ="""
\033[1;31m\033[1;37m ██████╗ █████╗ ███╗   ███╗      ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ ███████╗
██╔════╝██╔══██╗████╗ ████║      ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗██╔════╝
██║     ███████║██╔████╔██║█████╗███████║███████║██║     █████╔╝ █████╗  ██████╔╝███████╗
██║     ██╔══██║██║╚██╔╝██║╚════╝██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗╚════██║
╚██████╗██║  ██║██║ ╚═╝ ██║      ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║███████║
\033[1;31m ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝      ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝
\033[1;31m                  bifurcación de URB@N                ANGELSECURITYTEAM \033[1;31m\033[1;37m\r\n"""

try:
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        countries = data['countries']
        for key, value in countries.items():
            contenido+=f'codigo : ({key}) - {value["country"]} / cantidad de camaras: ({value["count"]}) \r\n'

    else: ejecucion = False        
except Exception as e:
    print(Fore.RED+f'\nhubo un error:\r\n{e}\n')
    ejecucion = False

def guardar(titulo,ip):

    with open(f'{titulo}.txt', 'a') as f:
            
        f.write(f'{ip}\n')

def main():
    ips = []
    print(logo)
    print(contenido)
    print(Fore.CYAN+'\nCTRL + C = salir del script\n')

    country = input(Fore.WHITE+"\ncodigo(##) >> ").strip()
    

    res = requests.get(
        f"http://www.insecam.org/en/bycountry/{country}", headers=headers
    )
    
    if res.status_code == 200:
        last_page = re.findall(r'pagenavigator\("\?page=", (\d+)', res.text)[0]

        for page in range(int(last_page)):
            res = requests.get(
                f"http://www.insecam.org/en/bycountry/{country}/?page={page}",
                headers=headers
            )
            encontrar = re.findall(r"http://\d+.\d+.\d+.\d+:\d+", res.text)

            for ip in encontrar:
            
                print(Fore.RED+ip)
                ips.append(ip)
    else: raise KeyboardInterrupt

    save = str(input(Fore.WHITE+'\n[0] guardar resultados >> ')).strip()

    if save == '0':
        
        for ip in ips:
            guardar(titulo=country,ip=ip)

        print(Fore.GREEN+'\narchivo guardado exitosamente'+country+'.txt\n')

    else: print(Fore.RED+'\narchivo no guardado\n')
    sleep(2)

    os.system(comando)

while ejecucion:
    try:
        main()
    except KeyboardInterrupt:
        ejecucion = False
        exit(1)
    except Exception as e:
        print(Fore.RED+f'\nhubo un error:\r\n{e}')
        ejecucion = False
        exit(1)