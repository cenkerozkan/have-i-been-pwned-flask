class UserAlreadyExistsException(Exception):
    def __init__(self):
        self.message = "User with the same credentials already exists."
        super().__init__(self.message)