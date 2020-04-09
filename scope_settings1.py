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
    parser.add_argument('--chann1_offset', default='10', help='Ofset kanala 1. Default je 10 V')
    parser.add_argument('--chann2_offset', default='-5', help='Ofset kanala 2. Default je -5 V')
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
    return string_args

if __name__ == "__main__":

    start_time = time.time()
    parser = create_parser()
    scope_params = args_dict(parser.parse_args())
    both = False;
    offset = '0'
    instr =  usbtmc.Instrument(6833, 1416)
    print(type(scope_params['channel']))
    print(scope_params['time_scale'])
    if scope_params['channel'] == '0': # Ako su oba, onda koristiti 
        both = True
    elif scope_params['channel'] == '1':
        offset = scope_params['chann1_offset']
    else:
        offset = scope_params['chann2_offset']
    if both == True:
        print("Error, both channels selected!")
        ## TODO: Ovo je ukoliko su 2 kanala ukljucena, tako da bi trebalo ovo jos pregledati ali prvo da odradimo sa 1 kanalom :)
        # instr.write(":CHAN" + str(1) + ":DISP ON")   # Ukljuciti prikaz kanala
        # instr.write(":CHAN" + str(1) + ":COUP DC")   # DC Coupling
        # instr.write(":CHAN" + str(1) + ":PROB 1")    # Probe podesen na pojacanje 1, ovo znaci da se scale moze podesiti izmedju 2 mV i 10V
        # instr.write(":CHAN" + str(1) + ":SCAL " + scope_params['volt_scale'])   
        # instr.write(":CHAN" + str(1) + ":OFFS " + scope_params['chann1_offset'])

        # instr.write(":CHAN" + str(2) + ":DISP ON")   # Ukljuciti prikaz kanala
        # instr.write(":CHAN" + str(2) + ":COUP DC")   # DC Coupling
        # instr.write(":CHAN" + str(2) + ":PROB 1")    # Probe podesen na pojacanje 1, ovo znaci da se scale moze podesiti izmedju 2 mV i 10V
        # instr.write(":CHAN" + str(2) + ":SCAL " + scope_params['volt_scale'])
        # instr.write(":CHAN" + str(2) + ":OFFS " + scope_params['chann2_offset'])
        
        # # Trigger settings
        # instr.write(":TRIG:MODE " + scope_params['trigger_mode'])     
        # instr.write(":TRIG:" + scope_params['trigger_mode'] + ":SOUR CHAN" + str(1))
        # instr.write(":TRIG:" + scope_params['trigger_mode'] + ":SWE " + scope_params['trigger_sweep']) 
        # instr.write(":TRIG:" + scope_params['trigger_mode'] + ":COUP DC")   # default DC coupling
        # instr.write(":TRIG:LEV "+ scope_params['trigger_level'])          
        # # Edge trigger settings
        # if scope_params['trigger_mode'] == 'EDGE':
        #     instr.write(":TRIG:EDGE:SLOP " + scope_params['edge_slope']) 
        #     instr.write(":TRIG:EDGE:SENS " + scope_params['edge_sens'])  # osjetljivost na pola podioka 
        # # Time scale settings
        # instr.write(":TIM:MODE MAIN") # default is main time mode (not delayed one)
        # # TODO: Insert more code for Time menagment (delays and possible offset - to be tested more)
        # instr.write(":TIM:SCAL " + scope_params['time_scale']) 
        # # Pokretanje osciloskopa 
        # instr.write(":RUN")
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
        # TODO: Insert more code for Time menagment (delays and possible offset - to be tested more)
        instr.write(":TIM:SCAL " + scope_params['time_scale']) 
        time.sleep(0.2)
        # Pokretanje osciloskopa 
        instr.write(":RUN")
        #instr.write(":FORC") Provjeriti jos sa prof. da li treba FORC, nisam primjetio nikakvu promjenu do sad
        time.sleep(1)
        while("STOP" != instr.ask(":TRIG:STAT?")):
            time.sleep(1)
        # Prikupljanje podataka 
        rawdata     = instr.ask_raw(str.encode(":WAV:DATA? CHAN" + scope_params['channel']))[10:]
        timescale   = float(instr.ask_raw(str.encode(":TIM:SCAL?")))
        timeoffset  = float(instr.ask_raw(str.encode(":TIM:OFFS?")))
        voltscale   = float(instr.ask_raw(str.encode(":CHAN" + scope_params['channel'] + ":SCAL?")))
        voltoffset  = float(instr.ask_raw(str.encode(":CHAN" + scope_params['channel'] + ":OFFS?")))
        # Slanje podataka 
        dict_to_send = { 'rawdata' : rawdata, 'timescale' : timescale, 'timeoffset' : timeoffset,  'voltscale' : voltscale, 'voltoffset' : voltoffset }
        with open('/home/pi/oscil-remote-access/.to_send.pickle', 'wb') as f:
            pickle.dump(dict_to_send, f, protocol=pickle.DEFAULT_PROTOCOL)

        print('finished in {} seconds'.format(round(time.time() - start_time, 2)))
