class NoHibpKeyFoundException(Exception):
    def __init__(self):
        self.message = str("No Hibp Key Found. Please make sure that your key exists in your environment.")
        super().__init__(self.message)