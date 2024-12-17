class MPGAResponse:
    def __init__(self, code=200, result=None, message="", error=None):
        self.code = code
        self.result = result
        self.message = message
        self.error = error

    def __str__(self):
        return f"MPGAResponse({self.code}, {self.result}, '{self.message}', {self.error})"
    def __repr__(self):
        return f"ReturnObject(code={self.code}, result={self.result}, message='{self.message}', error={self.error})"