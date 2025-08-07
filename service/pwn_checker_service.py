from decorators.sinlgeton import singleton
from util.have_i_been_pwned_request_executor import HaveIBeenPwnedRequestExecutor

@singleton
class PwnCheckerService:
    def __init__(self):
        request_executor: HaveIBeenPwnedRequestExecutor = HaveIBeenPwnedRequestExecutor()

    def run(self):
        pass