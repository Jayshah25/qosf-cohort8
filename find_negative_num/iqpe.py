import numpy as np
from qiskit import QuantumCircuit, BasicAer, execute
from qiskit.extensions import UnitaryGate

from iqpe_utils import isPowerOfTwo, get_controlled_unitary, convert_to_decimal

class IQPE:

    def __init__(self,unitary,ket_psi,precision_bits,SHOTS):
        self.unitary = unitary
        self.ket_psi = ket_psi
        self.precision_bits = precision_bits
        self.SHOTS = SHOTS
        self.backend = BasicAer.get_backend('qasm_simulator')

        # Exception handling
        if not (np.round(unitary.dot(np.conj(unitary).T),5)==np.eye(len(unitary)).astype(complex)).all():
            raise ValueError("The passed matrix is not Unitary")
        if not isPowerOfTwo(len(self.unitary)):
            raise ValueError("Input Unitary Matrix is not an N-qubit operator.")
        if len(self.unitary)!=len(self.ket_psi):
            raise ValueError("The dimensions of the Unitary and EigenVector don't match")
        if round(np.linalg.norm(ket_psi),9)!=1:
            print("Sum of amplitudes-squared does not equal one for the |psi>.")
            print("Iterative_QPE has normalized |psi>")
            l2_norm = np.linalg.norm(self.ket_psi)
            self.ket_psi = self.ket_psi / round(l2_norm,9)
            print("The modified |psi>: ")
            print(self.ket_psi)

    def iqpe(self, precision_bit:int, theta_reverse:str):
        num_qubits = int(np.log2(len(self.unitary)))
        circuit = QuantumCircuit(num_qubits + 1,1)

        # step 1
        # Prepare q[0] in |+>
        # Prepare Eigenstate for 
        circuit.h(0)
        # initial_state = np.kron(self.ket_psi,[1/np.sqrt(2),1/np.sqrt(2)])
        # print('is',circuit.qubits)
        circuit.initialize(self.ket_psi,circuit.qubits[1:])
        # eigen_state_gate = UnitaryGate(self.ket_psi,label='eigen state')
        # circuit.append(eigen_state_gate,list(range(1,int(np.log2(len(self.ket_psi))))))

        # step 2
        # Get the Controlled Unitary (C-Unitary)
        # raise the C-Unitary to 2**t times and apply it
        c_unitary = get_controlled_unitary(self.unitary)
        c_unitary_powered = np.linalg.matrix_power(c_unitary, 2 ** (self.precision_bits-precision_bit))
        c_u_gate = UnitaryGate(c_unitary_powered,f'2**{self.precision_bits-precision_bit}')
        circuit.append(c_u_gate,list(range(int(np.log2(len(c_unitary_powered))))))

        # step 3 (inverse rotation) 
        # apply rz rotations to eliminate relative phase
        if precision_bit>=2:
            theta = theta_reverse[::-1]
            inverse_rotation_angle, inverse_rotation_angle_frac = convert_to_decimal(theta, True)

            # if previous bit values are zero, no rz rotation
            if inverse_rotation_angle!=0:
                circuit.rz(-2*np.pi*inverse_rotation_angle,0)

        # Step 4 (QFT Inverse)
        circuit.h(0)

        # measure ancillary qubit
        circuit.measure(0,0)

        job = execute(circuit,backend=self.backend,shots=self.SHOTS)

        job_result = job.result()

        # get the measurement results
        meas_result = job_result.get_counts()

        # get the meas_result with highest frequency
        result = list(meas_result.keys())[np.argmax(list(meas_result.values()))]

        return result
    
    def solve(self):

        '''
        Implements Iterative Quantum Phase Estimation

        Returns:
        theta_binary (str): Binary string representation of theta
        theta (float): Value of theta converted from binary string to decimal
        theta_frac(tuple): fractional representation of the obtained value of theta as tuple (Numerator, Denominator)
        phi (float): Calculated Value of phi from theta (phi = 2 * PI * theta)
        '''



        # initialize string object to store the result theta
        theta_reverse = ''

        for precision_bit in range(self.precision_bits):

            # get the circuit result
            result = self.iqpe(precision_bit=precision_bit+1,theta_reverse=theta_reverse)
            
            # store the bit information
            theta_reverse+=result[0]  

        
        # reverse the theta bit string
        theta_binary = theta_reverse[::-1]

        theta, theta_frac = convert_to_decimal(theta_binary,False)

        phi = 2 * np.pi * theta

        
        return theta_binary, theta, theta_frac, phi
        