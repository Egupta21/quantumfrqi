#quantum_functions.py

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
from qiskit.circuit.library.standard_gates import RYGate, RYYGate
from qiskit.quantum_info import Statevector
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
from .data_management import convert_to_image

def num_qubit_finder(height, width):
    pix_upper = max(height, width)
    x = math.log2(pix_upper)
    x = math.ceil(x)
    num_qubit = 1
    while math.pow(2, num_qubit) < 2**x*2**x*2:
        num_qubit = num_qubit + 1
    return num_qubit

def hadamard(circ, n):
    for i in n:
        circ.h(i)
        
def change(state, new_state):
    n = len(state)
    c = np.array([])
    for i in range(n):
        if state[i] != new_state[i]:
            c = np.append(c, int(i))     
    if len(c) > 0:
        return c.astype(int)
    else:
        return c

def binary(circ, state, new_state, num_qubit):
    changed_indices = change(state, new_state)
    if len(changed_indices) > 0:
        for index in changed_indices:
            circ.x(index)
    else:
        pass

def cnri(circ, n, t, theta):
    controls = len(n)
    if controls == 0:
        raise ValueError("At least one control qubit must be specified")
    cry = RYGate(2*theta).control(controls)
    aux = np.append(n, t).tolist()
    circ.append(cry, aux)
    
def frqi(circ, n, t, angles):
    #t=num_qubit-1
    hadamard(circ, n)
    j = 0
    for i in angles:
        print("running frqi at angle index" + str(j))
        state = '{0:0{width}b}'.format(j-1, width=t)
        new_state = '{0:0{width}b}'.format(j, width=t)
        if j == 0:
            cnri(circ, n, t, i)
        else:
            binary(circ, state, new_state, t+1)
            cnri(circ, n, t, i)
        j += 1

def make_circ(num_qubit, dataset):
    img_side = math.sqrt(math.pow(2, num_qubit-1))
    img_side = int(img_side)
    # Read the Excel file
    dataset = pd.read_excel(dataset)
    # Reshape the array
    images = dataset.to_numpy()[0,:].reshape(1,img_side,img_side)
    pixel_values = images.reshape(1, img_side*img_side)
    plt.imshow(images[0,:], cmap='gray')
    normalized_pixels = pixel_values/255.0
    qr = QuantumRegister(num_qubit, 'q')
    cr = ClassicalRegister(num_qubit,'c')
    
    qc = QuantumCircuit(qr,cr)
    angles = np.arcsin(normalized_pixels[0])
    
    frqi(qc, list(range(num_qubit-1)), num_qubit-1, angles)
    
    #qc.draw(output='mpl', style="clifford")
    #plt.show()
    print(qc.draw(output='text'))
    return qc
    
def decode(counts, num_qubit, output_file, num_shots=1024*1024):
    img_side = math.sqrt(math.pow(2, num_qubit-1))
    img_side = int(img_side)
    print(img_side)
    retrieved_image = np.array([])
    
    for i in range(img_side*img_side):
        #print("running")
        try:
            s = format(i, '0' + str(num_qubit - 1) + 'b')
            new_s = '1' + s
            #retrieve_image = np.append(retrieve_image,np.sqrt(result.get_counts(qc)[new_s]/num_shots))
            retrieved_image = np.append(retrieved_image, np.sqrt(counts[new_s] / num_shots))
        except KeyError:
            retrieved_image = np.append(retrieved_image,[0.0])
    
    retrieved_image *=  img_side*255.0
    retrieved_image = retrieved_image.astype('int')
    retrieved_image = retrieved_image.reshape((img_side, img_side))
    print(retrieved_image)
    convert_to_image(retrieved_image, output_file)
    plt.imshow(retrieved_image, cmap='gray', vmin=0, vmax=255)
    plt.show()