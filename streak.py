from datetime import date
from database import Database


class Streak:
    def __init__(self, user_id: int):
        self.user_id = user_id
    
    def get_streak(self, current_streak: int, increment: bool=False) -> int:
        db = Database()
        rows = db.get_images(self.user_id)
        if len(rows) == 0:
            return 0
        elif len(rows) == 1:
            return 1
        else:
            most_recent_image_row = rows[-1]
            last_picture_date = most_recent_image_row[-1].date()
            current_date = date.today()
            day_difference = (current_date - last_picture_date).days
            
            if day_difference >= 2:
                return 0
            else:
                if increment and day_difference == 1:
                    return current_streak + 1
                else:
                    return current_streak