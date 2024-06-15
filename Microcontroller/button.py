import ili9342c
import vga2_8x8 as font
import sys

class Button:
  def __init__(self, x, y, width, height, color, tft, text, key, button_type):
    self.__x = x
    self.__y = y
    self.__width = width
    self.__height = height
    self.__color = color
    self.__tft = tft

    if type(text) is list:
      self.__texts = text
      self.__text = text[0]
    else:
      self.__text = text

    self.__key = key

    if type(button_type) is list:
      self.__button_types = button_type
      self.__button_type = button_type[0]
    else:
      self.__button_type = button_type
      
  def set_color(self, color):
    self.__color = color
      
  def get_color(self):
    return self.__color
  
  def get_text(self):
    return self.__text
  
  def get_key(self):
    return self.__key
  
  def get_type(self):
    return self.__button_type

  def switch_text(self, current_text):
    if '__texts' in dir(self):
      if current_text == self.__texts[0]:
        self.__text = self.__texts[1]
      else:
        self.__text = self.__texts[0]

  def switch_type(self, current_type):
    if '__button_types' in dir(self):
      if current_type == self.__button_types[0]:
        self.__button_type = self.__button_types[1]
      else:
        self.__button_type = self.__button_types[0]
          
  def draw(self, text_foreground_color = ili9342c.BLACK, text_background_color = ili9342c.WHITE):
    self.__tft.rect(self.__x-1,self.__y-1,self.__width+2,self.__height+2,ili9342c.BLACK) 
    self.__tft.rect(self.__x-2,self.__y-2,self.__width+4,self.__height+4,ili9342c.BLACK)
    self.__tft.rect(self.__x-3,self.__y-3,self.__width+6,self.__height+6,ili9342c.BLACK)
    self.__tft.fill_rect(self.__x, self.__y, self.__width, self.__height, self.__color)

    if self.__text != None:
      text_list = self.__text.split()
     
      while True:
        text_lengths = []
        successful = True
                  
        for i in range(0, len(text_list)):
          if len(text_list[i]) >= 10:
            temporary_word = text_list[i]
            text_list.remove(text_list[i])

            text_list.insert(i, temporary_word[:len(temporary_word)//2])
            text_list.insert(i + 1, temporary_word[len(temporary_word)//2:])
            
            text_lengths.append(len(temporary_word[:len(temporary_word)//2]))
            text_lengths.append(len(temporary_word[len(temporary_word)//2:]))
          else:
            text_lengths.append(len(text_list[i]))
    
        for length in text_lengths:
          if length >= 10:
            successful = False
          
        if successful:
          break
       
      if len(text_list) > 4:
        print("Your word is too long!")  
        sys.exit()

      splitted_text = list(reversed(text_list))
      total_words_count = len(text_list)
      
      padding = 0
      if total_words_count == 4:
        padding = 8
      
      for i in range(0, total_words_count):
        self.__tft.text(font, splitted_text[i],
                        (self.__x + int(self.__width / 2)) - (len(splitted_text[i]) * 4),
                        self.__y + (int(self.__height / 2) - (10 * i)) + padding,
                        text_foreground_color, text_background_color)

  def has_been_touched(self, touch_x, touch_y):
    button_range_w_left = self.__x
    button_range_w_right = self.__x + self.__width
    
    button_range_h_upper = self.__y
    button_range_h_lower = self.__y + self.__height
    
    if(touch_x >= button_range_w_left and touch_x <= button_range_w_right):
      if(touch_y >= button_range_h_upper and touch_y <= button_range_h_lower):
        return True
        
    return False