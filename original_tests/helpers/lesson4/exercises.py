
from udacity.lesson4.final import DefaultPortal

class FakePortal(DefaultPortal):
    def __init__(self, products=None, users=None):
        if not products:
            products = set()
        if not users:
            users = set()
        self.products = products
        self.users = users
        self.reviews = set()

    @classmethod
    def with_keyboard(cls, keyboard):
        return cls(products={keyboard})