from utils import get_date


class Person:
    def __init__(self, chat_id, age=None, dist_id=[],  dose_type=None, pincodes=[], notify=True, vaccine=None,
                 fee_type=None, min_slots=1, check_date=get_date()):
        self.check_date = check_date
        self.min_slots = min_slots
        self.fee_type = fee_type
        self.vaccine = vaccine
        self.dose_type = dose_type
        self.notify = notify
        self.pincodes = pincodes
        self.dist_id = dist_id
        self.age = age
        self.chat_id = chat_id

    def add_dist(self, new_dist_id):
        self.dist_id.append(new_dist_id)

    def remove_dist(self, new_dist_id):
        if new_dist_id in self.dist_id:
            self.dist_id.remove(new_dist_id)

    def add_pin(self, new_pin):
        self.dist_id.append(new_pin)

    def remove_pin(self, new_pin):
        if new_pin in self.pincodes:
            self.dist_id.remove(new_pin)
