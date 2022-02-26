"""
Implements the data loading. If the data is not available offline, it
is freshly fetched from https://www.fantasypros.com/nfl.

This is the base class for loading the data. The cleaning of the data
is implemented in the corresponding child classes. Make sure that the
data is available for the specified parameters.

The recorded fantasy points correspond to standard scoring. For other
scoring schemes, e.g. PPR or Half-PPR, the stats can be used to
compute points scored in that specific scheme.
"""
from abc import ABC

from src.loader.loader import Loader


class FantasyProsLoader(Loader, ABC):
    def __init__(self):
        Loader.__init__(self)




