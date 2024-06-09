# A Full adder using Lambda Calculus
# Some Helper functions to convert our little scheme to python for better print readability
bl2py = lambda b: b(1)(0) # A function for convert our little scheme to python TRUE FALSE
def bl2py_list(bl):
    if CDR(bl) == F or CDR(bl) == T:
        return [bl2py(CAR(bl)), bl2py(CDR(bl))]
    elif CDR(bl) == nil:
        return [bl2py(CAR(bl))]
    else:
        return [bl2py(CAR(bl))] + bl2py_list(CDR(bl))

# define some combinators
K = lambda a: lambda b : a
KI = lambda a: lambda b: b

# True and False
T = K
F = KI

# Logic Gates
NOT = lambda p: p(F)(T)
AND = lambda p: lambda q: p(q)(p) 
OR = lambda p: lambda q: p(p)(q)
XOR = lambda p :lambda q: p(q)(NOT(q))

# Some functions 
nil = lambda f: F
CONS = lambda a, b: lambda f: f(a, b)
CAR = lambda p: p(lambda a, b: K(a)(b)) 
CDR = lambda p: p(lambda a, b: KI(a)(b))

is_nil = (XOR(lambda p: p(lambda f: F))(F))

# Take A B C and return cons(SUM, COUT)
SUM = lambda A, B, C: XOR(C)(XOR(A)(B)) 
COUT = lambda A, B, C: AND(OR(A)(B))(OR(C)(XOR(A)(B)))
FULL_ADDER = lambda A, B, C: CONS(SUM(A,B,C), COUT(A,B,C))


# The four bit adder
MULTI_BIT_ADDER = lambda A, B, C: \
    CONS(SUM(CAR(A), CAR(B), C), MULTI_BIT_ADDER(CDR(A), CDR(B), COUT(CAR(A), CAR(B), C))) if not CDR(A) == nil else CONS(SUM(CAR(A), CAR(B), C), COUT(CAR(A), CAR(B), C))

# Let's test the four bit adder
A = CONS(T, CONS(F, CONS(T, CONS(T, nil)))) # 1101
B = CONS(T, CONS(T, CONS(F, CONS(T, nil)))) # 1011
C = F # 0
# 1101 + 1011 = 11000
# and reverse is 00011

RESULT = MULTI_BIT_ADDER(A, B, C)

print("A = ", bl2py_list(A))
print("B = ", bl2py_list(B))
print("SUM = ", bl2py_list(RESULT)[:-1])
print("COUT = ", bl2py_list(RESULT)[-1])