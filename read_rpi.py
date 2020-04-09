import paramiko
import argparse
import logging
from socket import gaierror
import pickle
from os import path
import re
import vis

logging.basicConfig(level=logging.INFO, format='%(levelname)s : %(message)s')


def create_parser():
    """
    Creates parser instance and adds arguments. Returns parser object.
    """
    parser = argparse.ArgumentParser(
        prog='IKM_OscRemote', description='IKM oscilloscope remote access.', argument_default=argparse.SUPPRESS)
    parser.add_argument(
        'hostname', help='Hostname ili IP adresa. Unos u formatu "proxyBLA.BLA" ili "hostname=proxyBLA.BLA"')
    parser.add_argument(
        'port', help='Port. Unos u formatu "12345" ili "port=12345"')
    parser.add_argument('--username', default=None,
                        help='Korisnicko ime. Unos u formatu "--username name". Default: pi')
    parser.add_argument('--password', default=None,
                        help='Lozinka. Unos u formatu "--password pass". Default: raspberry')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 1.0')
    return parser


def get_connection_params(args):
    """
    Parses command line arguments. Returns a dictionary.
    """
    if args.username is None and args.password is None:
        logging.warning(
            'Using default username("pi") and password("raspberry").\n')
    elif args.username is None:
        logging.warning('Using default username("pi").\n')
    elif args.password is None:
        logging.warning('Using default password("raspberry").\n')

    connection_params = {}
    connection_params['username'] = args.username if args.username is not None else 'pi'
    connection_params['password'] = args.password if args.password is not None else 'raspberry'
    connection_params['hostname'] = args.hostname.split(
        '=')[1] if '=' in args.hostname else args.hostname
    connection_params['port'] = args.port.split(
        '=')[1] if '=' in args.port else args.port
    return connection_params


def receive_file(ssh_client, remote_path, local_path):
    """
    Get file from remote host from remote_path and put it at local_path
    """
    ftp_client = ssh_client.open_sftp()
    ftp_client.get(remote_path, local_path)
    ftp_client.close()


def open_connection(connection_params):
    """
    Open SSH connection.
        connection_params - dictionary containing connection parameters(hostname, port, username, password)
        Returns SSHClient() object.

        Raises:  AuthenticationException, BadHostKeyException, socket.gaierror (propagated)
    """
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=connection_params['hostname'],
                       port=connection_params['port'],
                       username=connection_params['username'],
                       password=connection_params['password'])
    return ssh_client


def dump_in_file(osc_params):
    """
    Write oscilloscope parameters to file.
    Pickle is used since I don't want noone to change this manually.
    """
    with open('.previous_osc_params.pickle', 'wb') as f:
        pickle.dump(osc_params, f, protocol=pickle.DEFAULT_PROTOCOL)


def get_input(input_type):
    """
    Oscilloscope is too expensive to let someone send it garbage. 
    This funcion checks if given oscilloscope parameter is correct.
    Returns parameter as string.
    """
    # this regex matches decimals(both floats and ints)
    exp = '^[0-9]\d*(\.\d+)?$'
    user_input = ''
    if input_type == 'channel':
        while True:
            user_input = input('Broj kanala(1/2)? ')
            if user_input == '1' or user_input == '2':
                break
    elif input_type == 's_div':
        while True:
            user_input = input('s/div[sec]? ')
            if re.fullmatch(exp, user_input):
                if float(user_input) < 50.0:
                    break
    elif input_type == 'v_div':
        while True:
            user_input = input('V/div[V]? ')
            if re.fullmatch(exp, user_input):
                if float(user_input) < 50.0:
                    break
    elif input_type == 'trig_type':
        while True:
            user_input = input('Trigger type[EDGE, PULSE]? ')
            if user_input.upper() == 'EDGE' or user_input.upper() == 'PULSE':
                break
    elif input_type == 'trig_slope':
        while True:
            user_input = input('Trigger slope[POS, NEG]? ')
            if user_input.upper() == 'POS' or user_input.upper() == 'NEG':
                break
    elif input_type == 'trig_level':
        while True:
            user_input = input('Trigger level[V]? ')
            if re.fullmatch(exp, user_input):
                break
    elif input_type == 'sweep':
        while True:
            user_input = input('Trigger sweep[SING, AUTO, NORM]? ')
            if user_input.upper() == 'SING' or user_input.upper() == 'AUTO' or user_input.upper() == 'NORM':
                break  
    return user_input


def get_oscilloscope_params():
    """
    Get oscilloscope parameters from std input. Returns a dictionary.
    """
    if not path.exists('.previous_osc_params.pickle'):
        default_osc_params = {'channel': '1', 's_div': '0.5', 'v_div': '2', 'sweep' : 'SING',
                              'trig_type': 'EDGE', 'trig_slope': 'NEG', 'trig_level': '2'}
        with open('.previous_osc_params.pickle', 'wb') as f:
            pickle.dump(default_osc_params, f,
                        protocol=pickle.DEFAULT_PROTOCOL)

    osc_params = {}
    use_prev_params = None
    while True:
        use_prev_params = input('Koristi prethodne parametre?[y/n] ')
        if use_prev_params == 'y':
            with open('.previous_osc_params.pickle', 'rb') as f:
                osc_params = pickle.load(f)
            break
        elif use_prev_params == 'n':
            osc_params['channel'] = get_input('channel')
            osc_params['s_div'] = get_input('s_div')
            osc_params['v_div'] = get_input('v_div')
            osc_params['trig_type'] = get_input('trig_type').upper()
            osc_params['sweep'] = get_input('sweep').upper()
            osc_params['trig_slope'] = get_input('trig_slope').upper()
            osc_params['trig_level'] = get_input('trig_level')
            dump_in_file(osc_params)
            break
    return osc_params


if __name__ == "__main__":
    parser = create_parser()
    connection_params = get_connection_params(parser.parse_args())

    try:
        osc_params = get_oscilloscope_params()
        command = 'sudo python3 /home/pi/oscil-remote-access/scope_settings1.py channel={} trigger_mode={} sweep={} trig_level={} volt_scale={} time_scale={} --edge_sens=0.5 --edge_slope={} --chann1_offset=0 --chann2_offset=-5'.format(
            osc_params['channel'], osc_params['trig_type'], osc_params['sweep'], osc_params['trig_level'], osc_params['v_div'], osc_params['s_div'], osc_params['trig_slope'])

        ssh_client = open_connection(connection_params)
        stdin, stdout, stderr = ssh_client.exec_command(command)
        print(stdout.readlines()[-1]) # just last line
        receive_file(ssh_client, '/home/pi/oscil-remote-access/.to_send.pickle', vis.LOCAL_PATH)  # TODO > try tempfile here
    except paramiko.AuthenticationException:
        logging.error(
            'Connection failed. Check credentials(username and password).')
    except paramiko.BadHostKeyException:
        logging.error('Bad host key exception occurred.\n')
    except gaierror as err:
        logging.error('Exception occurred. Check hostname and port.\n')
    except Exception:
        logging.error('Exception occurred.\n')
        ssh_client.close()
    else:
        logging.info('Closing connection.')
        ssh_client.close()
        vis.visualize(osc_params['channel'])
