import random
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Given two sequences of length n, calculate hamming distance between the two. 
def hamming_distance(chaine1, chaine2):
    return sum(c1 != c2 for c1, c2 in zip(chaine1, chaine2))

# generate random bit string of length n
def random_bits(n):
    return format(random.randint(0, 2**n - 1), f'0{n}b')

def invert_bits(string):
    inverse = ""
    for bit in string:
        inverse += '1' if bit == '0' else '0'
    
    return inverse

# # equal strings
# s1 = "1010101010101"
# s2 = "1010101010101"
# print("size: ", len(s1))
# print(hamming_distance(s1, s2))

# # two random strings
# s3 = random_bits(5)
# s4 = random_bits(5)
# print(s3, s4)
# print("size: ", 5)
# print(hamming_distance(s3, s4))


iterations = 1000


# list of qubit measurements
# qubits = [random_bits(iterations) for _ in range(num_qubits)]

# q1 and q4 are same, q1 and q2 are inverse, q3 is independent
q1 = random_bits(iterations)
q2 = invert_bits(q1)
q3 = random_bits(iterations)
q4 = q1

qubits = [q1, q2, q3, q4]

num_qubits = len(qubits)
# 2D array to compare qubits against each other, but not against themselves
matrix = [[-0.1 for i in range(num_qubits)] for j in range(num_qubits)]

for r in range(0, num_qubits):
    for c in range(0, num_qubits):
        if r != c: 
            matrix[r][c] = hamming_distance(qubits[r], qubits[c]) / iterations # division to place values between 0 and 1

heatmap = np.matrix(matrix)
mask = np.triu(heatmap) # this masks out the upper triangular 
print(heatmap)

# using matplotlib
# plt.imshow(heatmap, cmap='hot', interpolation='nearest')

# using seaborn
labels = [x for x in range(1, num_qubits+1)]
# get rid of mask parameter to stop masking out upper triangular
ax = sns.heatmap(heatmap, linewidth=0.5, annot=True, xticklabels=labels, yticklabels=labels, mask=mask)
plt.show()
