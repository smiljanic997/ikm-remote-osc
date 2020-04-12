# Remote Oscilloscope Access
## Uputstvo

**Ovaj kod je potrebno download-ovati na Linux OS, na računar, a ne na RPi. Nije testirano na Windows-u**

### Instalacija neophodnih paketa

Ovaj dio je neophodno pokrenuti samo jednom.

1. Instalacija **pip**

`sudo apt-get install python3-pip`

2. Instalacija *dependency*-ja 
 
`sudo pip3 install paramiko`, 

`sudo apt install python3-numpy`

`sudo apt-get install python3-matlotlib`. 

### Pokretanje aplikacije

Za detaljan opis načina na koji se aplikacija poziva pokrenuti `python3 read_rpi.py -h`

Prvo je potrebno pozicionirati se u direktorijum gdje se nalaze `.py` skripte.

Otvoriti terminal pokrenuti skriptu `read_rpi.py`, na sljedeći način:

​			`python3 read_rpi.py proxy50.rt3.io 39489`

**!!!** Umjesto `proxy50.rt3.io` i `39489` unijeti dobijene pristupne parametre. **!!!** Ako nisu dobri ovi parametri, dolazi do *exception*-a. Generalno, ako se desi *exception*, prvo ovo dvoje provjeriti.

Prvo se radi podešavanje osciloskopa. Moguće je izabrati opciju da se osciloskop podesi prethodno unešenim parametrima(parametrima koji su unešeni pri prethodnom pokretanju aplikacije; ova opcija se može izabrati i pri prvom pokretanju, tada se koriste parametri koji su se dobro pokazali na testnim signalima). Druga opcija je da se parametri ponovo unesu.

Nakon toga, slijedi konekcija. Ako se konekcija uspostavi, dobija se prikaz na konzoli 

`INFO : Authentication (password) successful!`

Ako je osciloskop u EDGE modu, sada se čeka na detekciju signala.

Kada se pojavi poruka, pokrenuti C kod koji se tiče laboratorijske vježbe.

Dostavljanje slike može trajati desetak sekundi. Ovo zavisi od parametara koji se odaberu, prvenstveno od *s/div*. 

Slika se prikazuje u novom prozoru. U donjem lijevom uglu date su neke opcije za manipulaciju slikom. Bitno je to da, ako vam je ta slika potrebna poslije, istu sačuvate, pošto se fajl na RPi iz koga se generiše slika svaki put popunjava novim vrijednostima.

**Bitno** - ako se klijentski proces nasilno zatvori(`Ctrl+C `), serverska aplikacija ostaje pokrenuta, te se mora i ona nasilno ubiti, da bi se nastavilo sa radom. To radite tako što, na RPi kucate `ps -aux`, pronađete `pid` procesa koji u imenu imaju `scope_settings1.py`(ili jedan ili dva ovakva procesa), te ih `kill`-ujete sa komandom `sudo kill -9 pid`. Način da provjerite da niste zakočili osciloskop je da na RPi pokrenete `python3 scope_status.py`(u folderu oscil-remote-access) . Kao rezultat ne smijete dobiti `Recourse busy`.

Bagovi i prijedlozi se mogu prijaviti u sekciji [Issues](https://github.com/smiljanic997/ikm-remote-osc/issues).
