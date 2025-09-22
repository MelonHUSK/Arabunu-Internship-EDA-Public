import _datetime as date
import time

def countdown(t):
    total_time = 288000
    time_elapsed = 0

    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        print(timer, end="\r") 
        time.sleep(1)
        t -= 1
        time_elapsed += 1

    
    print("Sonunda bitti amk")

countdown(600)