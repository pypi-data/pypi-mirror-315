from typing_extensions import TypeAlias, SupportsFloat, SupportsIndex, Union
import math
import numpy 

_SupportsFloatOrIndex: TypeAlias = SupportsFloat | SupportsIndex

pi : float = 3.141592653589793
e : float = 2.718281828459045

# Point

class Point:
    def __init__(self, x: _SupportsFloatOrIndex, y: _SupportsFloatOrIndex):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self): 
        return self.__str__()

# Complex 

class Complex:
    def __init__(self, real: _SupportsFloatOrIndex, imag: _SupportsFloatOrIndex) -> None:
        self.real = real
        self.imag = imag
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __add__(self, other):
        if isinstance(other, Complex):
            return Complex(self.real + other.real, self.imag + other.imag)
        elif isinstance(other, (int, float)):
            return Complex(self.real + other, self.imag)
        
    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return Complex(other - self.real, self.imag)
        elif isinstance(other, Complex):
            return other.__sub__(self)
        else:
            return NotImplemented
    
    def __sub__(self, other):
        if isinstance(other, Complex):
            return Complex(self.real - other.real, self.imag - other.imag)
        elif isinstance(other, (int, float)):
            return Complex(self.real - other, self.imag)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Complex(other*self.real, other*self.imag)
        elif isinstance(other, Complex):
            return Complex(self.real*other.real - self.imag*other.imag, self.real*other.imag + self.imag*other.real)
        else:
            return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Complex):
            denom = other.real**2 + other.imag**2
            return Complex((self.real * other.real + self.imag * other.imag) / denom,
                           (self.imag * other.real - self.real * other.imag) / denom)
        elif isinstance(other, (int, float)):
            return Complex(self.real / other, self.imag / other)
        else:
            return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            denom = self.real**2 + self.imag**2
            return Complex((other * self.real) / denom, (-other * self.imag) / denom)
        else:
            return NotImplemented

    def __pow__(self, other):
        if isinstance(other, int):
            result = Complex(1, 0)
            base = Complex(self.real, self.imag)
            exp = other
            if exp == 0:
                return (Complex(1, 0))
            elif exp > 0:
                for _ in range(exp):
                    result *= base
            else:
                base = Complex(1, 0) / base
                exp = -exp
                for _ in range(exp):
                    result *= base
            return result
        else:
            return NotImplemented

    
    def conjugate(self) -> "Complex":
        return Complex(self.real, -self.imag)
    
    def polarForm(self) -> str:
        r = math.sqrt(self.real**2 + self.imag**2)
        theta = math.atan(self.imag/self.real)
        return f"{r}cis({theta})"
    
    def __str__(self) -> str:
        if self.real != 0 and self.imag != 0:
            return f"{self.real} {"+" if self.imag >= 0 else "-"} {abs(self.imag)}i"
        elif self.real != 0:
            return f"{self.real}"
        elif self.imag != 0:
            return f"{self.imag}i"
        return ""

# Polynomials

class Variable:
    def __init__(self, symbol : str) -> None:
        self.symbol = symbol
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Term(self, other > 0, other, 1)
        elif isinstance(other, Term):
            return Term(self, other.positive, other.coefficient, other.power + 1)
    
    def __pow__(self, power):
        if isinstance(power, (int, float)):
            return Term(self, True, 1, power)

class Term:
    def __init__(self, variable : Variable, positive : bool, coefficient : float, power : float) -> None:
        self.variable = variable
        self.positive = positive
        self.coefficient = coefficient
        self.power = power

    def __radd__(self, other):
        return self.__add__(other)

    def _rsub__(self, other):
        return self.__sub__(other)

    def __add__(self, other):
        if isinstance(other, Term):
            return Expression([self, other])
        elif isinstance(other, Variable):
            return Expression([self, Term(self.variable, True, 1, 1)])
        elif isinstance(other, (int, float)):
            return Expression([self, Term(self.variable, other > 0, other, 0)])
        elif isinstance(other, Expression):
            return Expression(other.terms + [self])
    
    def __sub__(self, other):
        if isinstance(other, Term):
            return Expression([self, Term(other.variable, False if other.positive else True, other.coefficient, other.power)])
        elif isinstance(other, Variable):
            return Expression(self, Term(self.variable, False, -1, 1))
        elif isinstance(other, (int, float)):
            return Expression([self, Term(self.variable, False, -other, 0)])
        elif isinstance(other, Expression):
            return Expression(other.terms + [self])
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Term(self.variable, self.coefficient * other > 0, self.coefficient * other, self.power)
    
    def __pow__(self, other):
        if isinstance(other, (int, float)):
            return Term(self.variable, self.coefficient ** other > 0, self.coefficient ** other, self.power * other)
    
    def __str__(self):
        if self.coefficient != 1:
            if self.power == 1:
                return f"{abs(self.coefficient)}{self.variable.symbol}"
            elif self.power == 0:
                return f"{abs(self.coefficient)}"
            else:
                return f"{abs(self.coefficient)}{self.variable.symbol}^{self.power}"
        else:
            if self.power == 1:
                return f"{self.variable.symbol}"
            elif self.power == 0:
                return f"{1}"
            else:
                return f"{self.variable.symbol}^{self.power}"

class Expression:
    def __init__(self, terms : list[Term]) -> None:
        self.terms = terms
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Expression(self.terms + [Term(self.terms[0].variable, other > 0, other, 0)])
        elif isinstance(other, (Term)):
            return Expression(self.terms + [other])

    def __rsub__(self, other):
        return self.__sub__(other)
    
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return Expression(self.terms + [Term(self.terms[0].variable, False, other, 0)])
        elif isinstance(other, (Term)):
            return Expression(self.terms + [Term(other.variable, False, other.coefficient, other.power)])

class Polynomial:
    def __init__(self, degree, expression : Expression):
        self.degree = degree
        self.expression = expression
    
    def subIn(self, x: _SupportsFloatOrIndex, complex = False) -> float:
        if complex == False:
            value = 0
            for term in self.expression.terms:
                if term.positive:
                    value += (term.coefficient*(x**term.power))
                else:
                    value -= (term.coefficient*(x**term.power))
        else:
            value = Complex(0,0)
            for term in self.expression.terms:
                if term.positive:
                    value += (term.coefficient*(x**term.power))
                else:
                    value -= (term.coefficient*(x**term.power))
        return value

    def roots(self) -> list[Point]:
        roots = []
        coefficients = []
        sorted(self.expression.terms, key= lambda t: -t.power)
        for term in self.expression.terms:
            while (self.degree - len(coefficients) > term.power):
                coefficients.append(0)

            if term.positive == False:
                coefficients.append(-term.coefficient)
            else:
                coefficients.append(term.coefficient)
        while (self.degree - len(coefficients) + 1 > 0):
            coefficients.append(0)
        npRoots = numpy.roots(coefficients)
        for root in npRoots:
            if type(root) == numpy.float64:
                roots.append(Point(root, 0)) 
            else:
                roots.append(Point(Complex(root.real, root.imag), 0))
                
        return roots

    def turningPoints(self) -> list[Point]:
        derivativePolynomial = self.derivative()
        points: list[Point] = derivativePolynomial.roots() 
        turnPoints = []
        for point in points:
            turnPoints.append(Point(point.x, self.subIn(point.x)))
        return turnPoints

    def derivative(self) -> "Polynomial":
        newTerms = []
        for term in self.expression.terms:
            if term.power != 0:
                newTerm = Term(term.variable, term.positive, term.coefficient*term.power, term.power - 1)
                newTerms.append(newTerm)

        derivedPolynomial = Polynomial(self.degree - 1, Expression(newTerms))
        return derivedPolynomial

    def gradientAt(self, x: _SupportsFloatOrIndex) -> float:
        derivativePolynomial = self.derivative()
        return derivativePolynomial.subIn(x)

    def integral(self) -> "Polynomial":
        newTerms = []
        for term in self.expression.terms:
            newTerm = Term(term.variable, term.positive, term.coefficient/(term.power+1), term.power + 1)
            newTerms.append(newTerm)
        
        integratedPolynomial = Polynomial(self.degree + 1, Expression(newTerms))
        return integratedPolynomial
    
    def definiteIntegral(self, lowerBound: _SupportsFloatOrIndex, upperBound: _SupportsFloatOrIndex) -> float:
        integratedPolynomial = self.integral()
        return integratedPolynomial.subIn(upperBound) - integratedPolynomial.subIn(lowerBound)

    def __str__(self) -> str:
        string = ""
        for term in self.expression.terms:
            if self.expression.terms.index(term) == 0:
                if term.positive == False:
                    string += "-"
            else:
                string += f'{" + " if term.positive else " - "}'
            string += term.__str__()
        return string

# Matrixes
#TODO: FIX error where you cant take determinant of a 2x2 matrix 
class Matrix:
    def __init__(self, matrix: list[list[_SupportsFloatOrIndex]]):
        self.matrix = matrix
        self.rows: int = len(matrix)
        self.columns: int = len(matrix[0])

        self._maxColumnLengths = []
        self._actualColumns = []
        
        for i in range(self.columns):
            actualColumn = []
            for j in range(self.rows):
                actualColumn.append(round(self.matrix[j][i], 2))
            self._actualColumns.append(actualColumn)

        for i in range(self.rows):
            for j in range(self.columns):
                maxColumnLength = max(len(x) for x in (str(x) for x in self._actualColumns[j]))
                self._maxColumnLengths.append(maxColumnLength)
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __add__(self, other):
        if isinstance(other, Matrix):
            if other.rows == self.rows and other.columns == self.columns:
                newMatrix = []
                for i in range(self.rows):
                    row = []
                    for j in range(self.columns):
                        row.append(self.matrix[i][j] + other.matrix[i][j])
                    newMatrix.append(row)

                return Matrix(newMatrix)
                        
            else:
                raise Exception("The addition of two matrix's require them to have the same dimensions")
        else:
            raise TypeError("Object of not type Matrix is trying to be added to a Matrix")

    def __rsub__(self, other):
        if isinstance(other, Matrix):
            if other.rows == self.rows and other.columns == self.columns:
                newMatrix = []
                for i in range(self.rows):
                    row = []
                    for j in range(self.columns):
                        row.append(other.matrix[i][j] - self.matrix[i][j])
                    newMatrix.append(row)

                return Matrix(newMatrix)
            else:
                raise Exception("The subtraction of two matrix's require them to have the same dimensions")
        else:
            raise TypeError("Object of not type Matrix is trying to be subtracte from a Matrix")
    
    def __sub__(self, other):
        if isinstance(other, Matrix):
            if other.rows == self.rows and other.columns == self.columns:
                newMatrix = []
                for i in range(self.rows):
                    row = []
                    for j in range(self.columns):
                        row.append(self.matrix[i][j] - other.matrix[i][j])
                    newMatrix.append(row)

                return Matrix(newMatrix)
            else:
                raise Exception("The subtraction of two matrix's require them to have the same dimensions")
        else:
            raise TypeError("Object of not type Matrix is trying to be subtracte from a Matrix")

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            resultingMatrix = [[other*element for element in row] for row in self.matrix]
            return Matrix(resultingMatrix)
        elif isinstance(other, Matrix):
            if self.columns == other.rows or other.columns == self.rows:
                result = [[0 for _ in range(other.columns)] for _ in range(self.rows)]

                for i in range(self.rows):
                    for j in range(other.columns):
                        for k in range(other.rows):
                            result[i][j] += self.matrix[i][k] * other.matrix[k][j]
                
                return Matrix(result)
            else:
                raise Exception("Matrix Multiplication requires the rows of one matrix to be equal to the columns of the other: Invalid Matrix Dimensions ")
        else:
            raise TypeError("Matrix's can only be multiplied by int/float scalars, or other Matrix's")

    def determinant(self) -> float:
        if self.rows == self.columns:
            if len(self.matrix) == 2:
                return self.matrix[0][0] * self.matrix[1][1] - self.matrix[1][0] * self.matrix[0][1]
            det = 0 
            for col in range(len(self.matrix)): 
                submatrix = [row[:col] + row[col + 1:] for row in self.matrix[1:]] 
                sign = (-1) ** col 
                sub_det = Matrix(submatrix).determinant()
                det += sign * self.matrix[0][col] * sub_det 

            return det  
        
        return None
    
    def transpose(self) -> "Matrix":
        newMatrix = []
        for i in range(self.columns):
            column = []
            for j in range(self.rows):
                column.append(self.matrix[j][i])
            newMatrix.append(column)
        return Matrix(newMatrix)
    
    #TODO: Implement function for cofactors and the adjoint* in future versions (code in the inverse function) 

    def inverse(self) -> "Matrix":
        if self.rows == self.columns:
            det = self.determinant()
            if det != 0:
                if self.rows == 2:
                    adjmatrix = [[self.matrix[1][1], -self.matrix[0][1]], [-self.matrix[1][0], self.matrix[0][0]]]
                    return Matrix(adjmatrix) * (1/det)
                else:
                    adjmatrix = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
                    for i in range(self.rows):
                        for j in range(self.columns):
                            submatrix = [row[:j] + row[j + 1:] for row in (self.matrix[:i] + self.matrix[i + 1:])]
                            subMatrix = Matrix(submatrix)
                            adjmatrix[i][j] = ((-1)**(i+j+2))*(subMatrix.determinant())
                    
                    adjMatrix = Matrix(adjmatrix).transpose()
                    return adjMatrix * (1/det)
            
        return None
    
    def __str__(self):
        string = f' _{(sum(self._maxColumnLengths[:self.columns])+2*self.columns-2)*" "}_\n'
        for i in range(self.rows):
            string += '|'
            if i == self.rows - 1:
                string += "_"
            for j in range(self.columns):
                maxColumnLength = max(len(x) for x in (str(x) for x in self._actualColumns[j]))
                string += f"{" "*(maxColumnLength-len(str(round(self.matrix[i][j], 2))))}{"" if i == self.rows - 1 and j == 0 else " "}{round(self.matrix[i][j], 2)}{"" if i == self.rows - 1 and j == self.columns - 1 else " "}"
            string += f'{'_' if i == self.rows - 1 else ""}|\n'
        return string
    
# 2D Vector

class Vector2:
    def __init__(self, i: _SupportsFloatOrIndex, j: _SupportsFloatOrIndex) -> None:
        self.i = i
        self.j = j

        self.magnitude = math.sqrt(self.i**2 + self.j**2)
        self.direction = math.atan(self.j/self.i)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector2(round(self.i * other, 4), round(self.j * other, 4))
        else:
            return NotImplemented
    
    def unitVector(self) -> "Vector2":
        return (1/self.magnitude) * self

    def __str__(self):
        return f"({round(self.i, 4)}, {round(self.j, 4)})"

# 3D Vector
#TODO: IMPLEMENT further vector functions (e.g. vector equation of a line) in future versions
class Vector3:
    def __init__(self, i: _SupportsFloatOrIndex, j: _SupportsFloatOrIndex, k: _SupportsFloatOrIndex) -> None:
        self.i = i
        self.j = j
        self.k = k

        self.magnitude = math.sqrt(self.i**2 + self.j**2 + self.k**2)
        self.direction = [math.atan(self.j/self.i), math.acos(self.k / self.magnitude)]

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector3(round(self.i * other, 4), round(self.j * other, 4), round(self.k * other, 4))
        elif isinstance(other, Vector3):
            return Vector3(self.j * other.k - self.k * other.j, self.k * other.i - self.i * other.k, self.i * other.j - self.j * other.i)
    
    def unitVector(self) -> "Vector3":
        return (1/self.magnitude) * self
    
    def __str__(self):
        return f"({round(self.i, 4)}, {round(self.j, 4)}, {round(self.k, 4)})"


def dotProduct(vectorA: Union[Vector2, Vector3], vectorB: Union[Vector2, Vector3]) -> float:
    if type(vectorA) == type(vectorB) and (type(vectorB) == Vector2 or type(vectorB) == Vector3):
        if type(vectorA) == Vector2:
            return vectorA.i*vectorB.i + vectorA.j*vectorB.j
        else:
            return vectorA.i*vectorB.i + vectorA.j*vectorB.j + vectorA.k*vectorB.k
    else:
        raise TypeError("Only vectors of the same type are valid inputs")

def scalarProjection(vectorA: Union[Vector2, Vector3], vectorB: Union[Vector2, Vector3]):
    if type(vectorA) == type(vectorB) and (type(vectorB) == Vector2 or type(vectorB) == Vector3):
        return dotProduct(vectorA, vectorB.unitVector())
    else:
        raise TypeError("Only vectors of the same type are valid inputs")
    
def vectorProjection(vectorA: Union[Vector2, Vector3], vectorB: Union[Vector2, Vector3]):
    if type(vectorA) == type(vectorB) and (type(vectorB) == Vector2 or type(vectorB) == Vector3):
        return (dotProduct(vectorA, vectorB) * (1 / dotProduct(vectorB, vectorB))) * vectorB
    else:
        raise TypeError("Only vectors of the same type are valid inputs")


#TODO: Implement further Specialist Applications in future versions (e.g. Partial Fractions and Integration / Differentiation with string functions, Motion?)

# Testing

#TODO: REbuild module after fixing issues


