import pytest
import jax.numpy as jnp
from ars import ARS, ars
import numpy as np
from jax.scipy.stats import truncnorm


def log_gaussian_pdf(x):
    """log of unnormalized gaussian distributioin satisfying is_logpdf=True."""
    return -0.5 * np.log(2 * np.pi) - 0.5 * (x**2)


def truncated_gaussian_pdf(x, mu=3.0, sigma=1.0, domain=(1.0, 5.0)):
    """Truncated Gaussian PDF."""
    a, b = domain
    gaussian = jnp.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * jnp.sqrt(2 * jnp.pi))
    return jnp.where((x >= a) & (x <= b), gaussian, 0.0)


def test_initial_points_ordering():
    """Test that initial points are correctly ordered in ascending order."""
    domain = (-2.0, 2.0)
    init_points = [-1.0, 0.0, 1.0]
    ars = ARS(
        log_gaussian_pdf,
        domain,
        is_logpdf=True,
        initial_points=init_points,
        n_initial_points=len(init_points),
    )
    assert len(ars.x_values) == len(init_points), "Initial points count mismatch."
    assert np.all(
        np.diff(ars.x_values) > 0
    ), "Initial points are not in ascending order."


def test_sampling_process():
    """Test the sampling process, ensuring the correct number, range, and properties of samples."""
    domain = (-2.0, 2.0)
    ars = ARS(log_gaussian_pdf, domain, is_logpdf=True)
    n_samples = 1500
    samples = ars(n_samples)

    assert (
        len(samples) == n_samples
    ), f"Expected {n_samples} samples, got {len(samples)}."
    assert jnp.all(
        (samples >= domain[0]) & (samples <= domain[1])
    ), "Samples are out of domain."

    # Validate sample mean and standard deviation
    sample_mean = jnp.mean(samples)
    sample_std = jnp.std(samples)
    assert (
        jnp.abs(sample_mean) < 0.2
    ), "Sample mean deviates significantly from the expected mean of 0."
    assert (
        jnp.abs(sample_std - 1.0) < 0.2
    ), "Sample standard deviation deviates significantly from 1."


def test_nonlog_pdf_sampling_process():
    """Test the sampling process of nonlog pdf, ensuring the correct number, range, and properties of samples."""
    domain = (1.0, 5.0)  # Domain for the truncated Gaussian
    ars = ARS(truncated_gaussian_pdf, domain, is_logpdf=False)
    n_samples = 1500
    samples = ars(n_samples)

    assert (
        len(samples) == n_samples
    ), f"Expected {n_samples} samples, got {len(samples)}."
    assert jnp.all(
        (samples >= domain[0]) & (samples <= domain[1])
    ), "Samples are out of domain."

    sample_mean = jnp.mean(samples)
    expected_mean = 3.0
    assert (
        jnp.abs(sample_mean - expected_mean) < 0.5
    ), f"Sample mean {sample_mean} is not close to expected mean {expected_mean}"

    sample_std = jnp.std(samples)
    expected_std = 1.0
    assert (
        jnp.abs(sample_std - expected_std) < 0.5
    ), f"Sample std {sample_std} is not close to expected std {expected_std}"

    pdf_values = truncated_gaussian_pdf(samples)
    assert jnp.all(pdf_values > 0), "Some samples have zero or negative PDF values"


def test_bounds_computation():
    """Test computation of lower and upper bound functions."""
    domain = (-1.0, 1.0)
    ars = ARS(log_gaussian_pdf, domain, is_logpdf=True)
    x = 0.0
    u_k = ars.compute_uk(x)
    l_k = ars.compute_lk(x)
    assert l_k <= u_k, "Lower bound exceeds upper bound."


def test_edge_cases():
    """Test edge cases including empty domains and excessive iterations."""
    # Test for empty domain
    domain = (1.0, 1.0)  # Start and end are the same
    with pytest.raises(AssertionError, match="domain should be in the form"):
        ARS(log_gaussian_pdf, domain, is_logpdf=True)

    # Test for excessive iterations
    domain = (-1.0, 1.0)
    ars = ARS(log_gaussian_pdf, domain, is_logpdf=True)
    with pytest.raises(ValueError, match="Maximum number of iterations reached"):
        ars(1000, max_iter=1)


def test_small_sample_sizes():
    """Test the ARS algorithm with small sample sizes."""
    domain = (-1.0, 1.0)
    ars = ARS(log_gaussian_pdf, domain, is_logpdf=True)

    # Test single sample
    samples = ars(1)
    assert len(samples) == 1, "Expected 1 sample."
    assert (
        domain[0] <= samples[0] <= domain[1]
    ), f"Sample {samples[0]} is out of the domain."

    # Test small batch of samples
    samples = ars(10)
    assert len(samples) == 10, "Expected 10 samples."
    assert jnp.all(
        (samples >= domain[0]) & (samples <= domain[1])
    ), "Samples are out of the domain."
