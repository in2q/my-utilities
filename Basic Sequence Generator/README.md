# Basic Sequence Generator

A CLI tool that generates and analyzes mathematical sequences, with support for various operations and CSV export.

## Prerequisites

- Python 3.6 or later
- No external dependencies required (utilizes Python's standard library)

## Usage

```bash
python sequence_generator.py
python sequence_generator.py --intonly
```

The `--intonly` flag restricts all values to integers and uses floor division instead of float division.

### Interactive Mode

When executed, the program guides you through sequence configuration:

1. Sequence initialization (starting value)
2. Operation selection (add/subtract/multiply/divide/custom)
3. Parameter specification (constant value or custom expression)
4. Sequence length configuration
5. Optional boundary conditions (upper/lower bounds)
6. Output preferences (integer/float mode)

## Operations

| Operation | Description |
|-----------|-------------|
| `add` | Add a constant each step |
| `subtract` | Subtract a constant each step |
| `multiply` | Multiply by a constant each step |
| `divide` | Divide by a constant each step |
| `custom` | Apply a custom math expression using `x` as the previous value |

### Custom Expressions

Custom mode accepts math expressions where `x` represents the previous number in the sequence. Expressions are validated via AST parsing to ensure only safe operations are allowed.

Available functions and constants:

`abs`, `round`, `min`, `max`, `pow`, `int`, `float`, `sqrt`, `log`, `log2`, `log10`, `sin`, `cos`, `tan`, `floor`, `ceil`, `pi`, `e`

Examples:
```
x * 2 + 1
sqrt(x) + pi
x ** 2 - 3 * x + 1
abs(sin(x)) * 10
```

## Sequence Detection

The generator automatically detects three conditions and stops early:

- **Convergence** -- consecutive values stabilize (within `1e-9` tolerance for floats, exact match for integers)
- **Cycle** -- a previously seen value reappears (tolerance-based for floats)
- **Divergence** -- value exceeds user-defined upper or lower bounds

## Technicals

### Numerical Precision

- Floating-point operations maintain standard Python precision
- Integer mode enforces floor division and type consistency
- Convergence detection uses a tolerance of 1e-9 for floating-point comparisons

### Error Handling

- Input validation for all user-provided values
- Graceful handling of mathematical edge cases (e.g., division by zero)
- Clear error messages for invalid expressions or operations

## Output

Results are printed to the console and saved to a CSV file of your choosing.

## Academic Applications

You may find this tool useful if you do:

- Numerical analysis exercises
- Algorithm development and testing
- Educational demonstrations of sequence behavior
- Research involving iterative numerical methods (maybe not Collatz...)

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.