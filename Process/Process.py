import struct
from ctypes import *

import psutil
import win32api
import win32process

from .Structures import *
from Utils import time

import logging
logger = logging.getLogger()

class Process():

  def __init__(self, proc_name):
    start = time.now()
    self.name = proc_name
    self.pid = self.get_pid(self.name)
    SetLastError(0)

    # Game
    self.proc_handler = windll.kernel32.OpenProcess(0x1F0FFF, 0, self.pid)

    # Modules
    self.modules = self.get_modules()

    self.parser_memory = {}
    self.parser_converter = {
        c_byte 	: 'c',
        c_int	: 'i',
        c_float	: 'f',
        c_bool	: '?'
    }

    logger.info(f'Process {self.name} found with PID -> {self.pid} | {len(self.modules)} modules loaded | {round(time.diff(start), 2)}ms')

  @staticmethod
  def get_pid(targetName):
    if targetName[::-1][0:4] == "exe.":
      targetName = targetName[0:-4]
    for proc in psutil.process_iter():
      try:	name = proc.name()
      except Exception:
        pass
      if name == f"{targetName}.exe": return proc.pid
    raise Exception("Process not found.")

  @staticmethod
  def Pack(st):
    buffer = create_string_buffer(sizeof(st))
    memmove(buffer, addressof(st), sizeof(st))
    return buffer.raw

  def parse_struct(self, struct):
    if struct in self.parser_memory:
      return self.parser_memory[struct]
    string = ""
    try:
        for attribute in struct._fields_:
            # <class 'Process.Structures.c_byte_Array_16'>
            if("c_byte_Array" in str(attribute[1])):
                string += f"{sizeof(attribute[1])}s"
                continue
            string += self.parser_converter[attribute[1]]
        self.parser_memory[struct] = string
        return string
    # If type is not a c_types structure
    except AttributeError:
        return self.parser_converter[struct]

  def get_modules(self):
    modules = {}
    for hModule in win32process.EnumProcessModulesEx(self.proc_handler, win32process.LIST_MODULES_ALL):
        modulepath = win32process.GetModuleFileNameEx(self.proc_handler, hModule)
        modules[modulepath.split('\\')[-1]] = hModule
    return modules

  def read(self, address, data_type):
    start = time.now()
    size = sizeof(data_type)
    read = c_ulonglong(0)
    buffer = (c_byte * sizeof(data_type))()
    RPM(self.proc_handler, address, buffer, size, byref(read))
    result = None
    try:
      data = list(struct.unpack(self.parse_struct(data_type), buffer))
    except AttributeError:
      data = list(struct.unpack(self.parse_struct(data_type), buffer))
    if len(data) > 1:
      for i in range(len(data)):
        if type(data[i]) == bytes:
          data[i] = (c_byte * len(data[i]))(*[j for j in data[i]])
      result = data_type(*data)
    else:
      result = data[0]
    if (diff := time.diff(start)) > 5.0:
      logger.debug(f'took {time.diff(start)}ms to read {size} bytes of data')
    return result

  def write(self, address, data, data_type):
    start = time.now()
    try:
      buffer = Process.Pack(data)
    except TypeError:
      buffer = Process.Pack(data_type(data))
    WPM(self.proc_handler, address, buffer, sizeof(data_type), byref(c_ulonglong(0)))
    if (diff := time.diff(start)) > 5.0:
      logger.debug(f'took {time.diff(start)}ms to write {sizeof(data_type)} bytes of data')


