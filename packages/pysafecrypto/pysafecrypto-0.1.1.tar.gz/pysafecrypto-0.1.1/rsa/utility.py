import random
from typing import List, Dict

class PrimeHandler:
    def __init__(self, prime_range_start: int=100, prime_range_end: int=150) -> None:
        """Initialize configuration for primehandler"""
        self.prime_number_range_start = prime_range_start
        self.prime_number_range_end = prime_range_end
        self.debug = False

    def generate_prime_number(self) -> int:
        """Generates a random prime number within the initalized prime ranges
        
        -- Method will use PrimeHandler.prime_range_start and self.prime_range_end as upper and lower limit for random prime number

        """
        while True:
            random_prime_number: int = random.randrange(self.prime_number_range_start, self.prime_number_range_end) # Choose random integer within given range
            if self.is_prime(random_prime_number): # Check if integer is prime
                return random_prime_number


    def solve_gcd(self, a: int, b: int, show_math_expr:bool=False) -> int | Dict:
        """Implements Euclidean algorithm to find gcd between a and b

        -- Will return gcd

        -- Variables a and b are used to compute a mathematical expresson of: a = bq * r
        
        a: represents the current dividend and must be an integer coprime to b
        b: represents the current divisor and an integer must be coprime to a
        q: represents the quoutient of a by b
        r: represnets the remainder of a by b

        """

        """Input Validation""" 
        if not isinstance(a, int):
            raise ValueError(f"a:'{a}' is not an integer.")
        elif not isinstance(b, int):
            raise ValueError(f"b:'{b}' is not an integer.")
        elif not isinstance(show_math_expr, bool):
            raise ValueError(f"chained:'{show_math_expr}' is not a bool")

        if a <= b:
            a , b = b, a # Switch a and b
        if int(a) <= 1:
            raise ValueError(f"a:'{a}' must be greater than 1")
        
        """Logical Implementation"""
        gcd: int = -1
        current_dividend: int = a # Set initial value for dividend to a
        current_divisor: int = b # Set initail value for divisor to b
        quotient: int = a // b # Find the quotient of a by b
        remainder: int = a % b # Find the remainder of a by b

        # Initialize chain

        math_expr_output: Dict[List[Dict]]  = {
            "expr_list": [{"id": 0, "a": a, "b": b, "q": quotient, "r": remainder}]
        }


        while remainder != 0: # Loops until a = bq + r leaves a 0 remainder
            if current_divisor % remainder == 0: # checks if the next expression of a = bq + r leaves a 0 remainder
                gcd = remainder
            current_dividend = current_divisor # Update current dividend to previous divisor
            current_divisor = remainder # Update current divisor to previous remainder
            quotient = current_dividend // current_divisor
            remainder = current_dividend % current_divisor
            
            if show_math_expr:
                id = len(math_expr_output["expr_list"])
                math_expr_output["expr_list"].append({"id": id, "a": current_dividend, "b": current_divisor, "q": quotient, "r": remainder})

        if show_math_expr:
            math_expr_output["gcd"] = gcd
            return math_expr_output
        return gcd

    def find_coprime(self, input_integer: int) -> int:
        """Finds coprime for given input_integer(n)"""

        """Input Validation"""
        if not isinstance(input_integer, int):
            raise ValueError(f"n:'{input_integer}' is not an integer but of type: {type(input_integer)}.")

        """Logical Implementation"""
        while True:
            candidate: int = random.randrange(2, input_integer)
            if self.is_coprime(a=input_integer, b=candidate):
                return candidate



    def solve_inverse_modulo(self, e: int, tn: int):
        """Brute force implementation to find multiplicative inverse modulo 

        -- Variables 'tn' and 'e' are used to compute the mathematical expression of: e * d ≡ 1 (mod tn)

        e: represents the public exponent
        d: represents the inverse modulo
        tn: represnets totient of n, it is the modolo context for the expression

        """

        public_exponent: int = e
        totient_of_n: int = tn

        # Check if inverse modolo
        if not self.is_coprime(totient_of_n, public_exponent):
            return None
        
        # Stops once iterations reach the range of integer(e)
        for inverse_modulo_check in range(0, totient_of_n): # Increments inverse_modolo_check 
            remainder =  (public_exponent * inverse_modulo_check) % totient_of_n
            
            # print(f"(e:{public_exponent} * d:{inverse_modulo_check}) % {totient_of_n} = {remainder}")
            
            if remainder == 1: 
                return inverse_modulo_check
        return -1

    def is_coprime(self, a: int, b: int):
        """Checks if integer(a) is coprime with integer(b)

        a: represents an integer coprime to b
        b represents an integer coprime to a
        
        """
        if self.solve_gcd(a, b) == 1: # check if greatest common divisor between a and b is 1
            return True
        return False

    def is_prime(self, prime_integer: int) -> True | False:
        """Checks if given input 'a' is a prime number"""
        if prime_integer <= 1:
            return False
        for i in range(2, int(prime_integer ** 0.5) + 1):
            if prime_integer % i == 0:  # Check if prime integer is divisible by 
                return False
        return True
    
    def eval_diphon(self, a, b):
        """Implements back-substituiton to finds the diphontine equation corresponding to gcd(a,b)"""
        pass

    def find_prime_fact(self, n:int, string:bool=False):
        for p in range(int(n ** 0.5)):
            if self.is_prime(p):
                for q in range(int(n ** 0.5)):
                    if self.is_prime(q):
                        if p * q == n:
                            if string:
                                return(p,q)
                            else:
                                return f"p:{p} q:{q} of n:{n}"
        return None


    def gcd_simple(self, a, b):
        while (b > 0):
            a, b = b, a % b

            return a

    def extdgcd(self, a:int, b:int):
        """Recursive approach to extended euclidean algorithm
        
        -- Returns two coefiecents to the equation ax * by = gcd(a,b)
        """
        if a == 0:
            return (0, 1)
        else:
            x, y = self.extdgcd(b % a, a)
            x1 = y - (b // a) * x
            y1 = x

            return (x1, y1)

    def diophantine_gcd(self, a:int, b:int):
        """Returns two coefiecents and gcd to the equation ax * by = gcd(a,b)"""
        # Initialize coefficients for a and b
        x0, y0 = 1, 0  # Coefficients for `a`
        x1, y1 = 0, 1  # Coefficients for `b`

        while b != 0:
            # Perform integer division
            q = a // b  # Quotient
            r = a % b   # Remainder

            # Update a and b (Euclidean algorithm)
            a, b = b, r

            # Update coefficients
            x_new = x0 - q * x1
            y_new = y0 - q * y1

            # Shift coefficients for next iteration
            x0, x1 = x1, x_new
            y0, y1 = y1, y_new

        # When b = 0, a contains gcd(a, b) and (x0, y0) are the coefficients
        return a, x0, y0


if __name__ == "__main__":
    ph = PrimeHandler()
    # print(ph.find_coprime(77))
    # print(ph.solve_gcd(77, 60))
    print(ph.diophantine_gcd(60, 77))

    






# TODO Create a method to workout the diphontine equation of a given 


# -- DONE -- #

# TODO Create a class to handle prime factor generation

# -- DONE -- #


