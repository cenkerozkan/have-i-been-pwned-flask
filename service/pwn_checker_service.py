from decorators.singleton import singleton
from util.hibp_client import HaveIBeenPwnedRequestExecutor

@singleton
class PwnCheckerService:
    def __init__(self):
        request_executor: HaveIBeenPwnedRequestExecutor = HaveIBeenPwnedRequestExecutor()

    def run(self):
        pass