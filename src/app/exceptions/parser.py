
class ListProductError(Exception):
    def __init__(self):
        self.message = "There is no list of products on the website."
        super().__init__(self.message)
        