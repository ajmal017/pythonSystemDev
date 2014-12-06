#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import numpy as np
import pandas as pd
import Queue

from abc import ABCMeta, abstractmethod

from event import SignalEvent

class Strategy(object):
 #ABC for strategy objects. Generates signals based on data from DataHandler
 __metaclass__ = ABCMeta

 @abstractmethod
 def calculate_signals(self):
  raise NotImplementedError("Should implement calculate_signals()")

