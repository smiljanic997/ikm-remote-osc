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

Prvo se radi podešavanje osciloskopa. Moguće je izabrati opciju da se osciloskop podesi prethodno unešenim parametrima(parametrima koji su unešeni pri prethodnom pokretanju aplikacije; ova opcija se može izabrati i pri prvom pokretanju, tada se koriste parametri koji su se dobro pokazali na testnim signalima). Druga opcija je da se parametri ponovo unesu.

Nakon toga, slijedi konekcija. Ako se konekcija uspostavi, dobija se prikaz na konzoli 

`INFO : Authentication (password) successful!`

Ako je osciloskop u EDGE modu, sada se čeka na detekciju signala.

*Sada pokrenuti C kod koji se tiče laboratorijske vježbe.* 

Dostavljanje slike može trajati desetak sekundi. To je zbog toga što se svaki put moraju podesiti parametri osciloskopa.

Slika se prikazuje u novom prozoru. U donjem lijevom uglu date su neke opcije za manipulaciju slikom. Bitno je to da, ako vam je ta slika potrebna poslije, istu sačuvate, pošto se fajl na RPi iz koga se generiše slika svaki put popunjava novim vrijednostima.

Bagovi i prijedlozi se mogu prijaviti u sekciji [Issues](https://github.com/smiljanic997/ikm-remote-osc/issues).