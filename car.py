class Car:
    _mileage = 0
    def __init__(self, make = "Ford", model = "Mustang", year = 2020, mileage = 25000):
        self.make = make
        self.model = model
        self.year = year
        self._mileage = mileage

    def display_info(self):
        print(f"{self.year} {self.make} {self.model} with {self._mileage} miles")

    def get_mileage(self):
        return self._mileage

    def max_mileage(self):
        if self.make in ["Ford", "Toyota", "Honda"]:
            return 200000
        elif self.make == "Tesla":
            return 300000
        else:
            return 150000
        
    def drive(self, miles):
        if miles < 0:
            raise ValueError("Cannot drive a negative number of miles.")
        if self._mileage + miles > self.max_mileage():
            print(f"Cannot drive {miles} miles. It would exceed the maximum mileage of {self.max_mileage()} miles.")
        else:
            self._mileage += miles
            print(f"Driven {miles} miles. Total mileage is now {self._mileage} miles.")

    def get_age(self, current_year=2026):
        """Return the car's age. Good for basic assert tests."""
        if current_year < self.year:
            raise ValueError("Current year cannot be before the car's year.")
        return current_year - self.year

    def is_vintage(self, current_year=2026):
        """A car is vintage if it is 25+ years old. Good for True/False tests."""
        return self.get_age(current_year) >= 25

    def set_mileage(self, mileage):
        """Set the odometer. Raises on invalid input — good for pytest.raises."""
        if mileage < 0:
            raise ValueError("Mileage cannot be negative.")
        if mileage < self._mileage:
            raise ValueError("Odometer rollback detected!")
        self._mileage = mileage

    def needs_service(self):
        """Service is due every 10,000 miles. Good for parametrized tests."""
        return self._mileage % 10000 == 0 and self._mileage > 0

    def fuel_efficiency(self, gallons_used):
        """Miles per gallon. Good for float comparison tests (pytest.approx)."""
        if gallons_used <= 0:
            raise ValueError("Gallons used must be positive.")
        return self._mileage / gallons_used

    def remaining_miles(self):
        """Miles left before hitting max mileage. Good for arithmetic tests."""
        return self.max_mileage() - self._mileage

    def can_drive(self, miles):
        """Check if a trip is possible without driving. Good for boolean edge cases."""
        if miles < 0:
            return False
        return self._mileage + miles <= self.max_mileage()

def main():
    #my_car = Car("Toyota", "Corolla", 2020)
    cars = [Car(), Car("Toyota", "Corolla", 2020, 15000), Car("Honda", "Civic", 2018, 30000), Car("Tesla", "Model 3", 2021, 5000)]

    for my_car in cars:
        my_car.display_info()
        my_car.drive(100000)
        my_car.display_info()
    #x = input("Press Enter to exit...")

if __name__ == "__main__":
    main()