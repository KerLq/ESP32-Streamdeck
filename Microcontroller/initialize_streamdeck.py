from machine import Pin, SPI, SoftI2C
import ili9342c
import axp202c
import focaltouch
import sys
import client
from button import Button
from time import sleep


def initialize():
  global tft
  global touch

  axp = axp202c.PMU(address=0x34) # PMU einbinden
  axp.enablePower(axp202c.AXP192_LDO2) # Display anschalten
  axp.setDC3Voltage(3000) # Hintergrundbeleuchtung einstellen
  spi = SPI(2, baudrate=60_000_000,sck=Pin(18),mosi=Pin(23)) # SPI init
  tft = ili9342c.ILI9342C(spi,320,240,reset=Pin(33, Pin.OUT),
        cs=Pin(5, Pin.OUT),dc=Pin(15, Pin.OUT),rotation=0) # Display init

  tft.init()

  i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

  touch = focaltouch.FocalTouch(i2c)
  
  initialize_buttons()

def initialize_buttons():
  global buttons

  field = 3
  buttons = []

  field_width = tft.width() // field
  field_height = tft.height() // field

  button_keys = ["{F1}", "{F2}", "{F3}", "{F4}", "{F5}", "{F6}", "{F7}", "{F8}", "{F9}"]
  # button_texts = None
  button_texts = [["Stream starten", "Stream beenden"], ["Aufnahme starten", "Aufnahme beenden"], ["Aufnahme pausieren", "Aufnahme fortsetzen"], ["Mikrofon stummschalten", "Mikrofon stummschaltung aufheben"], ["Audio stummschalten", "Audio stummschaltung aufheben"], ["Kamera deaktivieren", "Kamera aktivieren"], "Szene", "Test", "Ben"]
  button_types = [["Start Streaming", "Stop Streaming"], ["Start Recording", "Stop Recording"], ["Pause Recording", "Resume Recording"], ["Mute Microphone", "Unmute Microphone"], ["Mute Audio Sound", "Unmute Audio Sound"], ["Disable Camera", "Enable Camera"], "Scene 1", "Scene 2", "Scene 3"]
  
  if button_texts is not None:
    if len(button_texts) is not (field * field):
      print("[ERROR] - Array button_texts must have", field * field, "elements!")
      sys.exit()

  if len(button_keys) is not (field * field):
    print("[ERROR] - Array button_keys must have", field * field, "elements!")
    sys.exit()

  if len(button_types) is not (field * field):
    print("[ERROR] - Array button_types must have", field * field, "elements!")
    sys.exit()
  
  i = 0

  for y in range(field):
    for x in range(field):
      position_x = x * field_width + 6
      position_y = y * field_height + 6

      if button_texts is None:
        buttons.append(Button(position_x, position_y,
                              field_width - 10, field_height - 10,
                              ili9342c.WHITE, tft,
                              button_types[i], button_keys[i],
                              button_types[i]))
      else:
        buttons.append(Button(position_x, position_y,
                              field_width - 10, field_height - 10,
                              ili9342c.WHITE, tft,
                              button_texts[i], button_keys[i],
                              button_types[i]))

      i +=1
          
def draw_interface():
  tft.fill(ili9342c.WHITE)

  for button in buttons:
    button.draw()
        
def reset_scene_button(previous_scene_button):
  if previous_scene_button is not None:
    redraw_button(previous_scene_button, ili9342c.WHITE)

def wait_for_screen_touch(socket_client):
  previous_scene_button = None
  
  while(True):
    update_button = True

    if (touch.touched == 1):
      x = touch.touches[0]['x']
      y = touch.touches[0]['y']
          
      for button in buttons:
        if(button.has_been_touched(x,y)):
          if(button.get_color() == ili9342c.WHITE):
            if "Scene" in button.get_type():
              reset_scene_button(previous_scene_button)
              previous_scene_button = button
            elif any([x in button.get_type() for x in ["Pause Recording", "Stop Recording"]]):
              for record_button in buttons:
                if "Start Recording" in record_button.get_type():
                  update_button = False

            if update_button:
              print(socket_client)
              socket_client.send(button.get_key())
              redraw_button(button, ili9342c.RED, text_foreground_color = ili9342c.WHITE, text_background_color = ili9342c.RED)
              sleep(1)
          else:
            if button == previous_scene_button:
              continue

            if "Stop Recording" in button.get_type():
              for resume_button in buttons:
                if "Resume Recording" in resume_button.get_type():
                  redraw_button(resume_button, ili9342c.WHITE)

            socket_client.send(button.get_key())
            redraw_button(button, ili9342c.WHITE, text_foreground_color = ili9342c.BLACK, text_background_color = ili9342c.WHITE)
            sleep(1)

def redraw_button(button, color, text_foreground_color = ili9342c.BLACK, text_background_color = ili9342c.WHITE):
  button.set_color(color)
  button.switch_text(button.get_text())
  button.switch_type(button.get_type())
  button.draw(text_foreground_color = text_foreground_color, text_background_color = text_background_color)
        
if __name__ == '__main__':
  socket_client = client.initialize()
  
  initialize()
  draw_interface()

  wait_for_screen_touch(socket_client)

