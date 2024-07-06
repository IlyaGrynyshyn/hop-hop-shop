class ProductAlreadyExistException(Exception):
    def __init__(self):
        self.message = f"Product is already exist."
        super().__init__(self.message)


class ProductNotExistException(Exception):
    def __init__(self):
        self.message = f"Product does not exist."
        super().__init__(self.message)
