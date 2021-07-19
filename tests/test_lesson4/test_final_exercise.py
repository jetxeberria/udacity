import pytest
import udacity.lesson4.final as l4f
import tests.helpers.lesson4.exercises as l4h

@pytest.fixture
def portal():
    return l4h.FakePortal()

@pytest.fixture
def portal_with_keyboard(keyboard):
    portal = keyboard.portal
    portal.products.add(keyboard)
    return portal

@pytest.fixture
def brianna(portal):
    user_id = 1
    user_name = 'Brianna'
    return l4f.User(user_id, user_name, portal=portal)    

@pytest.fixture
def mary(portal):
    user_id = 2
    user_name = 'Mary'
    return l4f.User(user_id, user_name, portal=portal)    


@pytest.fixture
def keyboard(portal, brianna):
    return l4f.Product(portal, brianna, 'Keyboard', 'A nice mechanical keyboard', 100)

# brianna = User(1, 'Brianna')
# mary = User(2, 'Mary')
def test_user_g_no_user_w_created_t_exists(portal):
    user_id = 1
    user_name = 'Brianna'
    brianna = l4f.User(user_id, user_name, portal=portal)
    assert brianna.user_id == user_id and brianna.username == user_name
    assert brianna in portal.users

# mary.buy_product(keyboard)
def test_user_g_no_product_w_buy_t_error(mary, portal, keyboard):
    with pytest.raises(l4f.ProductNotFoundError):
        mary.buy_product(keyboard)

# keyboard = brianna.sell_product('Keyboard', 'A nice mechanical keyboard', 100)
# print(keyboard.available)  # => True
def test_user_g_no_product_w_sell_t_available_with_seller(brianna):
    brianna.sell_product('Keyboard', 'A nice mechanical keyboard', 100)
    portal = brianna.portal
    keyboard = None
    for prod in portal.products:
        if "Keyboard" is prod.name:
            keyboard = prod
    assert keyboard and keyboard.available

# mary.buy_product(keyboard)
# print(keyboard.available)  # => False
def test_user_g_product_w_buy_t_owned_and_not_available(portal_with_keyboard):
    user_id = 2
    user_name = 'Mary'
    mary = l4f.User(user_id, user_name, portal=portal_with_keyboard)  
    keyboard = list(portal_with_keyboard.products)[0]
    assert keyboard.available
    mary.buy_product(keyboard)
    assert not keyboard.available

# review = mary.write_review('This is the best keyboard ever!', keyboard)
# review in mary.reviews  # => True
# review in keyboard.reviews  # => True
def test_user_g_no_review_w_review_t_in_product_and_user(mary, keyboard):
    review = mary.write_review('This is the best keyboard ever!', keyboard)
    assert review in mary.reviews
    assert review in keyboard.reviews


