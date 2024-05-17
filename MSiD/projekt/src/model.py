coefficients = {
    "a": 31.004356594755563,
    "b": 1366.825647292178,
}


def model(area: int):
    return coefficients["a"] * area + coefficients["b"]


def is_occasional_rental(price: int, area: int, margin=500):
    prediction = model(area)

    return price < prediction - margin
