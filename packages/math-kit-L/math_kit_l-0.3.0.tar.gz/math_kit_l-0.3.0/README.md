# Math Library - Python

This repository contains a comprehensive Python library for performing various mathematical operations, ranging from basic arithmetic to advanced algebra, trigonometry, and geometry. Designed for ease of use, the library is ideal for students, educators, and developers seeking an all-in-one math toolkit.

---

## Features

### Arithmetic Operations

- **Addition** (`add(a, b)`): Returns the sum of two numbers.
- **Subtraction** (`subtract(a, b)`): Returns the difference of two numbers.
- **Multiplication** (`multiply(a, b)`): Returns the product of two numbers.
- **Division** (`divide(a, b)`): Returns the quotient of two numbers (raises an error for division by zero).
- **Modulus** (`modulus(a, b)`): Returns the remainder of the division of two numbers.

### Algebraic Functions

- **Power** (`power(a, b)`): Calculates .
- **Square Root** (`sq_root(x)`): Computes the square root of a number.
- **Cube Root** (`cu_root(x)`): Computes the cube root of a number.
- **Absolute Value** (`absolute_v(x)`): Returns the absolute value of a number.
- **Factorial** (`factorial(n)`): Returns .
- **Fibonacci Sequence** (`fibonacci(n)`): Computes the nth Fibonacci number.
- **Prime Checking** (`is_prime(n)`): Checks whether a number is prime.
- **Nth Prime** (`nth_prime(n)`): Finds the nth prime number.
- **GCD** (`gcd(a, b)`): Calculates the greatest common divisor of two numbers.
- **LCM** (`lcm(a, b)`): Calculates the least common multiple of two numbers.

### Trigonometry Functions

- **Sine** (`sine(angle_in_degrees)`): Calculates the sine of an angle (in degrees).
- **Cosine** (`cosine(angle_in_degrees)`): Calculates the cosine of an angle (in degrees).
- **Tangent** (`tangent(angle_in_degrees)`): Calculates the tangent of an angle (in degrees).
- **Arcsine** (`arcsine(value)`): Calculates the arcsine in degrees.
- **Arccosine** (`arccosine(value)`): Calculates the arccosine in degrees.
- **Arctangent** (`arctangent(value)`): Calculates the arctangent in degrees.
- **Hyperbolic Sine, Cosine, Tangent**: Computes hyperbolic trigonometric functions.

### Statistical Functions

- **Mean** (`mean(numbers)`): Returns the average of a list of numbers.
- **Median** (`median(numbers)`): Returns the median value of a list of numbers.
- **Mode** (`mode(numbers)`): Returns the most frequent value in a list.
- **Range** (`range_of_list(numbers)`): Calculates the range (max - min) of a list.

### Geometry Functions

- **Area of Circle** (`area_of_circle(radius)`): Computes the area of a circle.
- **Circumference of Circle** (`circumference_of_circle(radius)`): Computes the circumference of a circle.
- **Area of Triangle** (`area_of_triangle(base, height)`): Computes the area of a triangle.
- **Perimeter of Triangle** (`perimeter_of_triangle(a, b, c)`): Computes the perimeter of a triangle.
- **Area of Rectangle** (`area_of_rectangle(length, width)`): Computes the area of a rectangle.
- **Perimeter of Rectangle** (`perimeter_of_rectangle(length, width)`): Computes the perimeter of a rectangle.
- **Volume and Surface Area of 3D Shapes**: Functions to compute the volume and surface area of spheres, cylinders, cubes, and rectangular prisms.

### Utility Functions

- **Conversion**: Degrees to radians and vice versa.
- **Factorization** (`factors(n)`): Returns a list of all factors of a number.
- **Perfect Numbers**: Check for perfect squares and perfect cubes.
- **Summation**: Calculate the sum of all, even, or odd numbers up to .

---

## Installation

```bash
pip install math-kit-L
```

```python
# Import the library
from math_library import *

# Example usage
print(add(10, 5))  # Output: 15
print(area_of_circle(7))  # Output: 153.93804002589985
```

---

## Usage

### Example Code

```python
# Arithmetic
print(add(5, 3))  # Output: 8
print(divide(10, 2))  # Output: 5.0

# Geometry
radius = 10
print(f"Area of Circle: {area_of_circle(radius)}")
print(f"Circumference: {circumference_of_circle(radius)}")

# Algebra
n = 5
print(f"Factorial of {n}: {factorial(n)}")
print(f"Fibonacci({n}): {fibonacci(n)}")

# Trigonometry
angle = 30
print(f"Sine of {angle}: {sine(angle)}")
print(f"Cosine of {angle}: {cosine(angle)}")
```

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Author

Created by **lmc**.

---

## Acknowledgments

Special thanks to Python's `math` and `cmath` libraries for providing foundational functions and inspiration for this library.

