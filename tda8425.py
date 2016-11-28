# -*- coding: utf8 -*-
# TDA8425 Sound processor for Raspberry Pi
# Python version version - Andrey Zagorets 27/11/2016
#
# This code is provided to help with programming the TDA chip.

import smbus
from functools import partial
from string import printable

TDA8425_ADDRESS	=	0x41  

TDA8425_VOLL 	=	0b00000000
TDA8425_VOLR	=	0b00000001
TDA8425_BASS	=	0b00000010
TDA8425_TREBLE	=	0b00000011
TDA8425_SWITCH	=	0b00001000

VOLUME_MASK		=	0x3F
BASS_MASK		=	0x0F
SOURCE_MASK		=	0x07
SIGNAL_MASK		=	0x18

TDA8425_IS_BIT	=	0b00000001
TDA8425_ML0_BIT	=	0b00000010
TDA8425_ML1_BIT	=	0b00000100
TDA8425_STL_BIT	=	0b00001000
TDA8425_EFL_BIT	=	0b00010000
TDA8425_MU_BIT	=	0x20


TDA8425_CHAN_1_STEREO	=	TDA8425_ML1_BIT | TDA8425_ML0_BIT
TDA8425_CHAN_2_STEREO	=	TDA8425_ML1_BIT | TDA8425_ML0_BIT | TDA8425_IS_BIT
TDA8425_CHAN_1_A		=	TDA8425_ML0_BIT
TDA8425_CHAN_1_B		=	TDA8425_ML1_BIT
TDA8425_CHAN_2_A		=	TDA8425_ML0_BIT | TDA8425_IS_BIT
TDA8425_CHAN_2_B		=	TDA8425_ML1_BIT | TDA8425_IS_BIT
TDA8425_MONO            =	0x00
TDA8425_LINEAR_STEREO	=	TDA8425_STL_BIT
TDA8425_PSEUDO_STEREO	=	TDA8425_EFL_BIT
TDA8425_SPATIAL_STEREO	=	TDA8425_EFL_BIT | TDA8425_STL_BIT


class TDA8425:

    def __init__(self, busnum = 1):
        # Create I2C device.
        
        self.bus = smbus.SMBus(busnum)
        self.tda8425_vaules = [0x3C, 0x3C, 0xF6, 0xF6, 0xCE]

    def write_chip(self, param, value):

        self.bus.write_byte_data(TDA8425_ADDRESS, param, value)

    def init_chip(self):

    	self.write_chip(TDA8425_VOLL, self.tda8425_vaules[0])
    	self.write_chip(TDA8425_VOLR, self.tda8425_vaules[1])
    	self.write_chip(TDA8425_TREBLE, self.tda8425_vaules[2])
       	self.write_chip(TDA8425_BASS, self.tda8425_vaules[3])
    	self.write_chip(TDA8425_SWITCH, self.tda8425_vaules[4])

    def set_param(self, param, value):

    	if param == TDA8425_VOLL or param == TDA8425_VOLR:
    		if value <= VOLUME_MASK:
    			self.tda8425_vaules[param] = self.tda8425_vaules[param] & ~VOLUME_MASK
    			self.tda8425_vaules[param] = self.tda8425_vaules[param] | value
    	elif param == TDA8425_BASS or param == TDA8425_TREBLE:
    		if value <= BASS_MASK:
    			self.tda8425_vaules[param] = self.tda8425_vaules[param] & ~BASS_MASK
    			self.tda8425_vaules[param] = self.tda8425_vaules[param] | value

    	self.write_chip(param, self.tda8425_vaules[param])

    def select_input(self, input):

    	self.tda8425_vaules[4] = self.tda8425_vaules[4] & ~SOURCE_MASK
    	self.tda8425_vaules[4] = self.tda8425_vaules[4] | input
    	self.write_chip(TDA8425_SWITCH, self.tda8425_vaules[4])

    def select_signal(self, input):

    	self.tda8425_vaules[4] = self.tda8425_vaules[4] & ~SIGNAL_MASK
    	self.tda8425_vaules[4] - self.tda8425_vaules[4] | input
    	self.write_chip(TDA8425_SWITCH, self.tda8425_vaules[4])

    def mute_on(self):

    	self.tda8425_vaules[4] = self.tda8425_vaules[4] | TDA8425_MU_BIT
    	self.write_chip(TDA8425_SWITCH, self.tda8425_vaules[4])

    def mute_off(self):

    	self.tda8425_vaules[4] = self.tda8425_vaules[4] & ~TDA8425_MU_BIT
    	self.write_chip(TDA8425_SWITCH, self.tda8425_vaules[4])

    def get_param(self, param):

    	if param == TDA8425_VOLL or param == TDA8425_VOLR:
    		return self.tda8425_vaules[param] & VOLUME_MASK
    	elif param == TDA8425_BASS or param == TDA8425_TREBLE:
    		return self.tda8425_vaules[param] & BASS_MASK

    def get_input(self):

    	return self.tda8425_vaules[4] & SOURCE_MASK

    def get_signal(self):

    	return self.tda8425_vaules[4] & SIGNAL_MASK

    def get_mute_state(self):

    	return (self.tda8425_vaules[4] & TDA8425_MU_BIT) >> 5
