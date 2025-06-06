def validate_input(value):
    try:
        float_value = float(value)
        if float_value < 0:
            raise ValueError("Input must be a non-negative number.")
        return float_value
    except ValueError:
        raise ValueError("Invalid input. Please enter a valid number.")

def format_result(result):
    return f"{result:.2f}"