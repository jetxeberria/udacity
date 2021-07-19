class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.reviews = []

    def write_review(self, content, product):
        review = Review(content, self, product)
        self.reviews.append(review)
        product.reviews.append(review)

    def sell_product(self, name, description, price):
        product = Product(name, description, price, self, available=True)
        print(f"{product} is on the market!")
        return product

    def buy_product(self, product):
        if product.available:
            print(f"{self} is buying {product}.")
            product.available = False
        else:
            print(f"{product} is no longer available.")

    def __str__(self):
        return f"User(id={self.id}, name={self.name})"

class Review:
    def __init__(self, content, user, product):
        self.content = content
        self.user = user
        self.product = product

    def __str__(self):
        return f"Review of {self.product} by {self.user}: '{self.content}'"

class Product:
    def __init__(self, name, description, seller, price, availability):
        self.name = name
        self.description = description
        self.seller = seller
        self.reviews = []
        self.price = price
        self.availability = availability

    def __str__(self):
        return f"Product({self.name}, {self.description}) at ${self.price}"
