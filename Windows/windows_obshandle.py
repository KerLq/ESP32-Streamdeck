import sys
import logging
from importlib import import_module
from run_once_wrapper import run_once

libnames = ['win32gui', 'pywinauto']
global already_imported

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def get_obs_handle():
  def callback(hwnd, obs_handle):
    if "OBS" in win32gui.GetWindowText(hwnd):
      obs_handle.append(hwnd)

  obs_handle = []
  win32gui.EnumWindows(callback, obs_handle)

  if obs_handle:
    return obs_handle[0]
  
  return None


@run_once
def validate_modules():
  for libname in libnames:
    try:
      lib = import_module(libname)
    except:
      logging.info("Install pywinauto from GitHub to make use of it:" 
                  "https://github.com/pywinauto/pywinauto/releases")

      logging.info("Install win32gui from GitHub to make use of it:"
                  "https://github.com/mhammond/pywin32/releases")
      sys.exit()
    else:
      globals()[libname] = lib
    

def send(hotkey): 
  validate_modules()
 
  obs_handle = get_obs_handle()

  if not obs_handle:
    logging.warning("Cannot find OBS!")
  else:
    app = pywinauto.application.Application().connect(handle=obs_handle)
    app.top_window().send_keystrokes(hotkey)
