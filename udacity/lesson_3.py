

def create_profile(given_name, *surnames, **details):
    print(given_name, *surnames)
    for k,v in details.items():
        print(f"{k}: {v}")
    