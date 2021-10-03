class BlogInfoException(Exception):
    ...


class BlogInfoNotFoundError(BlogInfoException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Blog Not Found"


class BlogInfoInfoAlreadyExistError(BlogInfoException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Slug has been already used"
