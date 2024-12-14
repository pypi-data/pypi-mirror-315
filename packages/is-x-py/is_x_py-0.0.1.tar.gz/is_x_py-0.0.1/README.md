# is-x-py

Python implementation of is-x, a flexible and fun library for number comparison and manipulation.

## Installation

```bash
pip install is-x-py
```

## Basic Usage

```python
from is_x import Is

# Set a target number
Is(20).set_X()

# Compare other numbers
Is(15).plus(5).is_X()      # True (15 + 5 = 20)
Is(40).divided_by(2).is_X() # True (40 / 2 = 20)

# Check properties of target number
Is.X.is_even()           # True (20 is even)
Is.X.is_prime()          # False (20 is not prime)
```

## Features

### Math Operations

```python
# Basic Math
Is(15).plus(5).is_X()           # True (15 + 5 = 20)
Is(25).minus(5).is_X()          # True (25 - 5 = 20)
Is(10).times(2).is_X()          # True (10 * 2 = 20)
Is(40).divided_by(2).is_X()     # True (40 / 2 = 20)

# Chain operations
Is(10).plus(5).times(2).minus(10).is_X()  # True (10 + 5 = 15, *2 = 30, -10 = 20)

# Advanced Math
Is(4).squared()                # squares the number
Is(400).square_root()          # square root
Is(2).power(4)                # raises to power
Is(8000).root(3)              # nth root
Is(100).modulo(80)            # modulo operation
Is(-20).absolute()            # absolute value
Is(3).factorial()             # factorial
```

### Approximate Comparisons

```python
# Different levels of approximation
Is(19.9).roughly.is_X()           # True (within 0.2 units)
Is(19.5).approximately.is_X()     # True (within 0.5 units)
Is(18).within(3).of.is_X()        # True (within 3 units)
```

### Number Properties

```python
Is.X.is_perfect_square()    # checks if perfect square
Is.X.is_prime()            # checks if prime
Is.X.is_fibonacci()        # checks if Fibonacci number
Is.X.is_even()            # checks if even
Is.X.is_odd()             # checks if odd
Is.X.is_divisible_by(4)    # checks divisibility
Is.X.has_factors()        # returns all factors
Is.X.is_multiple_of(5)     # checks if multiple
```

### Fun Checks

```python
Is.X.is_current_hour()     # compares with current hour
Is.X.is_current_year()     # compares with current year
Is.X.is_answer_to_life()   # checks if 42
Is.X.is_unlucky()         # checks if 13
Is.X.is_dice_roll()       # checks if valid dice number (1-6)
Is.X.is_card_number()     # checks if valid card number (1-13)
Is.X.is_pokemon_number()   # checks if valid Pokémon number (1-898)
```

### Technical Checks

```python
Is.X.is_port()           # checks if valid port number (0-65535)
Is.X.is_http_status()    # checks if valid HTTP status code
Is.X.is_rgb_value()      # checks if valid RGB value (0-255)
Is.X.is_version()        # checks if valid version number
Is.X.is_phone_number()   # checks if valid phone number format
```

## Error Handling

The library includes proper error handling for:

- Division by zero
- Invalid square roots (negative numbers)
- Invalid factorials (negative numbers or non-integers)
- Invalid root calculations
- Invalid phone numbers
- Out of range values

## Related Packages

Check out our multi-language installer:

```bash
npm install -g is-x-installer
```

## Links

- JavaScript implementation: [is-x-js](https://www.npmjs.com/package/is-x-js)
- Installer implementation: [is-x-installer](https://www.npmjs.com/package/is-x-installer)
