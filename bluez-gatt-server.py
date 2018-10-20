#!/usr/bin/env python
"""Main mqtt-to-gatt-server program that provides functionality as described in the 'README.md' file.
"""

import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service
try:
  from gi.repository import GObject
except ImportError:
  import gobject as GObject
import argparse
import service_template

__author__ = "Kasidit Yusuf"
__copyright__ = "mqtt-to-gatt-server 1.0 Copyright (C) 2018 Kasidit Yusuf."
__credits__ = ["Kasidit Yusuf"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Kasidit Yusuf"
__email__ = "ykasidit@gmail.com"
__status__ = "Production"


def main():

    
    ### define options/args

    parser = argparse.ArgumentParser(
        description="mqtt-to-gatt-server 1.0 Copyright (C) 2018 Kasidit Yusuf.\nReleased under the GNU GPL v2 License - see COPYING file (from BlueZ project) for details. This project is a fork of 'python-gatt-server' (https://github.com/Jumperr-labs/python-gatt-server.git) originally by Jumper Labs which is based on 'BlueZ' (http://www.bluez.org/) example code. Credit goes to respective authors and see copyright notices of respective projects for further details.",
        usage="Use mqtt-to-gatt-server to define and start a Bluetooth Low Energy (BLE) service with read/notify characteristics. The characteristic values would be initilized and updated from the specified 'MQTT server and topic'."
    )

    parser.add_argument('-a', '--adapter-name', type=str, help='Adapter name', default='')

    parser.add_argument('--mqtt_host', type=str, help='MQTT Host URL', default='localhost')

    parser.add_argument('--service_assigned_number', type=str, help='BLE service ASSIGNED_NUMBER in hex starting with 0x - see https://www.bluetooth.com/specifications/gatt/services for the full list - e.g., "Battery Service" would be: 0x180F', required=True)

    parser.add_argument('--characteristic_assigned_number_list', type=str, help='Python-sytaxed list of Bluetooth service ASSIGNED_NUMBER in hex starting with 0x - see https://www.bluetooth.com/specifications/gatt/characteristics for the full list - e.g., A list containing one characteristic of "Battery Level" would be: [0x2A19]', required=True)
    

    ### parse/check arguments

    print "Getting args..."
    args = parser.parse_args()
    args_dict = vars(args)

    service_assigned_number = args_dict['service_assigned_number']
        
    characteristic_assigned_number_list = None    
    characteristic_assigned_number_list = eval(args_dict['characteristic_assigned_number_list'])
    
    ### prepare dbus stuff

    print "Preparing dbus..."
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    mainloop = GObject.MainLoop()

    
    ### create BLE service

    print "Creating BLE service..."

    service = service_template.create_read_notify_service(
        bus,
        0,
        service_assigned_number,
        True,
        characteristic_assigned_number_list
    )

    ### start BLE service
   
    service_template.start_services(mainloop, bus, args_dict['adapter_name'], [service])
    mainloop.run()

    # TODO: run another thread that reads from the mqtt server and updates the chrc on changes

    

if __name__ == '__main__':
    main()
