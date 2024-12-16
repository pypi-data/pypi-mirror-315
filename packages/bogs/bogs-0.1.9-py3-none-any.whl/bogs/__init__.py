"""Top-level package for TCRA."""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy
import folium
from matplotlib.colors import ListedColormap
from pandas import qcut  # For quantile-based binning in the interactive map function
from pandas import cut
from scipy.stats import lognorm 
from bogs import hazard
from bogs import vulnerability
from bogs import damageprob
from bogs import loss
from bogs import recovery
from bogs import plot
from bogs import functionality
from bogs import social

__author__ = """Ram Krishna Mazumder"""
__email__ = 'swaranjitroy08@gmail.com'
__version__ = '0.1'

