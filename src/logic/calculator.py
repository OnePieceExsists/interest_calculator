class InterestCalculator:
    def calculate_simple_interest(self, principal, rate, time):
        """
        Calculate simple interest.

        :param principal: The principal amount
        :param rate: The interest rate (as a percentage)
        :param time: The time period (in years)
        :return: The calculated simple interest
        """
        return (principal * rate * time) / 100

    def calculate_compound_interest(self, principal, rate, time, compounding_frequency=1):
        """
        Calculate compound interest.

        :param principal: The principal amount
        :param rate: The interest rate (as a percentage)
        :param time: The time period (in years)
        :param compounding_frequency: The number of times interest is compounded per year
        :return: The calculated compound interest
        """
        amount = principal * (1 + (rate / (100 * compounding_frequency))) ** (compounding_frequency * time)
        return amount - principal