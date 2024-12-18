
import pytest
import numpy as np
from scipy import stats
from ..datalib.statistics import mean, median, std_dev, correlation, t_test, chi_square

def test_mean():
    """Test the mean function."""
    data = [1, 2, 3, 4, 5]
    result = mean(data)
    assert result == 3.0

def test_median():
    """Test the median function."""
    data_odd = [1, 3, 5]
    data_even = [1, 2, 3, 4]
    assert median(data_odd) == 3.0
    assert median(data_even) == 2.5

def test_std_dev():
    """Test the standard deviation function."""
    data = [1, 2, 3, 4, 5]
    result = std_dev(data)
    expected = np.std(data)
    assert result == pytest.approx(expected, rel=1e-3)

def test_correlation():
    """Test the correlation function."""
    data1 = [1, 2, 3, 4, 5]
    data2 = [2, 4, 6, 8, 10]
    result = correlation(data1, data2)
    assert result == pytest.approx(1.0, rel=1e-3)

def test_t_test():
    """Test the t-test function."""
    data1 = [1, 2, 3, 4, 5]
    data2 = [2, 3, 4, 5, 6]
    t_stat, p_value = t_test(data1, data2)
    expected_t_stat, expected_p_value = stats.ttest_ind(data1, data2)
    assert t_stat == pytest.approx(expected_t_stat, rel=1e-3)
    assert p_value == pytest.approx(expected_p_value, rel=1e-3)

def test_chi_square():
    """Test the chi-square function."""
    observed = [10, 20, 30]
    expected = [15, 15, 30]
    chi2_stat, p_value = chi_square(observed, expected)
    expected_chi2, expected_p = stats.chisquare(observed, expected)
    assert chi2_stat == pytest.approx(expected_chi2, rel=1e-3)
    assert p_value == pytest.approx(expected_p, rel=1e-3)
