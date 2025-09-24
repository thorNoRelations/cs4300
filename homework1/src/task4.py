def calculate_discount(price, discount):

    if not (0 <= discount <= 100):
        raise ValueError("Discount must be between 0 and 100")

    return price * (1 - discount / 100)