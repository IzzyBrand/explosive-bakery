##############
## Collects rocket parameters
##############
## requires pySerial to be installed 
import serial
import sys
import os
import json

defaults = {
    'serial_port': '/dev/tty.wchusbserial1410',
    'baud_rate': 115200,
    'rocket_length': 0.0,
    'rocket_diameter': 0.0,
    'rocket_fuel_mass': 0.0,
    'rocket_mass': 0.0,
    'rocket_material': 'PVC',
    'fuel_type': 'Candy',
    'nozzle_used': True,
    'comments': '',
    'data': {},
    'date': ''
    'filename': '',
}

def json_sort(opts):
    from collections import OrderedDict as OD
    skeys = ['date', 'serial_port', 'baud_rate', 'rocket_length', 'rocket_diameter',
             'rocket_material', 'rocket_fuel_mass', 'rocket_mass', 'fuel_type',
             'nozzle_used', 'left_endpoint', 'right_endpoint', 'filename',
             'comments', 'data']
    return OD(sorted(opts.iteritems(), key=lambda x: skeys.index(x[0])))

def str_prompt(string):
    try:
        return raw_input(string)
    except KeyboardInterrupt:
        print '\nExiting...'
        sys.exit(0)

def numb_prompt(prompt, value):
    while True:
        try:
            inp = raw_input(prompt)
            return float(inp)
        except KeyboardInterrupt:
            print '\nExiting...'
            sys.exit(0)
        except ValueError:
            print '%s must be a number...' % value

def get_parameter(opts):
    print '\nEnter parameters (ctrl-c to exit)'
    print '0. Continue'
    print '1. Serial Port [%s]' % opts['serial_port']
    print '2. Baud Rate [%s]' % opts['baud_rate']
    print '3. Rocket length [%s]' % opts['rocket_length']
    print '4. Rocket inner diameter [%s]' % opts['rocket_diameter']
    print '5. Rocket mass with fuel [%s]' % opts['rocket_fuel_mass']
    print '6. Rocket mass without fuel [%s]' % opts['rocket_mass']
    print '7. Rocket material [%s]' % opts['rocket_material']
    print '8. Fuel type [%s]' % opts['fuel_type']
    print '9. Nozzle [%s]' % opts['nozzle_used']
    print '10. Comments'

    while 1:
        try:
            option = raw_input('> ')
            option = int(option)
            return option
        except KeyboardInterrupt:
            print '\nExiting...'
            sys.exit(0)
        except ValueError:
            print 'Invalid input'

def get_opt_dict(options=defaults):
    while True:
        opt = get_parameter(options)
        if opt == 0:
            break
        elif opt == 1:
            while True:
                options['serial_port'] = str_prompt('Serial port: ')
                try:
                    serial.Serial(options['serial_port'])
                    break
                except serial.SerialException:
                    print 'Serial port not detected.'
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
                    print 'Invalid input...'
                except KeyboardInterrupt:
                    print '\nExiting...'
                    sys.exit(0)
        elif opt == 10:
            if not options['comments']:
                options['comments'] = str_prompt('Enter comments: ')
            else:
                options['comments'] += '\n%s' % str_prompt('Additional comments: ')
        else:
            print 'Invalid input...'

    return options

if __name__ == '__main__':
    try:
        file_path = os.path.abspath(sys.argv[1])
        if not os.path.exists(file_path):
            raise IOError

        opts = json.load(open(file_path, 'r'))
        json.dump(json_sort(get_opt_dict(options=opts)),
                  open(file_path, 'w'), indent=2)
    except IndexError:
        print 'Must be run with format:'
        print 'python set_options.py <file-name.json>'
    except IOError:
        print 'File not found...'


