#!/usr/bin/python
#import evdev
from evdev import InputDevice, categorize, ecodes

import blinkt
 
def main_unit():
    path = "/proc/bus/input/devices"
    name = ""
    evhandler = ""

    with open(path) as f:
        content = f.readlines()

    for line in content:
        devide = line.split(':')
        if len(devide) > 0:
            if devide[0] == "N":
                name = devide[1]
                name = name[name.index('"')+1:name.rindex('"')]
#                print(name)

            if devide[0] == "H":
                handlers = devide[1]
                handlers = handlers[handlers.index("=")+1:].split(" ")
#                print(handlers)
                for handler in handlers:
                    if handler[:5] == "event":
                        evhandler = "/dev/input/{0}".format(handler)
                    if handler[:2] == "js":
                        type = "joystick"

    if type != "joystick":
        exit()

    #cree un objet gamepad | creates object gamepad
    try:
        gamepad = InputDevice(evhandler)
    except Exception as err:
        exit()
  

    #affiche la liste des device connectes | prints out device info at start
#    print(gamepad)
   
    flagA = 0
    #affiche les codes interceptes |  display codes
    for event in gamepad.read_loop():
        #Boutons | buttons 
        if event.type == ecodes.EV_KEY:
#            print event.code
            if event.code == 288:
                # buttonA
                blinkt.set_pixel(0, 255, 0, 0)
                blinkt.show()
            elif event.code == 289:
                # buttonB
                blinkt.set_pixel(1, 255, 255, 0)
                blinkt.show()
            elif event.code == 290:
                # buttonY
                blinkt.set_pixel(2, 0, 0, 255)
                blinkt.show()
            elif event.code == 291:
                # buttonX
                blinkt.set_pixel(3, 0, 255, 0)
                blinkt.show()
            elif event.code == 292:
                # buttonL
                blinkt.set_pixel(4, 0, 255, 255)
                blinkt.show()
            elif event.code == 293:
                # buttonR
                blinkt.set_pixel(5, 128, 255, 128)
                blinkt.show()
            elif event.code == 294:
                # buttonSelect
                for i in range(blinkt.NUM_PIXELS):
                    blinkt.set_pixel(i, 0, 0, 0)
                    blinkt.show()
            elif event.code == 295:
                # buttonStart
                for i in range(blinkt.NUM_PIXELS):
                    blinkt.set_pixel(i, 0, 0, 0)
                    blinkt.show()
        #Gamepad analogique | Analog gamepad
        elif event.type == ecodes.EV_ABS:
            absevent = categorize(event)
#            print ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value
            if absevent.event.code == 0:
                if absevent.event.value == 255:
                    blinkt.set_pixel(6, 255, 0, 255)
                    blinkt.show()
                elif absevent.event.value == 0:
                    blinkt.set_pixel(6, 0, 0, 0)
                    blinkt.show()
            elif absevent.event.code == 1:
                if absevent.event.value == 255:
                    blinkt.set_pixel(7, 0, 128, 128)
                    blinkt.show()
                elif absevent.event.value == 0:
                    blinkt.set_pixel(7, 0, 0, 0)
                    blinkt.show()

def daemonize():
    pid = os.fork()
    if pid > 0:
        pid_file = open('/var/run/python_daemon.pid','w')
        pid_file.write(str(pid)+"\n")
        pid_file.close()
        sys.exit()

    if pid == 0:
        main_unit()

if __name__ == '__main__':
    main_unit()

#    while True:
#        daemonize()
