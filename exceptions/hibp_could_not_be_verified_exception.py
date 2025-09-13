class HibpCouldNotBeVerifiedException(Exception):
    def __init__(self):
        self.message = str(
            "Your API could not be verified by the hibp platform. Make sure your subscription exists."
        )
        super().__init__(self.message)
