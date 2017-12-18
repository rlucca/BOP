import numpy as np
import matplotlib.pyplot as plt
from time import ctime, localtime
from sys import argv
from os import getenv
from os.path import basename

if len(argv) < 2:
  print 'Usage: python {} csv...'.format(argv[0])
  exit(1)

def get_colors(index):
  colors=['black', 'grey', 'silver', 'indianred', 'maroon', 'coral', 'chocolate', 'darkorange', 'goldenrod', 'olive', 'green', 'lightseagreen', 'teal', 'aqua', 'steelblue', 'darkblue', 'darkviolet', 'magenta', 'purple']
  return colors[index]

for (Index, filename) in enumerate(argv[1:]):
  matrix = np.genfromtxt(filename, delimiter=';',dtype="S4,i8,i8,f16,f16,i8,f16")
  time = []
  result = []
  balance = []
  wins = []
  consecutive_wins = []
  losses = []
  consecutive_losses = []
  ties = []
  consecutive_ties = []
  strike_tmp = 0

  for node in matrix:
    #time.append(ctime(node[2]))
    time.append(node[2])
    balance.append(node[6])
    if node[0] == 'WIN':
      result_value = 1
      wins.append(result_value)
    elif node[0] == 'LOSS':
      result_value = -1
      losses.append(result_value)
    else:
      result_value = 0
      ties.append(result_value)
    if len(result) > 0:
      if result[-1] == result_value:
        strike_tmp += 1
      else:
        if strike_tmp > 0:
          if result[-1] == 1:
            consecutive_wins.append(strike_tmp)
          elif result[-1] == -1:
            consecutive_losses.append(strike_tmp)
          elif result[-1] == 0:
            consecutive_ties.append(strike_tmp)
        strike_tmp = 0
    result.append(result_value)

  # check if after the last value, we have a strike
  if strike_tmp > 0 and len(result) > 0:
    if result[-1] == 1:
      consecutive_wins.append(strike_tmp)
    elif result[-1] == -1:
      consecutive_losses.append(strike_tmp)
    elif result[-1] == 0:
      consecutive_ties.append(strike_tmp)
    strike_tmp = 0

  def years(time):
    ret = []
    for t in time:
      Y = localtime(t).tm_year
      ret.append(Y)
    return ret

  max_fig = 18

  # Lets put the initial value!
  time = [time[0]] + time
  balance = [10000] + balance
  # Lets plot Time x Balance!
  #plt.figure((Index % max_fig))
  plt.plot(years(time), balance, '.', color=get_colors((Index % max_fig)))
  plt.ylabel('balance')
  plt.xlabel('time')

plt.show()
