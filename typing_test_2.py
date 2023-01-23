import string
import random
import sys
import tty
import termios
import time
import datetime

if len(sys.argv) > 1:
    remind_at = int(sys.argv[1])
else:
    remind_at = 100
N = 1
typed_key = ''
char_list = 4*string.digits + 2*'4589_=+' + string.punctuation
print( 'Test of {0} keys'.format(remind_at))
print( char_list )
print( "Enter 'q' to quit")
start_time = time.time()
num_right=0
num_wrong=0
num_typed=0
num_test_keys=0
test_key=''
last_test_key=''
quit_now=False

random.seed()

while True:
    test_key = ''.join(random.choices(char_list, k=N))
    num_test_keys = num_test_keys + 1
    typed_key = '';
    while typed_key != test_key:
        print(test_key, end=' ', flush=True)
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())          # Raw read
            typed_key = sys.stdin.read(1)
            num_typed = num_typed + 1
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        print(typed_key )
        if typed_key == test_key:
            num_right = num_right + 1
        if num_test_keys % remind_at == 0:
            print('\n{0} test keys ----------------'.format(num_test_keys))
            quit_now = True
            break
        if (typed_key == 'q') and (test_key != 'q'):
            break

    if quit_now:
        break

    if (typed_key == 'q') and (test_key != 'q'):
        num_typed = num_typed - 1
        break

end_time = time.time()
duration = end_time - start_time
num_wrong = num_typed - num_right


print('{0} test keys, {1} typed keys, {2} right keys, {3} wrong keys'.format(num_test_keys, num_typed, num_right, num_wrong))

output=''
result=''

if num_wrong + num_right   > 0:
    result='{0}\tkeys\t{1:0.1f}\tsecs\t{2:0.0f}\t%\t{3:.02f}\tkps'.format(num_test_keys, duration, 100*num_right/(num_wrong + num_right), num_right/duration)
    timestamp=datetime.datetime.now()
    output = '{0}\t{1}'.format(timestamp.strftime('%Y-%m-%d %H:%M:%S'), result)
    print(output)
    f = open("results.txt", "a")
    f.write(output + "\n")
    f.close()
else:
    print('No keys tested')

