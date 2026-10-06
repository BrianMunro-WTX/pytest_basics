"""Full pytest suite for car.py.

Demonstrates the core pytest concepts:
  - plain assert statements
  - fixtures (see conftest.py)
  - @pytest.mark.parametrize
  - pytest.raises for exceptions
  - pytest.approx for float comparisons
  - capsys for capturing printed output
  - caplog for capturing log output
  - grouping tests with section comments (no classes needed)
  - markers: skip / xfail
  - descriptive logging (run with --log-cli-level=INFO, already set in pytest.ini)
"""
import logging

import pytest

from car import Car

# A module-level logger. pytest.ini sets log_cli = true so these messages
# appear live in the test output next to each test.
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# Constructor & basic getters — plain asserts
# ----------------------------------------------------------------------
def test_default_values(default_car):
    logger.info("Checking the default Car() constructor values")
    logger.debug(
        "Car under test: %s %s (%s), mileage=%s",
        default_car.make, default_car.model, default_car.year,
        default_car.get_mileage(),
    )
    assert default_car.make == "Ford"
    assert default_car.model == "Mustang"
    assert default_car.year == 2020
    assert default_car.get_mileage() == 25000
    logger.info("All four default attributes matched expected values")

def test_custom_values():
    logger.info("Constructing a custom car: 2018 Honda Civic with 30000 miles")
    car = Car("Honda", "Civic", 2018, 30000)
    assert car.make == "Honda"
    assert car.model == "Civic"
    assert car.year == 2018
    assert car.get_mileage() == 30000
    logger.info("Custom constructor values verified")


# ----------------------------------------------------------------------
# display_info / drive output — capturing stdout with capsys
# ----------------------------------------------------------------------
def test_display_info(capsys):
    car = Car("Honda", "Civic", 2018, 30000)
    logger.info("Calling display_info() and capturing stdout")
    car.display_info()
    captured = capsys.readouterr()
    logger.debug("Captured stdout: %r", captured.out)
    assert captured.out.strip() == "2018 Honda Civic with 30000 miles"

def test_drive_prints_confirmation(default_car, capsys):
    logger.info("Driving 100 miles, expecting a confirmation message")
    default_car.drive(100)
    out = capsys.readouterr().out
    logger.debug("Captured stdout: %r", out)
    assert "Driven 100 miles" in out

def test_drive_beyond_max_prints_warning(tesla, capsys):
    logger.info("Attempting to drive a Tesla 999999 miles (max is 300000)")
    tesla.drive(999999)
    out = capsys.readouterr().out
    logger.debug("Captured stdout: %r", out)
    assert "Cannot drive" in out
    assert "300000" in out
    logger.info("Warning message contained the make and the 300000 limit")


# ----------------------------------------------------------------------
# max_mileage — parametrized tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "make, expected",
    [
        ("Ford", 200000),
        ("Toyota", 200000),
        ("Honda", 200000),
        ("Tesla", 300000),
        ("BMW", 150000),
        ("UnknownMake", 150000),
    ],
)
def test_max_mileage_by_make(make, expected):
    logger.info("Verifying max mileage for make=%r is %s", make, expected)
    actual = Car(make).max_mileage()
    logger.debug("max_mileage() returned %s", actual)
    assert actual == expected

def test_max_mileage_with_fixture(standard_car):
    """Runs once per parametrized fixture value (Ford/Toyota/Honda)."""
    logger.info("Fixture supplied a %s — expecting max mileage 200000",
                standard_car.make)
    assert standard_car.max_mileage() == 200000


# ----------------------------------------------------------------------
# drive — state changes, edge cases, exceptions
# ----------------------------------------------------------------------
def test_drive_updates_mileage(default_car):
    logger.info("Driving 500 miles from %s miles", default_car.get_mileage())
    default_car.drive(500)
    logger.info("Mileage is now %s, expecting 25500", default_car.get_mileage())
    assert default_car.get_mileage() == 25500

def test_drive_zero_miles(default_car):
    logger.info("Edge case: driving 0 miles must not change the odometer")
    default_car.drive(0)
    assert default_car.get_mileage() == 25000

def test_drive_exactly_to_max():
    car = Car("Tesla", "Model S", 2022, 299999)
    logger.info("Boundary case: driving 1 mile from 299999 (max 300000)")
    car.drive(1)
    assert car.get_mileage() == 300000
    logger.info("Reached exactly the maximum allowed mileage")

def test_drive_past_max_does_nothing(default_car):
    logger.info("Attempting to exceed max mileage — odometer must not move")
    default_car.drive(200000)
    assert default_car.get_mileage() == 25000  # unchanged

def test_drive_negative_raises(default_car):
    logger.info("Negative miles must raise ValueError")
    with pytest.raises(ValueError, match="negative"):
        default_car.drive(-1)
    logger.info("ValueError raised as expected")


# ----------------------------------------------------------------------
# get_age / is_vintage — arithmetic and boolean assertions
# ----------------------------------------------------------------------
def test_get_age(default_car):
    logger.info("A %s car should be 6 years old in 2026", default_car.year)
    assert default_car.get_age(2026) == 6

def test_get_age_zero_for_new_car():
    logger.info("Edge case: a car built in the current year has age 0")
    assert Car(year=2026).get_age(2026) == 0

def test_get_age_future_year_raises(default_car):
    logger.info("Asking for age in 2010 (before the car's year) must raise")
    with pytest.raises(ValueError):
        default_car.get_age(2010)

@pytest.mark.parametrize(
    "year, current_year, expected",
    [
        (2000, 2026, True),   # 26 years old -> vintage
        (2001, 2026, True),   # exactly 25 -> vintage (boundary)
        (2002, 2026, False),  # 24 years old -> not vintage
        (2026, 2026, False),  # brand new -> not vintage
    ],
)
def test_is_vintage(year, current_year, expected):
    logger.info(
        "is_vintage check: year=%s, current_year=%s, expecting %s",
        year, current_year, expected,
    )
    car = Car(year=year)
    assert car.is_vintage(current_year) is expected


# ----------------------------------------------------------------------
# set_mileage — exception testing with pytest.raises
# ----------------------------------------------------------------------
def test_set_higher_mileage(default_car):
    logger.info("Raising odometer from %s to 50000 — allowed",
                default_car.get_mileage())
    default_car.set_mileage(50000)
    assert default_car.get_mileage() == 50000

def test_set_same_mileage_allowed(default_car):
    logger.info("Setting the same mileage (%s) is allowed",
                default_car.get_mileage())
    default_car.set_mileage(25000)
    assert default_car.get_mileage() == 25000

def test_negative_mileage_raises(default_car):
    logger.info("Negative mileage must raise ValueError")
    with pytest.raises(ValueError, match="negative"):
        default_car.set_mileage(-1)

def test_rollback_raises(default_car):
    logger.info("Rolling the odometer back to 10000 must raise ValueError")
    with pytest.raises(ValueError, match="rollback"):
        default_car.set_mileage(10000)


# ----------------------------------------------------------------------
# needs_service — parametrized boundary tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "mileage, expected",
    [
        (0, False),       # zero is not a service interval
        (10000, True),    # exactly on interval
        (15000, False),   # between intervals
        (20000, True),
        (9999, False),
        (10001, False),
    ],
)
def test_needs_service(mileage, expected):
    logger.info("needs_service at %s miles -> expecting %s", mileage, expected)
    car = Car(mileage=mileage)
    assert car.needs_service() is expected


# ----------------------------------------------------------------------
# fuel_efficiency — float comparison with pytest.approx
# ----------------------------------------------------------------------
def test_exact_division():
    logger.info("30000 miles / 1000 gallons should be exactly 30.0 mpg")
    assert Car(mileage=30000).fuel_efficiency(1000) == 30.0

def test_float_result_needs_approx():
    # 25000 / 3 is a repeating decimal — never compare floats with ==
    logger.info("25000 / 3 is a repeating decimal — comparing with pytest.approx")
    result = Car().fuel_efficiency(3)
    logger.debug("fuel_efficiency returned %r", result)
    assert result == pytest.approx(8333.3333, rel=1e-4)

@pytest.mark.parametrize("gallons", [0, -5])
def test_nonpositive_gallons_raises(gallons):
    logger.info("gallons=%s must raise ValueError", gallons)
    with pytest.raises(ValueError, match="positive"):
        Car().fuel_efficiency(gallons)


# ----------------------------------------------------------------------
# remaining_miles / can_drive — arithmetic & boolean edge cases
# ----------------------------------------------------------------------
def test_remaining_miles(default_car):
    logger.info("Ford with %s miles should have 175000 miles remaining",
                default_car.get_mileage())
    assert default_car.remaining_miles() == 200000 - 25000

def test_remaining_miles_tesla(tesla):
    logger.info("Tesla with %s miles should have 295000 miles remaining",
                tesla.get_mileage())
    assert tesla.remaining_miles() == 300000 - 5000

@pytest.mark.parametrize(
    "miles, expected",
    [
        (0, True),          # driving nowhere is always fine
        (174999, True),     # just under the limit
        (175000, True),     # exactly at the limit
        (175001, False),    # one mile over
        (-1, False),        # negative trip rejected
    ],
)
def test_can_drive(default_car, miles, expected):
    # default car: 25000 miles, max 200000 -> 175000 remaining
    logger.info("can_drive(%s) with 175000 remaining -> expecting %s",
                miles, expected)
    assert default_car.can_drive(miles) is expected


# ----------------------------------------------------------------------
# caplog — asserting on log records produced during a test
# ----------------------------------------------------------------------
def test_drive_logs_nothing_but_we_can_capture_our_own(default_car, caplog):
    """caplog captures log records so a test can assert on them."""
    with caplog.at_level(logging.INFO):
        logger.info("About to drive the default car")
        default_car.drive(50)
        logger.info("Finished driving")

    logger.debug("caplog captured %d records", len(caplog.records))
    assert "About to drive the default car" in caplog.text
    assert "Finished driving" in caplog.text

