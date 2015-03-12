import numpy as np
import numpy.linalg as linalg
from argparse import ArgumentParser



parser = ArgumentParser()
parser.add_argument("--polynomial", type=str, help="enter the polynomial to use Routh-Hurwitz criterion on")
parser.add_argument("--coefficients", type=str, help="enter the list of coefficients for a polynomial, it is assumed here that all degrees are non zero unless specified with a 0")
args = parser.parse_args()



class Polynomial:

    def __init__(self):
        self.poly_tuples = list()
        self.degree = 0
        self.stable = True
        
    #preprocess string into polynome tuples
    def preprocess(self, polynomial):
    
        if "-" in polynomial and "+" in polynomial:
            return None
        else:
            
            #split the string into its different powers
            components = polynomial.split("+") if "+" in polynomial else polynomial.split("-")
            for element in components:
                if "^" in element:
                    #split the term into its coefficient 
                    element = element.split("s^")
                    coeff = element[0] if element[0] != '' else 1
                    self.poly_tuples.append((float(coeff), int(element[-1])))
                else:
                    if "s" in element:
                        coeff = element[0:-1] if element[0:-1] != '' else 1
                        self.poly_tuples.append((float(coeff), 1))
                    else:
                        self.poly_tuples.append((float(element), 0))
                        
            #degree check
            self.degree = max([x[1] for x in self.poly_tuples]) 
            if len(self.poly_tuples) != self.degree+1:
                return None
            else:
                return "OK"


    def is_stable(self):
        #matrix contaning the calculated values
        i_range = self.degree + 1
        j_range = 1 + self.degree/2

        
        mat = np.zeros(shape=(self.degree+1, 1+ self.degree/2))
        coefficients = [x[0] for x in self.poly_tuples]

        k=0
        for coef in coefficients[::2]:
            mat[0][k] =  coef
            k += 1
            
        k=0
        for coef in coefficients[1::2]:
            mat[1][k] = coef
            k += 1

        i=2
        while i< i_range:
            for j in xrange(j_range-1):
                mat[i][j] = -linalg.det([[mat[i-2][0], mat[i-2][j+1]], [mat[i-1][0], mat[i-1][j+1]]])/mat[i-1][0]
                if mat[i][j] < 0:
                    self.stable = False
            i += 1

        print mat
        print "System is Stable" if self.stable  else "System is Unstable"
                
            
        
p = Polynomial()
status =p.preprocess(args.polynomial)
if status is None:
    print "System is unstable"
else:
    p.is_stable()
