import pytest
import jax.numpy as jnp
import numpy as np
from jax.scipy.stats import truncnorm
import os

# allow access to project.
# parent_dir = os.path.dirname(os.getcwd())
# sys.path.append(parent_dir)
print(os.getcwd())

from ars.utils import *


def func(x):
    return -(x**2), -2 * x  # Return function value and gradient


def test_finite_domain():
    # Test case 1: domain is finite, both endpoints
    domain = [-2.0, 2.0]
    points, values, gradients = find_initial_points(domain, func)
    # Check that we have two points
    assert len(points) == 2, f"Expected 2 points, but got {len(points)}"
    # Check that points are within domain
    assert domain[0] <= points[0] <= domain[1], f"Point {points[0]} is out of domain"
    assert domain[0] <= points[1] <= domain[1], f"Point {points[1]} is out of domain"
    # Check that gradients are non-zero
    assert gradients[0] != 0, "Gradient at x_0 should be non-zero"
    assert gradients[1] != 0, "Gradient at x_1 should be non-zero"


def test_neg_inf_domain():
    # Test case 2: domain with negative infinity, find x_0 such that gradient > 0
    domain = [-np.inf, 2.0]
    points, values, gradients = find_initial_points(domain, func)
    assert (
        points[0] < domain[1]
    ), f"Point x_0 {points[0]} should be less than right domain"
    # Treat -0.0 as 0.0 and check if gradient is positive
    gradient_0 = gradients[0]
    assert gradient_0 > 0 or np.isclose(
        gradient_0, 0
    ), f"Gradient at x_0 {gradient_0} should be positive"


def test_pos_inf_domain():
    domain = [-2.0, np.inf]
    points, values, gradients = find_initial_points(domain, func)
    assert (
        points[1] > domain[0]
    ), f"Point x_1 {points[1]} should be greater than left domain"
    # Treat -0.0 as 0.0 and check if gradient is negative
    gradient_1 = gradients[1]
    assert gradient_1 < 0 or np.isclose(
        gradient_1, 0
    ), f"Gradient at x_1 {gradient_1} should be negative"


def test_pos_and_neg_inf_domain():
    domain = [-np.inf, np.inf]
    points, values, gradients = find_initial_points(domain, func)
    assert len(points) == 2
    assert (
        points[0] < points[1]
    ), f"Point x_0 {points[0]} should be less than point x_1 {points[1]}."
    assert gradients[0] > 0, f"Gradient at x_0 {gradients[0]} should be positive"
    assert gradients[1] < 0, f"Gradient at x_1 {gradients[1]} should be negative"
