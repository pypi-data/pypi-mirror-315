import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy
import folium
from matplotlib.colors import ListedColormap
from pandas import qcut  # For quantile-based binning in the interactive map function
from pandas import cut
from .mapplot import plot_scatter, plot_interactive_map