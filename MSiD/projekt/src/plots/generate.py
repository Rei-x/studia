import matplotlib.pyplot as plt
import seaborn as sns

from src.plots.area_regression import area_regression
from src.plots.difference_in_price_of_best_offers import (
    difference_in_price_of_best_offers,
)
from src.plots.distance_regression import distance_regression
from src.plots.distribution_price import price_distribution
from src.plots.mean_price_over_number_of_rooms import mean_price_over_number_of_rooms
from src.plots.model_vs_data import model_vs_data
from src.plots.preliminary_analysis import preliminary_analysis
from src.plots.price_over_time import price_over_time
from src.plots.rooms_price_distribution import rooms_price_distribution

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Palatino"],
    }
)
sns.set_theme(style="whitegrid", font_scale=1.5, palette="bright")

if __name__ == "__main__":
    preliminary_analysis()
    price_over_time()
    mean_price_over_number_of_rooms()
    area_regression()
    distance_regression()
    price_distribution()
    model_vs_data()
    difference_in_price_of_best_offers()
    rooms_price_distribution()
