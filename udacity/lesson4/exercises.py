INVALID_PASSWORDS = (
    'password',
    'abc123',
    '123abc',
)

def debug_fn(fn):
    def wrapper(*args, **kwargs):
        print(f"{fn}. args: {fn.__dict__}")
        return fn(*args, **kwargs)
    return wrapper

def validate_password(username, password):
    valid = password != username and password not in INVALID_PASSWORDS
    if not valid:
        raise InvalidPasswordError

#@debug_fn
def create_account(username, password):
    validate_password(username, password)
    return (username, password)


def main(username, password):
    try:
        account = create_account(username, password)
    except InvalidPasswordError:
        print("Oh no!")

class InvalidPasswordError(Exception):
    def __init__(self):
        print("Password given is invalid")

    

    
if __name__ == '__main__':
    main('jim', 'jam')
    main('admin', 'password')  # Oh no!
    main('guest', 'guest')  # Oh no!