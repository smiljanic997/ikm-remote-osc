# Remote Oscilloscope Access
## Ukratko o skriptama

Skripte koje se nalaze na ovoj grani repozitorijuma su potrebne za komunikaciju Raspberry Pi 3 platforme sa osciloskopom Rigol DS1000D. Python skripte koje su neophodne za ispravan rad su _scope_settings1.py_ i skripte unutar foldera _usbtmc_, te za njih je neophodno da se nalaze na putanji _/home/pi/oscil-remote-access_. Skripta _scope_settings_2chan.py_ se poziva sa host uređaja pokretanjem skripte _read_rpi_, te zbog toga je neophodno da se nalazi na datoj putanji.

Skripta _scope_status.py_ je skripta koja ispisuje trenutna podešavanja osciloskopa te je korisna za provjeru parametara, pokreće se komandom `python3 scope_status.py`. Rezultat poziva skripte je prikazan na slici ispod: 
![Scope status](https://user-images.githubusercontent.com/45833725/78932976-c798dd80-7aa8-11ea-8996-f25945b5dfa3.png)

Skripta _square_wave_test.py_ je pomoćna skripta za generisanje impulsa na GPIO 14 pinu na Raspberry Pi 3 platformi. Izlaz iz skripte je moguć pritiskom stastera `Ctrl + C`

## Uputstvo
1. Nakon pristupa Raspberry Pi 3 platformi sa host uređaja, pozicionirati se u folder _/home/pi/_ komandom `cd /home/pi`.
2. Klonirati repozitorijum komandom `git clone https://github.com/smiljanic997/ikm-remote-osc`
3. Kreirati direktorijum _oscil-remote-access_
4. Pozicionirati se u direktorijum _ikm-remote-osc_ komandom `cd ikm-remote-osc`
5. Izvršiti prelazak na granu _oscil-remote-access_ komandom `git checkout oscil-remote-access`
6. Kopirati željene datoteke komandom `cp -r _scope_settings_2chan.py scope_status.py square_wave_test.py usbtmc /home/pi/oscil-remote-access`
7. Pozicionirati se u direktorijum `/home/pi/oscil-remote-access/usbtmc` sa komandom `cd /home/pi/oscil-remote-access/usbtmc`, zatim pokrenuti instalaciju _usbtmc_ biblioteke komandom `python3 setup.py install`
8. Po završetku instalacije, potrebno je instalirati i modul _pyusb_ komandom `pip3 install pyusb`. Ukoliko niste sigurni da imate modul _pip3_, provjerite komandom `pip3 --version`, ukoliko sistem ne prepoznaje komandu potrebno je instalirajti modul komandom `sudo install python3-pip` nakon čega možete pokrenuti instalaciju _pyusb_ modula.
9. Nakon prethodnog koraka, Raspberry Pi je spreman za komunikaciju sa osciloskopom. Ukoliko želite obrisati klonirani direktorijum, potrebno je pozicionirati se u direktorijum iznad komandom `cd /home/pi`, a zatim obrisati direktorijum i datoteke unutar njega komandom `sudo rm -r ikm-remote-osc`
