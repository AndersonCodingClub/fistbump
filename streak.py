from datetime import date
from database import Database


class Streak:
    def __init__(self, user_id: int):
        self.user_id = user_id
        
    def handle_streak(self, increment: bool=False) -> int:
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
                if increment:
                    return db.set_streak(self.user_id, 1)
                else:
                    return db.set_streak(self.user_id, 0)
            else:
                if increment and day_difference == 1:
                    return db.increment_streak(self.user_id)
                else:
                    return db.get_streak(self.user_id)