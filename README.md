# QOSF Cohourt 8

## Task - For a given list, return True if there exists a negative number or return False otherwise

## Approach

1. Using simple element wise self division, transform a given list [a,-b,c,d] to [1,-1,1,1]

2. Create a diagonal matrix U of size (len(list) X len(list)) with diagonal entries as [1,-1,1,1]

3. Since for a diagonal matrix, diagonal values are the eigen values, we can obtain eigen vector for each diagonal entry

4. Use Iterative Phase Estimation to estimate the phase for each eigenvalue-eigenvector pair

5. If a phase of 3.142 is found, it corresponds to a negative value. Therefore, the algorithm returns `TRUE`

6. If a phase of 3.142 is not found (all phases are 0), it corresponds to all positive numbers. The algorithm returns `FALSE`

## Limitations

1. A given list must be padded with Ones to the next power of 2.

2. Although the coded algorithm correctly identifies the case when there are all positive numbers and successfully solves the problem at hand, in the case of multiple negative values it messes up the index for a phase value.