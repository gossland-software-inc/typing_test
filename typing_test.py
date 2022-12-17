import string
import random
import sys
import tty
import termios
import time
 
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
#num_right = num_typed - num_wrong

#print('keys: {0}, typed {1}, right: {2}, wrong: {3}'.
#      format(num_test_keys, num_typed, num_right, num_wrong))
if num_test_keys > 0:
    print('{0} keys in {1:0.1f} secs, {2:0.0f}% accuracy at {3:.02f} keys per second'.
        format(num_test_keys, duration, 100*num_right/(num_wrong + num_right), num_right/duration))
else:
    print('Duration: {0:.0f},  no keys tested')
