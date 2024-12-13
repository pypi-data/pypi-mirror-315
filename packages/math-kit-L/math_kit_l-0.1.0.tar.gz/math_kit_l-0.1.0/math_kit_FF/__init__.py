import math
import cmath

def add(a,b):
    return a + b

def substract(a,b):
    return a - b

def multiply(a,b):
    return a * b 

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b

def absolute_v(x):
    return abs(x)

def power(a,b):
    return a ** b

def sq_root(x):
    return x ** 0.5

def cu_root(x):
    return x ** (1/3)

def floor_d(x):
    return math.floor(x)

def ceil_d(x):
    return math.ceil(x)

def round_n_int(x):
    return round(x)

def factorial(n):
    result = 1
    for i in range(1, n+1):
        result *= i
    return result

def fibonacci(n):
    if n <= 0:
        return "Input must be a positive integer"
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    a, b = 0, 1
    for _ in range(2, n):
        a, b = b, a + b
    return b

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return absolute_v(a * b) // gcd(a, b)

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(sq_root(n)) + 1):
        if n % i == 0:
            return False
    return True

def nth_prime(n):
    count = 0
    num = 1
    while count < n:
        num += 1
        if is_prime(num):
            count += 1
    return num

def solve_quadratic(a, b, c):
    # Calculate the discriminant
    discriminant = b**2 - 4*a*c
    
    # Calculate the two solutions using the quadratic formula
    root1 = (-b + cmath.sqrt(discriminant)) / (2*a)
    root2 = (-b - cmath.sqrt(discriminant)) / (2*a)
    
    return root1, root2

def mean(numbers):
    total = sum(numbers)  # Sum of all numbers
    count = len(numbers)  # Number of numbers
    return total / count

def median(numbers):
    numbers.sort()  # Sort the numbers
    n = len(numbers)
    
    if n % 2 == 1:  # If odd number of elements
        return numbers[n // 2]  # Return the middle number
    else:  # If even number of elements
        mid1 = numbers[n // 2 - 1]
        mid2 = numbers[n // 2]
        return (mid1 + mid2) / 2  # Return the average of the two middle numbers

def sine(x):
    angle_degrees = 30
    angle_radians = math.radians(angle_degrees)  # Convert degrees to radians
    result = math.sin(angle_radians)

    return result

def area_of_circle(radius):
    return math.pi * radius ** 2

def circumference_of_circle(radius):
    return 2 * math.pi * radius

def area_of_triangle(base, height):
    return 0.5 * base * height

def perimeter_of_triangle(a, b, c):
    return a + b + c

def area_of_rectangle(length, width):
    return length * width

def perimeter_of_rectangle(length, width):
    return 2 * (length + width)

def volume_of_sphere(radius):
    return (4/3) * math.pi * radius ** 3

def surface_area_of_sphere(radius):
    return 4 * math.pi * radius ** 2

def volume_of_cylinder(radius, height):
    return math.pi * radius ** 2 * height

def surface_area_of_cylinder(radius, height):
    return 2 * math.pi * radius * (radius + height)

def cosine(angle_in_degrees):
    angle_in_radians = math.radians(angle_in_degrees)  # Convert to radians
    return math.cos(angle_in_radians)

def tangent(angle_in_degrees):
    angle_in_radians = math.radians(angle_in_degrees)  # Convert to radians
    return math.tan(angle_in_radians)

def arcsine(value):
    return math.degrees(math.asin(value))  # Convert result from radians to degrees

def arccosine(value):
    return math.degrees(math.acos(value))  # Convert result from radians to degrees

def arctangent(value):
    return math.degrees(math.atan(value))  # Convert result from radians to degrees

def hyperbolic_sine(value):
    return math.sinh(value)

def hyperbolic_cosine(value):
    return math.cosh(value)

def hyperbolic_tangent(value):
    return math.tanh(value)

def degrees_to_radians(degrees):
    return math.radians(degrees)

def radians_to_degrees(radians):
    return math.degrees(radians)

def volume_of_cube(side_length):
    return side_length ** 3

def surface_area_of_cube(side_length):
    return 6 * side_length ** 2

def volume_of_rectangular_prism(length, width, height):
    return length * width * height

def surface_area_of_rectangular_prism(length, width, height):
    return 2 * (length * width + length * height + width * height)

def factors(n):
    return [i for i in range(1, n + 1) if n % i == 0]

def is_perfect_square(n):
    return int(math.sqrt(n)) ** 2 == n

def is_perfect_cube(n):
    return round(n ** (1/3)) ** 3 == n

def is_divisible(a, b):
    return a % b == 0

def range_of_list(numbers):
    return max(numbers) - min(numbers)

def mode(numbers):
    from collections import Counter
    data = Counter(numbers)
    return data.most_common(1)[0][0]

def average(numbers):
    return sum(numbers) / len(numbers)

def seconds_in_minutes(minutes):
    return minutes * 60

def minutes_in_hours(hours):
    return hours * 60

def hours_in_days(days):
    return days * 24

def is_positive(n):
    return n > 0

def is_negative(n):
    return n < 0

def sum_of_numbers(n):
    return sum(range(1, n + 1))

def sum_of_even_numbers(n):
    return sum(i for i in range(2, n + 1, 2))

def sum_of_odd_numbers(n):
    return sum(i for i in range(1, n + 1, 2))

def is_even(n):
    return n % 2 == 0

def is_odd(n):
    return n % 2 != 0

def cube(n):
    return n ** 3

def square(n):
    return n ** 2

def modulus(a, b):
    return a % b


