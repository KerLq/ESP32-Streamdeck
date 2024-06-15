import os
import sys
import logging
from shutil import which
from run_once_wrapper import run_once

XDOTOOL = "xdotool"
#### xdotool only works for X11 and not for wayland! ####

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

@run_once
def checkIfXdotoolIsInstalled():
  if which(XDOTOOL) is None:
    logging.info('xdotool is not installed!')
    logging.info('Install xdotool: sudo apt install xdotool')
    sys.exit()

def send(hotkey):
  checkIfXdotoolIsInstalled()

  obs_exists = os.system('xdotool search --name "OBS "') # Sucht nach Fenstertitel
  
  if obs_exists == 256:
    logging.info('OBS is not open!')
    sys.exit()
  else:
    hotkey = hotkey.replace('{', '').replace('}', '')
    os.system(f'xdotool search --name "OBS " key --window %1 {hotkey}')