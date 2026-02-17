import csv
import argparse

def get_user_input(integers_only):
    """Gets all the necessary inputs from the user."""
    try:
        number_type = int if integers_only else float
        
        start_number = number_type(input("Enter the starting number: "))
        
        print("Available operations: add, subtract, multiply, divide, custom")
        operation = input("Enter the operation: ").strip().lower()
        if operation not in ['add', 'subtract', 'multiply', 'divide', 'custom']:
            print("Invalid operation. Please choose from the available options.")
            return None

        operator_value = None # Initialize to None
        if operation == 'custom':
            print("Warning: Using 'eval()' for custom functions can be a security risk if input is not trusted.")
            operator_value = input("Enter a custom function (e.g., x * 2 + 1, where 'x' = previous number): ").strip()
            # Basic validation for custom function to ensure 'x' is present
            if 'x' not in operator_value:
                print("Custom function must include 'x' as the placeholder for the previous number.")
                return None
        else:
            operator_value = number_type(input(f"Enter the value to {operation} by: "))
        
        length = int(input("Enter the length of the sequence to generate: "))
        if length <= 0:
            print("Sequence length must be a positive integer.")
            return None

        filename = input("Enter the output filename (e.g., sequence.csv): ").strip()
        if not filename.endswith('.csv'):
            filename += '.csv'

        # Divergence detection bounds
        upper_bound = None
        lower_bound = None
        add_bounds = input("Add bounds for divergence detection? (yes/no): ").strip().lower()
        if add_bounds == 'yes':
            try:
                upper_bound_str = input("Enter upper bound (or press Enter to skip): ").strip()
                if upper_bound_str:
                    upper_bound = number_type(upper_bound_str)
                
                lower_bound_str = input("Enter lower bound (or press Enter to skip): ").strip()
                if lower_bound_str:
                    lower_bound = number_type(lower_bound_str)
            except ValueError:
                print("Invalid bound value. Bounds must be numbers.")
                # Decide if we should stop or just ignore bounds
                print("Invalid input. Ignoring divergence bounds.")
                upper_bound = None
                lower_bound = None


        return start_number, operation, operator_value, length, filename, upper_bound, lower_bound

    except ValueError:
        print("Invalid input. Please enter valid numbers.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def generate_sequence(start, op, op_val, length, upper_bound=None, lower_bound=None, integers_only=False):
    """Generates the numerical sequence with convergence, cycle, and divergence detection."""
    sequence = [start]
    seen_numbers = [start] if not integers_only else None
    seen_set = {start} if integers_only else None
    current_number = start

    for _ in range(length - 1):
        previous_number = current_number
        if op == 'add':
            current_number += op_val
        elif op == 'subtract':
            current_number -= op_val
        elif op == 'multiply':
            current_number *= op_val
        elif op == 'divide':
            if op_val == 0:
                print("Error: Division by zero is not allowed.")
                return None
            if integers_only:
                current_number //= op_val
            else:
                current_number /= op_val
        elif op == 'custom':
            try:
                # 'x' = variable representing previous number in sequence
                x = current_number
                current_number = eval(op_val, {"x": x})
            except Exception as e:
                print(f"Error evaluating custom function '{op_val}': {e}")
                return None
        
        if integers_only:
            current_number = int(current_number)

        # Divergence Detection
        if upper_bound is not None and current_number > upper_bound:
            print(f"\nDivergence detected: {current_number} exceeded upper bound of {upper_bound}.")
            break # Don't append violating number
        if lower_bound is not None and current_number < lower_bound:
            print(f"\nDivergence detected: {current_number} exceeded lower bound of {lower_bound}.")
            break # Don't append violating number

        # Convergence, Cycle Detection
        if integers_only:
            converged = current_number == previous_number
        else:
            converged = abs(current_number - previous_number) <= 1e-9
        if converged:
            print(f"\nConvergence detected: Sequence stabilized at {current_number} (previous: {previous_number}).")
            sequence.append(current_number)
            break
        
        if integers_only:
            if current_number in seen_set:
                print(f"\nCycle detected: Number {current_number} repeated. Sequence is entering a loop.")
                sequence.append(current_number)
                break
        else:
            if any(abs(current_number - seen) <= 1e-9 for seen in seen_numbers):
                print(f"\nCycle detected: Number {current_number} repeated (within tolerance). Sequence is entering a loop.")
                sequence.append(current_number)
                break

        sequence.append(current_number)
        if integers_only:
            seen_set.add(current_number)
        else:
            seen_numbers.append(current_number)
    
    return sequence

def save_to_csv(sequence, filename):
    """Saves the sequence to a CSV file."""
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Value'])  # Header
            for item in sequence:
                writer.writerow([item])
        print(f"Sequence successfully saved to {filename}")
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")

def main():
    """Main function to run the sequence generator program."""
    parser = argparse.ArgumentParser(description="Generate mathematical sequences.")
    parser.add_argument('--intonly', action='store_true', help='Enable integer-only mode (disables floating point numbers and scientific notation).')
    args = parser.parse_args()

    print("--- Mathematical Sequence Generator ---")
    
    inputs = get_user_input(args.intonly)
    
    if inputs:
        start_number, operation, operator_value, length, filename, upper_bound, lower_bound = inputs
        integers_only = args.intonly # Use flag from argparse
        
        sequence = generate_sequence(start_number, operation, operator_value, length, upper_bound, lower_bound, integers_only)
        
        if sequence:
            print("\nGenerated Sequence:")
            print(sequence)
            save_to_csv(sequence, filename)

if __name__ == "__main__":
    main()
