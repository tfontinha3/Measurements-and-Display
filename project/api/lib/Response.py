class Response:
    def __init__(self, status: bool, code: int, body: any):
        self.status = status
        self.code = code
        self.body = body