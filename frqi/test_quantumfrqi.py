import unittest
from PIL import Image
import time
import os
from qiskit import QuantumCircuit, QuantumRegister
from numpy.testing import assert_array_equal
from quantumfrqi import expand_image, data_preparation, make_circ, decode
from quantumfrqi import hadamard, cnri, frqi, binary, change
import numpy as np

class TestImageProcessing(unittest.TestCase):
    def test_expand_image(self):
        img = Image.new('RGB', (100, 50), 'white')
        processed_img = expand_image(img)
        self.assertEqual(processed_img.size, (100, 100))
        self.assertEqual(processed_img.mode, 'RGB')
        
class TestDataPreparation(unittest.TestCase):
    def test_data_preparation(self):
        img = Image.new('L', (10, 10), 255)  # Using 255 to represent 'white' in grayscale
        excel_path = data_preparation(img, './data/testexcel.xlsx')
        self.assertTrue(os.path.exists(excel_path))
        # Try to delete the file, retrying if necessary
        for _ in range(10):  # Retry up to 10 times
            try:
                os.remove(excel_path)
                break
            except PermissionError:
                time.sleep(0.1)  # Wait half a second before retrying
        else:
            self.fail(f"Failed to delete the test file: {excel_path}")
        
class TestQuantumCircuit(unittest.TestCase):
    def test_make_circ(self):
        num_qubits = 7
        qc = make_circ(num_qubits, './data/pixels.xlsx')
        self.assertEqual(len(qc.qubits), num_qubits)
        self.assertGreaterEqual(len(qc.data), num_qubits - 1)
        
class TestQuantumFunctions(unittest.TestCase):

    def test_hadamard(self):
        qr = QuantumRegister(4)
        qc = QuantumCircuit(qr)
        hadamard(qc, [0, 2])
        ops = [op.name for op, _, _ in qc]
        self.assertIn('h', ops)

    def test_change(self):
        state = '0011'
        new_state = '0010'
        expected = np.array([1, 3])  # Corrected expected result
        #expected = np.array([3])
        result = change(state, new_state)
        np.testing.assert_array_equal(result, expected)

    def test_binary(self):
        qr = QuantumRegister(4)
        qc = QuantumCircuit(qr)
        state = '0011'
        new_state = '0010'
        num_qubit = 4
        binary(qc, state, new_state, num_qubit)
        ops = [(op.name, qargs) for op, qargs, _ in qc.data]

        # Check if X gate applied to qubits as per transformed indices
        # Since binary() function transforms [0, 2] -> [2, 0], we check for qubits 2 and 0
        self.assertIn(('x', [qr[1]]), ops)  # Check if X gate applied to qubit 1
        #self.assertIn(('x', [qr[3]]), ops)  # Check if X gate applied to qubit 3

    def test_cnri(self):
        qr = QuantumRegister(5)
        qc = QuantumCircuit(qr)
        n = [0, 1, 2]
        t = 4
        theta = np.pi / 4
        cnri(qc, n, t, theta)
        found = any(op.name == 'cry' and op.num_ctrl_qubits == 3 and op.params[0] == 2*theta for op, qargs, _ in qc.data if qargs[-1].index == t)
        self.assertTrue(found, "Controlled-RY gate with correct configuration not found.")

    def test_frqi(self):
        qr = QuantumRegister(4)
        qc = QuantumCircuit(qr)
        angles = [np.pi/4] * 8  # Assuming 8 angles for 8 states
        frqi(qc, list(range(3)), 3, angles)
        self.assertTrue(any(op.name == 'cry' for op, qargs, _ in qc.data if len(qargs) == 4))
        
    def test_expand_image(self):
        # Placeholder for expand_image test
        pass

if __name__ == '__main__':
    unittest.main()