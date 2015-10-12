#!/usr/bin/python

import time
import datetime
from Adafruit_LEDBackpack import LEDBackpack

# ===========================================================================
# 7-Segment Display
# ===========================================================================

# This class is meant to be used with the four-character, seven segment
# displays available from Adafruit

class SevenSegment:
  disp = None

  # Some 7Segment-Display have several different colons, e.g. the
  # 1,2" display. To seperately control such different colons
  # use the following values where applicable:
  #
  # 0x00 - nothing
  # 0x02 - center colon
  # 0x04 - left colon - upper dot
  # 0x08 - left colon - lower dot
  # 0x10 - decimal point
  # 0xFFFF - everything (default)
  mask_colons = 0xFFFF
 
  # Hexadecimal character lookup table (row 1 = 0..9, row 2 = A..F)
  DIGITS_NORMAL = [ 0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F, \
                    0x77, 0x7C, 0x39, 0x5E, 0x79, 0x71 ]
  DIGITS_INVERTED = [ 0x3F, 0x30, 0x5B, 0x79, 0x74, 0x6D, 0x6F, 0x38, 0x7F, 0x7D, \
                      0x7E, 0x67, 0x0F, 0x73, 0x4F, 0x4E ]
  digits = DIGITS_NORMAL
  display_inverted = False
  
  # Constructor
  def __init__(self, address=0x70, debug=False):
    if (debug):
      print "Initializing a new instance of LEDBackpack at 0x%02X" % address
    self.disp = LEDBackpack(address=address, debug=debug)

  def invertDisplay(self):
    if (self.display_inverted): # we were inverted, so switch back to normal
      self.digits = self.DIGITS_NORMAL
      self.display_inverted = False
    else:                       # we were displaying normally, so switch to inverted
      self.digits = self.DIGITS_INVERTED
      self.display_inverted = True
  
  def writeDigitRaw(self, charNumber, value):
    "Sets a digit using the raw 16-bit value"
    if (charNumber > 7):
      return
     if ((self.display_inverted) & (charNumber < 5)):
      "if inverted we need to use reverse character positioning"
      charNumber = 4 - charNumber
    # Set the appropriate digit
    self.disp.setBufferRow(charNumber, value)

  def writeDigit(self, charNumber, value, dot=False):
    "Sets a single decimal or hexademical value (0..9 and A..F)"
    if (charNumber > 7):
      return
    if (value > 0xF):
      return
    if ((self.display_inverted) & (charNumber < 5)):
      "if inverted we need to use reverse character positioning"
      charNumber = 4 - charNumber
    # Set the appropriate digit
    self.disp.setBufferRow(charNumber, self.digits[value] | (dot << 7))

  def setColon(self, state=True):
    "Enables or disables the colon character"
    # Warning: This function assumes that the colon is character '2',
    # which is the case on 4 char displays, but may need to be modified
    # if another display type is used
    
    if (state):
      self.disp.setBufferRow(2, self.mask_colons)
    else:
      self.disp.setBufferRow(2, 0)

