from qiskit import QuantumCircuit
import numpy as np

from iqpe import IQPE

def break_list(list_:list,size:int = 4):
    for i in range(0,len(list_),size):
        yield list_[i:i+size]

def get_unitary(nums_list):
    diagonal_values = []
    for num in nums_list:
        try:
            value = abs(num)//num
        except ZeroDivisionError:
            value = 1
        diagonal_values.append(value)
    unitary = np.eye(len(nums_list))
    for i in range(len(diagonal_values)):
        unitary[i,i] = diagonal_values[i]
    return unitary, diagonal_values

def find_negative_numbers(nums_list:list = [4,1,4,1], precision_bits:int = 4, SHOTS:int = 1024):
    unitary, diagonal_values = get_unitary(nums_list=nums_list)
    for j in range(len(diagonal_values)):
        ket_psi = [0] * len(diagonal_values)
        ket_psi[j] = 1
        iqpe = IQPE(unitary=unitary,ket_psi=np.array(ket_psi),precision_bits=precision_bits, SHOTS=SHOTS)
        theta_binary, theta, theta_frac, phi = iqpe.solve()
        if  phi==np.pi:
            return True
        
    return False

def main(my_list:list):
    my_lists = list(break_list(my_list,4))
    if len(my_lists[-1])!=4:
        for j in range(len(my_lists[-1]),4):
            my_lists[-1].append(1)

    for my_list in my_lists:
        result = find_negative_numbers(my_list)
        if result==True:
            print('There exists at least one negative entry!')
            return True
    
    if result==False:
        print('All numbers are positive!')
        return False
    
if __name__=='__main__':
    my_list = [-1,2,3,4,5]
    res = main(my_list=my_list)
    print(f'This is the required output -> {res}')

