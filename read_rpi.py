import paramiko
import argparse
import logging
from socket import gaierror
import pickle
from os import path
import vis

logging.basicConfig(level=logging.INFO, format='%(levelname)s : %(message)s')

def create_parser():
    parser = argparse.ArgumentParser(prog='IKM_OscRemote', description='IKM oscilloscope remote access.', argument_default=argparse.SUPPRESS)
    parser.add_argument('hostname', help='Hostname ili IP adresa. Unos u formatu "proxyBLA.BLA" ili "hostname=proxyBLA.BLA"')
    parser.add_argument('port', help='Port. Unos u formatu "12345" ili "port=12345"')
    parser.add_argument('--username', default=None, help='Korisnicko ime. Unos u formatu "--username name". Default: pi')
    parser.add_argument('--password', default=None, help='Lozinka. Unos u formatu "--password pass". Default: raspberry')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    return parser

def get_connection_params(args):
    if args.username is None and args.password is None:
        logging.warning('Using default username("pi") and password("raspberry").\n')
    elif args.username is None:
        logging.warning('Using default username("pi").\n')
    elif args.password is None:
        logging.warning('Using default password("raspberry").\n')
    
    connection_params = {}
    connection_params['username'] = args.username if args.username is not None else 'pi'
    connection_params['password'] = args.password if args.password is not None else 'raspberry'
    connection_params['hostname'] = args.hostname.split('=')[1] if '=' in args.hostname else args.hostname
    connection_params['port'] = args.port.split('=')[1] if '=' in args.port else args.port
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

def get_oscilloscope_params():
    if not path.exists('.previous_osc_params.pickle'):
        # create file with default parameters
        # this is only done the first time the script runs
        # using pickle to save dictionary
        default_osc_params = {'p1' : 'parameter 1', 'p2' : 'parameter 2'}
        with open('.previous_osc_params.pickle', 'wb') as f:
            pickle.dump(default_osc_params, f, protocol=pickle.DEFAULT_PROTOCOL)
    
    osc_params = {}
    use_prev_params = None
    while True:
        use_prev_params = input('Koristi prethodne parametre?[y/n] ')
        if use_prev_params == 'y':
            with open('.previous_osc_params.pickle', 'rb') as f:
                osc_params = pickle.load(f)
            break
        elif use_prev_params == 'n':
            # load from std input
            break
    
    return osc_params

if __name__ == "__main__":
    parser = create_parser()
    connection_params = get_connection_params(parser.parse_args())
    
    try:
        ssh_client = open_connection(connection_params) 
        # stdin, stdout, stderr = ssh_client.exec_command('python3 /home/pi/slaven/testing_py/read_values_v2.py 1.5')
        # print(stdout.readlines())
        # receive_file(ssh_client, '/home/pi/slaven/testing_py/.to_send_v2.pickle', vis.LOCAL_PATH) # TODO > try tempfile here
    except paramiko.AuthenticationException:
        logging.error('Connection failed. Check credentials(username and password).')
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
        vis.visualize()
