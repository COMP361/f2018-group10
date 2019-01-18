

class PlayerModel(object):
    #  Should probably extend GameUnit once we make it
    def __init__(self):
        self.user_name = ""
        self.password = ""
        self.status = None  #  Should be some status enum

