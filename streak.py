from datetime import date


class Streak:
    last_picture_date = None
    current_streak = 0
    
    def add_streak():
        current_date = date.today()
        Streak.check_streak()
        
        if Streak.last_picture_date is not None:
            if current_date != Streak.last_picture_date and current_date - Streak.last_picture_date == 1:
                Streak.current_streak += 1
                Streak.last_picture_date = current_date
        else:
            Streak.current_streak += 1
            Streak.last_picture_date = current_date
    
    @staticmethod
    def check_streak():
        if date.today() - Streak.last_picture_date >= 2:
            Streak.current_streak = 0