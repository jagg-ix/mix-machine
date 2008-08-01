# in, out, ioc (c_code = 35..37)

# ALL DONE

from word_parser import *
from errors import *

def _get_device(vmachine):
  num = WordParser.get_field(vmachine)
  if num in vmachine.devices:
    return vmachine[num]
  else:
    raise InvalidDeviceError(num)

def ioc(vmachine):
  vmachine.cycles += 1
  _get_device(vmachine).control()

def _in_out(vmachine):
  vmachine.cycles += 1
  dev = _get_device(vmachine)
  addr = WordParser.get_full_addr(vmachine, check_mix_addr = True)
  words_num = dev.block_size/5
  if not vmachine.check_mem_addr(addr + words_num - 1):
    raise IOMemRangeError( (words_num, addr, addr + words_num - 1) )

  # locked checking

  return (dev, addr, words_num)

def _in(vmachine):
  dev, addr, words_num = _in_out(vmachine)

  bytes = dev.read()
  for i in xrange(words_num):
    vmachine[addr + i].word_list[1:6] = bytes[5*i: 5*(i + 1)]

def out(vmachine):
  dev, addr, words_num = _in_out(vmachine)

  bytes = []
  for i in xrange(words_num):
    bytes += vmachine[addr + i].word_list[1:6]
  dev.write(bytes)
