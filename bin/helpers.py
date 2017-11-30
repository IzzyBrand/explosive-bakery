import serial
import sys
import os
import json
from datetime import datetime
import coloredlogs, logging

FORMAT = "[%(asctime)4s] %(message)s"
coloredlogs.install(fmt=FORMAT, level='DEBUG')

SCRIPT_PATH   = os.path.realpath(__file__)
SCRIPT_FOLDER = os.path.dirname(SCRIPT_PATH)
BAKERY_FOLDER = os.path.dirname(SCRIPT_FOLDER)
DATA_FOLDER   = os.path.join(BAKERY_FOLDER, 'thrust-tests')

defaults = {
    'serial_port': '/dev/tty.wchusbserial1410',
    'baud_rate': 115200,
    'rocket_length': 0.0,
    'rocket_diameter': 0.0,
    'rocket_fuel_mass': 0.0,
    'rocket_mass': 0.0,
    'rocket_material': 'PVC',
    'fuel_type': 'Corn Syrup',
    'nozzle_used': True,
    'comments': '',
    'data': {},
    'date': '',
    'datafile': 'test-data.json',
    'test-path': '',
    'test-name': '',
    'complete': False
}

def json_sort(options):
    from collections import OrderedDict as OD
    skeys = ['date', 'complete', 'test-path', 'datafile', 'test-name',
             'serial_port', 'baud_rate', 'rocket_length', 'rocket_diameter',
             'rocket_material', 'rocket_fuel_mass', 'rocket_mass', 'fuel_type',
             'nozzle_used', 'left_endpoint', 'right_endpoint', 'comments',
             'data']
    return OD(sorted(options.iteritems(), key=lambda x: skeys.index(x[0])))

def str_prompt(string):
    try:
        return raw_input(string)
    except KeyboardInterrupt:
        print ''
        logging.warning('Exiting...')
        sys.exit(0)

def numb_prompt(prompt, value):
    while True:
        try:
            inp = raw_input(prompt)
            return float(inp)
        except KeyboardInterrupt:
            print ''
            logging.warning('Exiting...')
            sys.exit(0)
        except ValueError:
            logging.error('%s must be a number...' % value)

def get_parameter(options):
    print '\nEnter parameters (ctrl-c to exit)'
    print '0. Continue'
    print '1. Serial Port [%s]' % options['serial_port']
    print '2. Baud Rate [%s]' % options['baud_rate']
    print '3. Rocket length [%s]' % options['rocket_length']
    print '4. Rocket inner diameter [%s]' % options['rocket_diameter']
    print '5. Rocket mass with fuel [%s]' % options['rocket_fuel_mass']
    print '6. Rocket mass without fuel [%s]' % options['rocket_mass']
    print '7. Rocket material [%s]' % options['rocket_material']
    print '8. Fuel type [%s]' % options['fuel_type']
    print '9. Nozzle [%s]' % options['nozzle_used']
    print '10. Comments [%s]' % options['comments']

    while 1:
        try:
            option = raw_input('> ')
            if option == '':
                option = 0
            option = int(option)
            return option
        except KeyboardInterrupt:
            print ''
            logging.warning('Exiting...')
            sys.exit(0)
        except ValueError:
            logging.error('Invalid input')

def get_opt_dict(options=defaults, check_ser=False):
    while True:
        opt = get_parameter(options)
        if opt == 0:
            break
        elif opt == 1:
            if check_ser:
                while True:
                    options['serial_port'] = str_prompt('Serial port: ')
                    try:
                        serial.Serial(options['serial_port'])
                        break
                    except serial.SerialException:
                        logging.error('Serial port not detected.')
            else:
                options['serial_port'] = str_prompt('Serial Port: ')
        elif opt == 2:
            options['baud_rate'] = numb_prompt('Baud Rate: ', 'Baud rate')
        elif opt == 3:
            options['rocket_length'] = numb_prompt('Rocket length (in.): ',
                                                   'Rocket length')
        elif opt == 4:
            options['rocket_diameter'] = numb_prompt('Inner diameter (in.): ',
                                                     'Diameter')
        elif opt == 5:
            options['rocket_fuel_mass'] = numb_prompt('Rocket + Fuel Mass (g): ',
                                                      'Rocket + fuel mass')
        elif opt == 6:
            options['rocket_mass'] = numb_prompt('Rocket Mass (g): ',
                                                 'Rocket mass')
        elif opt == 7:
            options['rocket_material'] = str_prompt('Rocket material: ')
        elif opt == 8:
            options['fuel_type'] = str_prompt('Fuel type: ')
        elif opt == 9:
            while True:
                try:
                    inp = raw_input('1 for nozzle, 2 for no nozzle\n')
                    inp = int(inp)
                    if not (inp == 1 or inp == 2):
                        raise ValueError
                    elif inp == 1:
                        options['nozzle_used'] = True
                        break
                    elif inp == 2:
                        options['nozzle_used'] = False
                        break

                except ValueError:
                    logging.error('Invalid input...')
                except KeyboardInterrupt:
                    print ''
                    logging.warning('Exiting...')
                    sys.exit(0)
        elif opt == 10:
            if not options['comments']:
                options['comments'] = str_prompt('Enter comments: ')
            else:
                options['comments'] += '\n%s' % str_prompt('Additional comments: ')
        else:
            logging.error('Invalid input...')

    return options

def get_defaults():
    return defaults

def remove_home(string):
    return string.replace(string[0:string.index('explosive-bakery/')], '')

def init_test(name, set_opts):
    # if args['json_file'] is not None:
    #     f = args['json_file']
    #     options = get_opt_dict(json.load(args['json_file']), check_ser=check_ser)
    #     args['json_file'].close()
    #     f = open(args['json_file'].name, 'w')
    if set_opts:
        options = get_opt_dict(get_defaults())
    else:
        options = get_defaults()
    while True:
        try:
            inp = raw_input('Launch date [dd-mm-yy] (blank for today): ')
            if not inp:
                date = datetime.now()
            else:
                date = datetime.strptime(inp, '%d-%m-%y')
            break
        except KeyboardInterrupt:
            print ''
            logging.warning('Exiting...')
            sys.exit(0)
        except ValueError:
            logging.warning('Invalid format...')
            continue

    date_folder = date.strftime('%d-%m-%y')
    date_path   = os.path.join(DATA_FOLDER, date_folder)
    test_path = os.path.join(date_path, name)
    datafile_path = os.path.join(test_path, options['datafile'])

    if os.path.exists(test_path):
        logging.warning('Test path already exists.')
        try:
            prompt = 'Continue anyway? (will use existing JSON) [y/n]: '
            resp = raw_input(prompt)
            if resp.lower() != 'y':
                print ''
                logging.warning('Exiting...')
                sys.exit(0)
            else:
                new_json = False
        except KeyboardInterrupt:
            print ''
            logging.warning('Exiting...')
            sys.exit(0)
    else:
        new_json = True

    os.mkdir(date_path) if not os.path.exists(date_path) else None
    os.mkdir(test_path) if not os.path.exists(test_path) else None

    options['test-path'] = remove_home(test_path)
    options['date'] = date_folder
    options['datafile'] = remove_home(datafile_path)
    options['test-name'] = name

    f = open(datafile_path, 'w')

    json.dump(json_sort(options), f, indent=2)
    f.close()
    if new_json:
        logging.debug('JSON written to %s.' % options['datafile'])
    else:
        logging.debug('JSON at %s updated.' % options['datafile'])
    return options

