from .utility import PrimeHandler
from typing import List, Dict
class KeyGenerator(PrimeHandler):
    def __init__(self, debug=False) -> None:
        self.debug = debug
        super().__init__()


    def generate(self, debug=False):
        """Method to create complete rsa key set
        
        -- returns dictionary containing public_exponent, private_exponent and rsa_modoulus
        """
        payload: Dict = self.__generate_private_exponent_from_public_exponent()
        self.debug = debug

        return {
            "public exponent": payload["e"],
            "private exponent": payload["d"],
            "rsa_modulus": payload["n"]
        }


    
    
    def __generate_private_exponent_from_public_exponent(self):
        """Generates private exponent for rsa encrpytion
        
        -- returns d in addition to deconstructed properties from self.__generate_public_exponent()

        d: Solution to private key, and multiplicative inverse to mathematical expression of: e * d ≡ 1(mod totient_of_n)
        
        """

        public_key_payload: Dict = self.__generate_public_exponent()
        d = self.solve_inverse_modulo(e=public_key_payload["e"], tn=public_key_payload["totient_of_n"]) # Iterate until valid inverse modulo is found
        return {**public_key_payload, "d": d}


    def __generate_public_exponent(self) -> Dict:
        """Method to generate public key for rsa encryption
        
        -- returns dictionary containing 'e' in addition to deconstructed properties of self.__generate_n_and_totient_of_n()

        e: Solution to the public key, it must be an integer coprime to the totient of n 

        """

        n_and_totient_of_n_dict: Dict = self.__generate_n_and_totient_of_n()
        e = self.find_coprime(n_and_totient_of_n_dict["totient_of_n"])

        return {**n_and_totient_of_n_dict, "e": e}


    def __generate_n_and_totient_of_n(self) -> Dict:
        """Method to generate n and tn values for rsa key generation
        
        -- returns dictionary contaning 'n' and 'totient_of_n'

        n: represents the solution to the mathematical expression of: p * q
            p: random prime number unique to q
            q: random prime number unique to p
        
        totient_of_n: represents the solution to the mathematical expression of: (p - 1) * (q - 1)

        """
        pq: List[int] = self.__generate_prime_numbers() # Find 2 random prime numbers for p and q
        n: int = (pq[0] * pq[1]) 
        totient_of_n: int = (pq[0] - 1) * (pq[1] - 1)

        if self.debug:
            print("\n------- OUTPUT AFTER __gen_n_tn() -------\n")
            print({"p": pq[0], "q": pq[1], "n": n, "tn": totient_of_n})
            print("\n------- OUTPUT AFTER __gen_n_tn() -------\n")

        return {"n": n, "totient_of_n": totient_of_n}


    def __generate_prime_numbers(self) -> List[int]:
        """Method to generate p and q values for rsa key generation
        
        -- returns a list containing p and q

        p: represents a random prime number unique to q
        q: represents a random prime number unique to p

        """
        p: int = self.generate_prime_number()
        q: int = self.generate_prime_number()

        while p == q:
            q = self.generate_prime_number()
        return [p, q]

