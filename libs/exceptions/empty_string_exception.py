class EmptyStringException(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{self.code}] - {self.message}")
