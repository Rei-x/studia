coefficients = {
    "a": 31.46995209400817,
    "b": 1349.317640356113,
}


def model(area: int):
    return coefficients["a"] * area + coefficients["b"]


def is_occasional_rental(price: int, area: int):
    prediction = model(area)
    confidence = 0.2

    return price < prediction * (1 - confidence)
