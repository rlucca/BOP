import numpy as np
import matplotlib.pyplot as plt
from time import ctime, localtime
from sys import argv
from os import getenv

if len(argv) != 2 or len(argv[1]) < 4:
  print 'Usage: python {} csv'.format(argv[0])
  exit(1)

filename = argv[1]
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

# Lets put the initial value!
time = [time[0]] + time
balance = [10000] + balance
# Lets plot Time x Balance!
plt.plot(years(time), balance, '.', color='black')
plt.ylabel('balance')
plt.xlabel('time')

if getenv('NO_BALANCE', 0) == 0:
  plt.show()

show_only_balance = getenv('ONLY_BALANCE')
if show_only_balance and show_only_balance != 0:
  exit(0)

def calculate_delta(ar):
  ret = [ar[0]]
  last = ar[0]
  for T in ar[1:]:
    ret.append(T - last)
    last = T
  return ret

def calculate_data(ar):
  if len(ar) == 0:
    return (0, 0, 0)
  minimal = 9999999999999;
  maximal = -9999999999998;
  total = 0;
  for a in ar:
    if a < minimal:
      minimal = a
    if a > maximal:
      maximal = a
    total += a
  return (minimal, maximal, float(total)/float(len(ar)))

def number_of_repetitions(ar):
  from operator import itemgetter
  if len(ar) == 0:
    return (0, 0, 0, 0)
  H = {}
  for a in ar:
    try:
      H[a] = H[a] + 1
    except KeyError:
      H[a] = 1
  maximal = max(H.iteritems(), key=itemgetter(1))
  minimal = min(H.iteritems(), key=itemgetter(1))
  return (minimal[1], minimal[0]+1, maximal[1], maximal[0]+1)

def print_time(T_in_seconds):
  years = int(T_in_seconds / 31536000.0)
  remain = (T_in_seconds % 31536000.0)
  months = int(remain / 2592000)
  remain = (remain % 2592000)
  weeks = int(remain / 604800)
  remain = (remain % 604800)
  days = int(remain / 86400)
  remain = (remain % 86400)
  hours = int(remain / 3600)
  remain = (remain % 3600.0)
  minutes = int(remain / 60)
  remain = (remain % 60.0)
  seconds = int(remain)
  if years >= 1:
    return '{}y:{}m:{}w:{}d:{}h:{}m:{}'.format(years, months, weeks, days, hours, minutes, seconds)
  elif months >= 1:
    return '{}m:{}w:{}d:{}h:{}m:{}'.format(months, weeks, days, hours, minutes, seconds)
  elif weeks >= 1:
    return '{}w:{}d:{}h:{}m:{}'.format(weeks, days, hours, minutes, seconds)
  elif days >= 1:
    return '{}d:{}h:{}m:{}'.format(days, hours, minutes, seconds)
  elif hours >= 1:
    return '{}h:{}m:{}'.format(hours, minutes, seconds)
  return '{}m:{}'.format(minutes, seconds)

def calculate_time(ar, tp):
    #     min, hour, day, week,    month,  year
    tps = [60, 3600, 86400, 604800, 2592000, 31536000]
    tms = set()
    total = 0
    for a in ar:
      key = int(a / tps[tp])
      tms.add(key)
      total += 1
    return (total / float(len(tms)))

def spaces(T, tp):
  start = len('%2.2f' % calculate_time(T, tp))
  return ' ' * (12 - start)

# Show other data
print 'Interval to have a signal'
delta = calculate_delta(time[1:])
mi, ma, av = calculate_data(delta)
print 'Minimal: {}'.format(print_time(mi))
print 'Maximal: {}'.format(print_time(ma))
print 'Average: {}'.format(print_time(av))
print 'Average signals in'
print 'a year: %2.2f%sa month: %2.2f%sa week: %2.2f' % (calculate_time(time, 5), spaces(time, 5), calculate_time(time, 4), spaces(time, 4)[:-1], calculate_time(time, 3))
print ' a day: %2.2f%sa hour: %2.2f%sa minute: %2.2f' % (calculate_time(time, 2), spaces(time, 2), calculate_time(time, 1), spaces(time, 1), calculate_time(time, 0))
#print delta
last_year = localtime(time[-1]).tm_year
del time
del delta
print '-'*71
print 'Consecutive wins ({})'.format(len(consecutive_wins))
(mi, ma, a) = calculate_data(consecutive_wins)
print 'Minimal: %-10d Maximal: %-10d Average: %-10.3f' % (mi, ma, a)
(mir, mi, mar, ma) = number_of_repetitions(consecutive_wins)
print 'Minimal: %d (rep. %d) Maximal: %d (rep. %d)' % (mi, mir, ma, mar)
print 'Consecutive losses ({})'.format(len(consecutive_losses))
(mi, ma, a) = calculate_data(consecutive_losses)
print 'Minimal: %-10d Maximal: %-10d Average: %-10.3f' % (mi, ma, a)
(mir, mi, mar, ma) = number_of_repetitions(consecutive_losses)
print 'Minimal: %d (rep. %d) Maximal: %d (rep. %d)' % (mi, mir, ma, mar)
print 'Consecutive ties ({})'.format(len(consecutive_ties))
(mi, ma, a) = calculate_data(consecutive_ties)
print 'Minimal: %-10d Maximal: %-10d Average: %-10.3f' % (mi, ma, a)
(mir, mi, mar, ma) = number_of_repetitions(consecutive_ties)
print 'Minimal: %d (rep. %d) Maximal: %d (rep. %d)' % (mi, mir, ma, mar)
print '-'*71
print 'Total Trades: {}'.format(len(result))
print '  Wins: %-10d   Losses: %-10d   Ties: %-10d' % (len(wins), len(losses), len(ties))
if len(result) == 0: result.append(0)
print 'Wins %%: %-10.2f Losses %%: %-10.2f Ties %%: %-10.2f' % (len(wins) * 100.0 / len(result), len(losses) * 100.0 / len(result), len(ties) * 100.0 / len(result))
print '       Wins/Losses Rate %%: %-10.2f' % ((len(wins) * 100.0 / len(losses)) - 100.0)
print 'Wins/(Losses+Ties) Rate %%: %-10.2f' % ((len(wins) * 100.0 / (len(losses) + len(ties))) - 100.0)
ppm = (len(wins) * 1 + len(losses) * -1.5 + len(ties) * -0.5) / 3.0
print '                      PPM: %-10.2f' % (ppm)
print '-'*71
(mi, ma, a) = calculate_data(balance)
print 'Initial balance: {} -> {} ({})'.format(balance[0], balance[-1], last_year)
print 'Minimal: %-10.2f Maximal: %-10.2f Average: %-10.2f' % (mi, ma, a)
