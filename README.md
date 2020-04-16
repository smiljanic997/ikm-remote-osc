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

`sudo apt install python3-matlotlib`. 

Takođe, neke distribucije nemaju preinstaliran interfejs za crtanje(*Tkinter*). Provjera da li *tkinter* postoji se vrši sa `python3 -m tkinter`. Ukoliko ovo vrati grešku, potrebno je instalirati `tkinter` komandom:

`sudo apt install python3-tk`

### Pokretanje aplikacije

Za detaljan opis načina na koji se aplikacija poziva pokrenuti `python3 read_rpi.py -h`

Prvo je potrebno pozicionirati se u direktorijum gdje se nalaze `.py` skripte.

Otvoriti terminal pokrenuti skriptu `read_rpi.py`, na sljedeći način:

​			`python3 read_rpi.py proxy50.rt3.io 39489`

**!!!** Umjesto `proxy50.rt3.io` i `39489` unijeti dobijene pristupne parametre. **!!!** Ako nisu dobri ovi parametri, dolazi do *exception*-a. Generalno, ako se desi *exception*, prvo ovo dvoje provjeriti.

Prvo se radi podešavanje osciloskopa. Moguće je izabrati opciju da se osciloskop podesi prethodno unešenim parametrima(parametrima koji su unešeni pri prethodnom pokretanju aplikacije). Druga opcija je da se parametri ponovo unesu sa standardnog ulaza.



Nakon toga, slijedi konekcija. Ako se konekcija uspostavi, dobija se prikaz na konzoli 

`INFO : Authentication (password) successful!`

Osciloskop je podešen tako da radi u EDGE trigger mode-u, sa SINGLE sweep-om.

Kada se pojavi poruka, pokrenuti C kod koji se tiče laboratorijske vježbe.

Dostavljanje slike može trajati desetak sekundi. Ovo zavisi od parametara koji se odaberu, prvenstveno od *s/div*. 

Slika se prikazuje u novom prozoru. U donjem lijevom uglu date su neke opcije za manipulaciju slikom. Bitno je to da, ako vam je ta slika potrebna poslije, istu sačuvate, pošto se fajl na RPi iz koga se generiše slika svaki put popunjava novim vrijednostima.

**Bitno** - ako se klijentski proces nasilno zatvori(`Ctrl+C `), serverska aplikacija ostaje pokrenuta još 60 sekundi. Tek nakon tog vremena se može opet komunicirati sa osciloskopom.

Bagovi i prijedlozi se mogu prijaviti u sekciji [Issues](https://github.com/smiljanic997/ikm-remote-osc/issues).
