from datetime import datetime
from datetime import date
from datetime import time
current_date_and_time = datetime.now()

print("The current date and time is", current_date_and_time)

# The current date and time is 2022-07-12 10:22:00.776664


print("The current date and time is", current_time)

class Streak:
    time_now = datetime.now()
    current_time = time_now.strftime("%H:%M:%S")
    last_streak_date_and_time = capture_last_streak()
    today = date.today()
    last_streak_date = None
    last_picture_date = None
  
    
    current_date_and_time = datetime.now()


    today = date.today()
    d1 = today.strftime("%m/%d/%y")
    current_streak = 0
   
    def check_streak(current_date_and_time, last_streak_date_and_time):
        if current_date_and_time - last_streak_date_and_time > 24:
            current_streak = 0
            return False
        else:
            return True
    def add_streak():
        if check_streak() == True and current_time == 23:59:59:
            current_streak += 1
            return current_streak


    def capture_last_streak():
        if """picturetaken""" and last_picture_date != date.today():
            last_picture_date = datetime.now()
            return last_picture_date
