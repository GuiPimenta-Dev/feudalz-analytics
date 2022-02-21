import matplotlib.pyplot as plt


def plot_scatter(x, y, offset: tuple = (0, 10)):
    for x, y in zip(x, y):
        plt.annotate(y, (x, y), textcoords="offset points", xytext=offset, ha="center")
