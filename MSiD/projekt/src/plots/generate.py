import matplotlib.pyplot as plt
import seaborn as sns

from src.plots.area_regression import area_regression
from src.plots.distance_regression import distance_regression
from src.plots.mean_price_over_number_of_rooms import mean_price_over_number_of_rooms
from src.plots.price_over_time import price_over_time

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Palatino"],
    }
)
sns.set_theme(style="whitegrid", palette="pastel", font_scale=1.5)

if __name__ == "__main__":
    price_over_time()
    mean_price_over_number_of_rooms()
    area_regression()
    distance_regression()
