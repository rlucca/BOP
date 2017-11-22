import numpy as np
from time import ctime, localtime
from sys import argv, stdout
from os.path import basename
from glob import glob

if len(argv) != 3 or len(argv[1]) < 4 or len(argv[2]) < 4:
  print 'Usage: python {} directory_with_csvs output_file'.format(argv[0])
  exit(1)

def stats_from_file(filename):
  stdout.write('.')
  stdout.flush()
  ret = {}
  matrix = np.genfromtxt(filename, delimiter=';',dtype="S4,i8,i8,f16,f16,i8,f16")
  time = []
  result = []
  balance = []
  wins = []
  losses = []
  ties = []
  for node in np.atleast_1d(matrix):
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
    result.append(result_value)
  del matrix
  first_year = localtime(time[0]).tm_year
  last_year = localtime(time[-1]).tm_year
  ret['trading_years'] = (first_year, last_year)
  del time
  n_trades = len(result)
  n_win_trades = len(wins)
  n_loss_trades = len(losses)
  n_tie_trades = len(ties)
  ret['trades'] = {
      'total': n_trades,
        'win': n_win_trades,
       'loss': n_loss_trades,
        'tie': n_tie_trades,
    }
  del result
  del wins
  del losses
  del ties
  first_balance = balance[0]
  last_balance = balance[-1]
  ret['balance'] = (first_balance, last_balance)
  del balance
  ret['filename'] = basename(filename).split('.')[0].split('_')
  return ret

dir_path = argv[1]
output = argv[2]
with file(output, 'w') as fd:
  fd.write('first_operational_year;last_operational_year;initial_balance;final_balance;total_trades;win_trades;loss_trades;tie_trades;filename_elements...\n')
  line = 2
  files = glob(dir_path + '/*.csv')
  for filename in sorted(files):
    data = stats_from_file(filename)
    years = '{};{}'.format(data['trading_years'][0], data['trading_years'][1])
    balances = '{};{}'.format(data['balance'][0], data['balance'][1])
    trades = '{};{};{};{}'.format(data['trades']['total'], data['trades']['win'], data['trades']['loss'], data['trades']['tie'])
    elements = ';'.join(data['filename'])
    win_rate = '=F{}/SUM(F{}:H{})'.format(line, line, line)
    ppm = '=(F{}-G{}*1.5-H{}*0.5)/3'.format(line, line, line)
    fd.write(';'.join([years, balances, trades, elements, win_rate, ppm]))
    fd.write('\n')
    line += 1
print ''
