# Remote Oscilloscope Access
## Uputstvo

### Instalacija neophodnih paketa

Ovaj dio je neophodno pokrenuti samo jednom.

1. Instalacija **Python3**

`sudo apt-get update`

`sudo apt-get install python3.6`

2. Instalacija **pip**

`sudo apt-get install python3-pip`

3. Instalacija *dependency*-ja 

U direktorijumu gdje se nalazi kod, pokrenuti:

`sudo python3 setup.py install`

Moguće je da sam zaboravio da dodam neki *dependency*. U tom slučaju se taj paket koji fali može instalirati sa `pip3 install naziv_paketa` .

### Pokretanje aplikacije

Za detaljan opis načina na koji se aplikacija poziva pokrenuti `python3 read_rpi.py -h`

Prvo je potrebno pozicionirati se u direktorijum gdje se nalaze `.py` skripte.

Otvoriti terminal pokrenuti skriptu `read_rpi.py`.

​			`python3 read_rpi.py proxy50.rt3.io 39489`

**!!!** Umjesto `proxy50.rt3.io` i `39489` unijeti dobijene pristupne parametre. **!!!** Ako nisu dobri ovi parametri, dolazi do *exception*-a. Generalno, ako se desi *exception*, prvo ovo dvoje provjeriti.

Prvo se radi podešavanje osciloskopa. Moguće je izabrati opciju da se osciloskop podesi prethodno unešenim parametrima(parametrima koji su unešeni pri prethodnom pokretanju aplikacije). Druga opcija je da se parametri ponovo unesu.

Nakon toga, slijedi konekcija. Ako se konekcija uspostavi, dobija se prikaz na konzoli 

`INFO : Authentication (password) successful!`

Ako je osciloskop u EDGE modu, sada se čeka na detekciju signala.

*Sada pokrenuti C kod koji se tiče laboratorijske vježbe.* 

Dostavljanje slike može trajati desetak sekundi. To je zbog toga što se svaki put moraju podesiti parametri osciloskopa.