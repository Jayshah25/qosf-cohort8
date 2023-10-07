# QOSF Cohourt 8

## Task - For a given list, return True if there exists a negative number or return False otherwise

## Approach

0. Break the given list into a list of lists with the size of each list being 4. Pad the lists with 1 when required. This is to make the algorithm NISQ era friendly.

```For example, a given list [a,-b,c,d,e] changes to [[a,-b,c,d],[e,1,1,1]]```

FOR EACH LIST

1. Using simple element wise self division, transform a given list [a,-b,c,d] to [1,-1,1,1]

2. Create a diagonal matrix U of size (len(list) X len(list)) with diagonal entries as [1,-1,1,1]

3. Since for a diagonal matrix, diagonal values are the eigen values, we can obtain eigen vector for each diagonal entry

4. Use Iterative Phase Estimation to estimate the phase for each eigenvalue-eigenvector pair

5. If a phase of 3.142 is found, it corresponds to a negative value. Therefore, the algorithm returns `TRUE`

6. If a phase of 3.142 is not found (all phases are 0), it corresponds to all positive numbers. The algorithm returns `FALSE`

## Advantages

1. The Algorithm is NISQ Era friendly since it requires only 3 qubits to run the algorithm.

2. The algorithm will successfully solve the challenge irrespective of the magnitude of the positive/negative number due to the use of self division.

3. The Algorithm uses the popular Iterative Quantum Phase Estimation technique at its core to solve the problem.

## Limitations

1. A given list must be padded with Ones to the next power of 2 when required.

2. The algorithm correctly differentiates the case of all positive numbers versus a case where list contains negative values and successfully solves the problem at hand. However, in the case of multiple negative values it messes up the index of the phase value.