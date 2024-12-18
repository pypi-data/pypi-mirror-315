from datetime import datetime

import polars as pl
import pytest
from matplotlib.testing.decorators import image_comparison
from numpy.testing import assert_almost_equal

import odisi
from odisi import read_tsv


@pytest.fixture
def luna_data():
    return read_tsv("tests/data/verification_data_ch1_gages.tsv")


class TestSynchronization:
    @image_comparison(
        baseline_images=["time_synchronization"],
        remove_text=True,
        extensions=["png"],
        style="mpl20",
    )
    def test_time_synchronization(self, luna_data):
        signal = pl.read_csv("tests/data/verification_load.csv", try_parse_dates=True)
        signal = signal.rename({"load [kN]": "signal"})

        odisi._called_from_test = True

        delta = luna_data.synchronize_data(
            data=signal, time="time [s]", segment=0, invert_signal=True
        )
