"""
A module that implements Private Authentication Keys into your application.
"""

class PK():
    import random
    
    def __init__(self, *args, **kwargs):
        """
        Represents a private key.
        """
        self._pk = None
        self.choices = self.alphabet

    def generate(self, bits=1024):
        """
        Generates a private key using the specified number of bits. This private key is randomly generated every time.
        
        @param bits: The number of bits to generate
        """
        _pk = [self.random.choice(self.choices) for _ in range(bits)]
        self._pk = "".join(_pk)
        return self._pk
        
    @property
    def alphabet(self):
        return["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
               "-","_","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y", "Z"]
        
    def __str__(self):
        """
        Returns a string representation of the private key.
        """
        if not self._pk:
            raise RuntimeError("Private key was not generated during initialization (during conversion to a string)")
        
        return str(self._pk)