import sys
sys.path.append('.')
import aoc
import math

data_rows = aoc.get_input(25, sample=False, index=0).splitlines()

snafu_char_map = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}

def snafu_to_dec(chars):
  out = 0
  for exp, char in enumerate(reversed(chars)):
    place = int(math.pow(5, exp))
    out += snafu_char_map[char] * place
  return out

def dec_to_snafu_hack(val):
  snafu_chars = ""
  exp = int(math.log(val, 5)) + 1
  while exp >= 0:
    place = int(math.pow(5, exp))
    place_val = int(math.floor(val/place))
    snafu_chars += str(place_val)
    val = int(val % place)
    # print(f"Place: {place}, val: {place_val}, rem: {val}")
    exp -= 1
  return snafu_chars

def snafu_hack_to_snafu(snafu_hack):
  snafu = ""
  carry = 0
  for char in reversed(snafu_hack):
    num = int(char) + carry
    if num in [0, 1, 2]:
      snafu += str(num)
      carry = 0
    elif num == 3:
      snafu += "="
      carry = 1
    elif num == 4:
      snafu += "-"
      carry = 1
    elif num == 5:
      snafu += "0"
      carry = 1
    else:
      raise ValueError(f"Invalid value {num}")
  snafu = "".join([c for c in reversed(snafu)])
  if snafu[0] == "0":
    snafu = snafu[1:]
  return snafu


def part1():
  snafu_nums = data_rows
  total_dec = 0
  for num in snafu_nums:
    dec_num = snafu_to_dec(num)
    total_dec += dec_num
    # print(f"snafu: {num}, dec: {dec_num}, snafu hack: {hack_snafu}, snafu2: {snafu}")
    # print("")

  print(total_dec)
  hack_snafu = dec_to_snafu_hack(total_dec)
  snafu = snafu_hack_to_snafu(hack_snafu)
  print(snafu)

part1()

#def part2():
#  pass

#part2()