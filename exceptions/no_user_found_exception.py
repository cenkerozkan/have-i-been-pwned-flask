class NoUserFoundException(Exception):
    def __init__(self):
        self.message = "No user found with this credentials."
        super().__init__(self.message)
