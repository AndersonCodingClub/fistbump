from datetime import datetime
from datetime import date
from datetime import time
import time 



class Streak:
   

    current_picture_date = None
    last_picture_date = None
    current_streak = 0


    def capture_last_picture_date():
        if current_picture_date == None:
            current_picture_date = date.today()
        else:
            last_picture_date = current_picture_date
            current_picture_date = date.today()
        return last_picture_date
   
    def add_streak(last_picture_date, current_picture_date):
        if current_streak == 0 or last_picture_date == None:
            current_streak += 1
        elif last_picture_date != None and < current_picture_date and (current_picture_date - last_picture_date) == 1:
            current_streak += 1
    def remove_streak(last_picture_date, current_picture_date):
        if current_picture_date - last_picture_date >= 2:
            current_streak = 0
    
    
    
    capture_last_picture_date()
    capture_last_streak()