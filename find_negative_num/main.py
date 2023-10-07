from qiskit import QuantumCircuit
import numpy as np

from iqpe import IQPE

# list1 = [-1,2,3,4]

# def get_oracle_matrix(list_nums:list):
#     diagonal_values = []
#     for num in list_nums:
#         try: 
#             value = num//num
#         except ZeroDivisionError:
#             value = 1
    
# U = np.array([[1,0,0,0],[0,1,0,0],[0,0,-1,0],[0,0,0,-1]])
# # eval, evec = np.linalg.eig(U)
# # print(len(U.tolist()))
# # print(evec)

# # declare the eigenstate (|psi>)
# ket_psi = np.array([0,1])

# # Unitary Gate (U)
# unitary = np.array([[1,0],[0,np.exp(1j*(np.pi))]]) # np.exp(1j*(2 * np.pi * 0.0053))

# # bit accuracy
# m = 4

# get a Iterative_QPE class instance
# test_case = IQPE(unitary=unitary,ket_psi=ket_psi,precision_bits=m,SHOTS=100)
# test_case.solve()
# k = np.kron(ket_psi,[1/np.sqrt(2),1/np.sqrt(2)])
# print(k)

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
    # print(unitary,diagonal_values)
    return unitary, diagonal_values

def find_negative_numbers(nums_list:list = [4,1,4,1], precision_bits:int = 4, SHOTS:int = 1024):
    unitary, diagonal_values = get_unitary(nums_list=nums_list)
    ev, evec = np.linalg.eig(unitary)
    # print(ev, evec)
    for j in range(len(diagonal_values)):
        ket_psi = [0] * len(diagonal_values)
        ket_psi[j] = 1
        iqpe = IQPE(unitary=unitary,ket_psi=np.array(ket_psi),precision_bits=precision_bits, SHOTS=SHOTS)
        theta_binary, theta, theta_frac, phi = iqpe.solve()
        if np.round(phi) == np.pi:
            return True
    return False
    
if __name__=='__main__':
    result = find_negative_numbers()
    if result==True:
        print('There exists at least one negative entry!')
    else:
        print('All numbers are positive!')
