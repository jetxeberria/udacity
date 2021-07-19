

class ProductNotFoundError(Exception):
    pass


class DefaultPortal():
    def __init__(self):
        self.products = set()
        self.users = set()
        self.reviews = set()

    def add_user(self, user):
        self.users.add(user)

    

class User():
    portal = DefaultPortal()

    def __init__(self, user_id, username, portal = None):
        if portal:
            self.portal = portal
        self.user_id = user_id
        self.username = username
        self.portal.add_user(self)

    def sell_product(self, product_name, description, price):
        details = [
            self.portal,
            self.username,
            product_name,
            description,
            price 
        ]
        product = Product(*details)
        self.portal.products.add(product)
        return product

    def buy_product(self, product):
        try:
            self.portal.products.remove(product)
        except KeyError as err:
            print(err)
            raise ProductNotFoundError
        
            
    def write_review(self, review, product):
        review = Review(product, review, self)
        self.portal.reviews.add(review)
        return review

    @property
    def reviews(self):
        return [
            rev
            for rev in self.portal.reviews
            if rev.reviewer == self
        ]


class Review():
    def __init__(self, product, description, reviewer):
        self.product = product
        self.description = description
        self.reviewer = reviewer
        
    
    def __contain__(self, review):
        return review in self.reviews
        

class Product():
    def __init__(self, portal, seller, name, description, price):
        self.portal = portal
        self.seller = seller
        self.name = name
        self.description = description
        self.price = price 

    
    @property
    def available(self):
        return self in self.portal.products

    @property
    def reviews(self):
        return [
            rev
            for rev in self.portal.reviews
            if rev.product == self
        ]
