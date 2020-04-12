import argparse
import usbtmc
import time
import pickle 


def create_parser():
    parser = argparse.ArgumentParser( description='Parser for oscilloscope parameters.')
    parser.add_argument('channel', default='1', help='Zeljeni kanal za koji se odnose data podesavanja. Vrijednosti mogu biti: 0,1,2 . Vrijednost 0 oznacava da ce se ista podesavanja primjeniti na oba kanala, s izuzetkom offset-a koji se mora naknadno unijeti.')
    parser.add_argument('trigger_mode', default='EDGE', help='Tip trigger-a. Moguce vrijednosti su: EDGE, PULSE, VIDEO, SLOPE, PATT, DUR, ALT. Trenutno je sve testirano samo za EDGE mode')
    parser.add_argument('trigger_sweep', default='SING', help='Trigger sweep mode. Moguce vrijednosti su: AUTO, NORM, SIGN. Default-na vrijednost je SINGLE')
    parser.add_argument('trigger_level', default='1', help='Podesavanje nivoa na koji triger reaguje u voltima. Moguce vrijednosti su opsegu: -6*Scale - 6*Scale . Default-na vrijednost je 1')
    parser.add_argument('volt_scale', default='2', help='Vertikalna skala. Moguce vrijednosti su u opsegu: 0.002 V/div - 10 V/div. Default je 2 V/div')
    parser.add_argument('time_scale', default='1', help='Horizontalna skala. Moguce vrijednosti su u opsegu: 0.000000002 s/div(2ns) - 50 s/div. Default je 1 s/div')
    parser.add_argument('--edge_sens', default='0.5', help='Osjetljivost ivice. Moguce vrijednosti su u opsegu: 0.1 div - 1 div Default-na vrijednost je 0.5')
    parser.add_argument('--edge_slope', default='POS', help='Aktivna ivica kod EDGE trigera. Moguce vrijednosti su: POS, NEG. Default je POS')
    parser.add_argument('--chann1_offset', default='0', help='Ofset kanala 1. Default je 0 V')
    parser.add_argument('--chann2_offset', default='-5', help='Ofset kanala 2. Default je -5 V')
    # Kada je u WAIT/RUN modu ovo je otprilike 1s, ali ako se radi u STOP modu (bez da se pokrece run, ovo moze ici +/- 500s tako da bi se to moglo poslije eksploatisati vise)
    parser.add_argument('--time_offset', default='0', help='Vremenski ofset.')
    # Ovo je bitno kada je za channel odabrana 0
    parser.add_argument('--trigger_source', default='1', help='Trigger source channel. Moguce ulazne vrijednosti su 1 ili 2.')
    return parser

def args_dict(args):

    string_args = {}
    string_args['channel'] = args.channel.split('=')[1]
    string_args['trigger_mode'] = args.trigger_mode.split('=')[1]
    string_args['trigger_sweep'] = args.trigger_sweep.split('=')[1]
    string_args['trigger_level'] = args.trigger_level.split('=')[1]
    string_args['volt_scale'] = args.volt_scale.split('=')[1]
    string_args['time_scale'] = args.time_scale.split('=')[1]
    string_args['edge_sens'] = args.edge_sens
    string_args['edge_slope'] = args.edge_slope
    string_args['chann1_offset'] = args.chann1_offset
    string_args['chann2_offset'] = args.chann2_offset
    string_args['time_offset'] = args.time_offset
    string_args['trigger_source'] = args.trigger_source
    return string_args

if __name__ == "__main__":
    
    MAX_TIME = 60
    start_time = time.time()
    parser = create_parser()
    scope_params = args_dict(parser.parse_args())
    both = False;
    offset = '0'
    instr =  usbtmc.Instrument(6833, 1416)
    if scope_params['channel'] == '0': # Ako su oba, onda koristiti 
        both = True
    elif scope_params['channel'] == '1':
        offset = scope_params['chann1_offset']
    else:
        offset = scope_params['chann2_offset']
    if both == True:
        ## TODO: Ovo je ukoliko su 2 kanala ukljucena, tako da bi trebalo ovo jos pregledati ali prvo da odradimo sa 1 kanalom :)
        instr.write(":CHAN" + str(1) + ":DISP ON")   # Ukljuciti prikaz kanala
        time.sleep(0.2)
        instr.write(":CHAN" + str(1) + ":COUP DC")   # DC Coupling
        time.sleep(0.2)
        instr.write(":CHAN" + str(1) + ":PROB 1")    # Probe podesen na pojacanje 1, ovo znaci da se scale moze podesiti izmedju 2 mV i 10V
        time.sleep(0.2)
        instr.write(":CHAN" + str(1) + ":SCAL " + scope_params['volt_scale'])   
        time.sleep(0.2)
        instr.write(":CHAN" + str(1) + ":OFFS " + scope_params['chann1_offset'])
        time.sleep(0.2)

        instr.write(":CHAN" + str(2) + ":DISP ON")   # Ukljuciti prikaz kanala
        time.sleep(0.2)
        instr.write(":CHAN" + str(2) + ":COUP DC")   # DC Coupling
        time.sleep(0.2)
        instr.write(":CHAN" + str(2) + ":PROB 1")    # Probe podesen na pojacanje 1, ovo znaci da se scale moze podesiti izmedju 2 mV i 10V
        time.sleep(0.2)
        instr.write(":CHAN" + str(2) + ":SCAL " + scope_params['volt_scale'])
        time.sleep(0.2)
        instr.write(":CHAN" + str(2) + ":OFFS " + scope_params['chann2_offset'])
        time.sleep(0.2)
        
        # Trigger settings
        instr.write(":TRIG:MODE " + scope_params['trigger_mode'])     
        time.sleep(0.2)
        instr.write(":TRIG:" + scope_params['trigger_mode'] + ":SOUR CHAN" + scope_params['trigger_source'])
        time.sleep(0.2)
        instr.write(":TRIG:" + scope_params['trigger_mode'] + ":SWE " + scope_params['trigger_sweep']) 
        time.sleep(0.2)
        instr.write(":TRIG:" + scope_params['trigger_mode'] + ":COUP DC")   # default DC coupling
        time.sleep(0.2)
        instr.write(":TRIG:LEV "+ scope_params['trigger_level'])    
        time.sleep(0.2)      
        # Edge trigger settings
        if scope_params['trigger_mode'] == 'EDGE':
            instr.write(":TRIG:EDGE:SLOP " + scope_params['edge_slope']) 
            time.sleep(0.2)
            instr.write(":TRIG:EDGE:SENS " + scope_params['edge_sens'])  # osjetljivost na pola podioka 
            time.sleep(0.2)
        # Time scale settings
        instr.write(":TIM:MODE MAIN") # default is main time mode (not delayed one)
        # TODO: Insert more code for Time menagment (delays and possible offset - to be tested more)
        instr.write(":TIM:SCAL " + scope_params['time_scale']) 
        time.sleep(0.2)
        instr.write(":TIM:OFFS " + scope_params['time_offset'])
        time.sleep(0.2)
        # Pokretanje osciloskopa 
        instr.write(":RUN")
        time.sleep(0.2)
        # instr.write(":FORC")
    else:
        instr.write(":CHAN" + scope_params['channel'] + ":DISP ON")   # Ukljuciti prikaz kanala
        time.sleep(0.2)
        instr.write(":CHAN" + scope_params['channel'] + ":COUP DC")   # DC Coupling
        time.sleep(0.2)
        instr.write(":CHAN" + scope_params['channel'] + ":PROB 1")    # Probe podesen na pojacanje 1, ovo znaci da se scale moze podesiti izmedju 2 mV i 10V
        time.sleep(0.2)
        instr.write(":CHAN" + scope_params['channel'] + ":SCAL " + scope_params['volt_scale'])
        time.sleep(0.2)
        instr.write(":CHAN" + scope_params['channel'] + ":OFFS " + offset)
        time.sleep(0.2)
        # Trigger settings
        instr.write(":TRIG:MODE " + scope_params['trigger_mode'])     
        time.sleep(0.2)
        instr.write(":TRIG:" + scope_params['trigger_mode'] + ":SOUR CHAN" + scope_params['channel'])
        time.sleep(0.2)
        instr.write(":TRIG:" + scope_params['trigger_mode'] + ":SWE " + scope_params['trigger_sweep']) 
        time.sleep(0.2)
        instr.write(":TRIG:" + scope_params['trigger_mode'] + ":COUP DC")   # default DC coupling
        time.sleep(0.2)
        instr.write(":TRIG:LEV " + scope_params['trigger_level'])          
        time.sleep(0.2)
        # Edge trigger settings
        if scope_params['trigger_mode'] == "EDGE":
            instr.write(":TRIG:EDGE:SLOP " + scope_params['edge_slope']) 
            time.sleep(0.2)
            instr.write(":TRIG:EDGE:SENS " + scope_params['edge_sens'])  # osjetljivost na pola podioka 
            time.sleep(0.2)
        # Time scale settings
        instr.write(":TIM:MODE MAIN") # default is main time mode (not delayed one)
        time.sleep(0.2)
        instr.write(":TIM:OFFS " + scope_params['time_offset'])
        time.sleep(0.2)
        instr.write(":TIM:SCAL " + scope_params['time_scale']) 
        time.sleep(0.2)
        instr.write(":TIM:OFFS " + scope_params['time_offset'])
        time.sleep(0.2)
        # Pokretanje osciloskopa 
        instr.write(":RUN")
        #instr.write(":FORC") Provjeriti jos sa prof. da li treba FORC, nisam primjetio nikakvu promjenu do sad
        time.sleep(1)
    print("Podaci su popunjeni!")
    count = 0
    while(("STOP" != instr.ask(":TRIG:STAT?")) & (count < MAX_TIME)):
        time.sleep(1)
        count += 1
    if "STOP" != instr.ask(":TRIG:STAT?"):
        print("Aplikacija je izasla iz programa nakon 60 sekundi.")
        instr.write(":STOP")
        time.sleep(1)
    # Prikupljanje podataka 
    rawdata_1   = instr.ask_raw(str.encode(":WAV:DATA? CHAN1"))[10:]
    rawdata_2   = instr.ask_raw(str.encode(":WAV:DATA? CHAN2"))[10:]
    timescale   = float(instr.ask_raw(str.encode(":TIM:SCAL?")))
    timeoffset  = float(instr.ask_raw(str.encode(":TIM:OFFS?")))
    voltscale   = float(instr.ask_raw(str.encode(":CHAN1:SCAL?"))) # Voltscale je isti za oba kanala ovako
    voltoffset_1  = float(instr.ask_raw(str.encode(":CHAN1:OFFS?")))
    voltoffset_2  = float(instr.ask_raw(str.encode(":CHAN2:OFFS?")))
    # Slanje podataka 
    dict_to_send = { 'rawdata_1' : rawdata_1, 'rawdata_2' : rawdata_2, 'timescale' : timescale, 'timeoffset' : timeoffset,  'voltscale' : voltscale, 'voltoffset_1' : voltoffset_1, 'voltoffset_2' : voltoffset_2 }
    with open('/home/pi/oscil-remote-access/.to_send.pickle', 'wb') as f:
        pickle.dump(dict_to_send, f, protocol=pickle.DEFAULT_PROTOCOL)

    print('finished in {} seconds'.format(round(time.time() - start_time, 2)))
