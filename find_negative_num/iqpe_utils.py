import numpy as np


def get_controlled_unitary(unitary:list):
    '''
    Returns controlled version of the passed unitary matrix

    Args:
    unitary (Numpy Array): The required Unitary Matrix

    Returns:
    c_unitary (Numpy Array):  Controlled form of the passed unitary
    '''

    # Define projectors onto the computational basis
    p0 = np.array([[1.0, 0.0], [0.0, 0.0]])

    p1 = np.array([[0.0, 0.0], [0.0, 1.0]])

    # Construct numpy matrix
    id_matrix = np.eye(len(unitary))
    c_unitary = np.kron(p0, id_matrix) + np.kron(p1,unitary)

    return c_unitary


def isPowerOfTwo(n:int):
    '''
    Checks if a given integer is a Power of Two by using the concept of set bits in an integer. 
    Every value which is the power of two has only one bit with value 1 in its binary string representation.
    We count the values in the binary representation of the value. If the count is 1, the number is a power of two. 
    Otherwise, it is not.

    Args:
    n (int): integer value of the numer to evaluate

    Returns False if count of 1 in bitstring of inout is not 1, True otherwise
    '''
    if n==1:
        return False
    count = 0
    while n > 0:
        if n & 1 == 1:
            count = count + 1
        n = n >> 1
    
    if count != 1 :
        return False
    else:
        return True
    
def convert_to_decimal(theta_binary:str, cz_angle:bool):
    '''
    Returns the fraction form of the phase (theta)

    Args:
    theta (str): binary string representing the iqpe output

    Returns:
    theta (float): The decimal base value of the inverse rotation angle theta
    theta_frac (tuple): The Fractional value of the inverse rotation angle theta as a tuple (numerator, denominator)
    '''
    if cz_angle:
        theta_binary = '0' + theta_binary
    bitstring = list()
    for index, result in enumerate(list(theta_binary)):
        bitstring.append(int(result)/(2**(index+1)))

    correction_angle = np.sum(bitstring)
    correction_angle_frac = correction_angle.as_integer_ratio()

    return correction_angle, correction_angle_frac