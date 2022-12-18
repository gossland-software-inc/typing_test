import string
import random
import sys
import tty
import termios
import time
import datetime

N = 1
typed_key = ''
print( 4*string.digits + 2*'4589_=+' + string.punctuation)
start_time = time.time()
num_right=0
num_wrong=0
num_typed=0
num_test_keys=0
test_key=''
last_test_key=''
looping=True
new_key=False

while looping:
    test_key = ''.join(random.choices(4*string.digits + 2*'4589_=+' + string.punctuation, k=N))
    new_key = True
    while True:
        print(test_key, end=' ', flush=True)
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())          # Raw read
            typed_key = sys.stdin.read(1)
            if typed_key != 'q':
                num_typed = num_typed + 1
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        print(typed_key )
        if new_key and typed_key != 'q':
            num_test_keys = num_test_keys + 1
            new_key = False
        if typed_key == test_key:
            num_right = num_right + 1
            break
        if typed_key == 'q':
            break

    looping = typed_key != 'q'

    # while typed_key != test_key and typed_key != 'q':
    #     last_test_key = test_key
    #     if typed_key != '\n':
    #         print(test_key, end=' ', flush=True)
    #         num_wrong = num_wrong + 1
 
    #     if typed_key == test_key:
    #         num_right = num_right + 1

 
end_time = time.time()
duration = end_time - start_time
num_wrong = num_typed - num_right

output=''
result=''

if num_test_keys > 0:
    result='{0}\tkeys\t{1:0.1f}\tsecs\t{2:0.0f}\t%\t{3:.02f}\tkps'.format(num_test_keys, duration, 100*num_right/(num_wrong + num_right), num_right/duration)
    timestamp=datetime.datetime.now()
    output = '{0}\t{1}'.format(timestamp.strftime('%Y-%m-%d %H:%M:%S'), result)
    print(output)
    f = open("results.txt", "a")
    f.write(output + "\n")
    f.close()
else:
    print('No keys tested')

