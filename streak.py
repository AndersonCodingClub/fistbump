from datetime import date


class Streak:
    last_picture_date = None
    current_streak = 0
    
    @staticmethod
    def add_streak():
        current_date = date.today()
        Streak.check_streak()
        
        if Streak.last_picture_date is not None:
            if (current_date - Streak.last_picture_date).days == 1:
                Streak.current_streak += 1
                Streak.last_picture_date = current_date
        else:
            Streak.current_streak += 1
            Streak.last_picture_date = current_date
    
    @staticmethod
    def check_streak():
        if Streak.last_picture_date is not None:
            if (date.today() - Streak.last_picture_date).days >= 2:
                Streak.current_streak = 0