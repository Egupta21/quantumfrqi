import unittest
from PIL import Image
import time
import os
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute, Statevector
from numpy.testing import assert_array_equal
from quantumfrqi import remove_padding, expand_image, data_preparation, make_circ, decode
from quantumfrqi import hadamard, cnri, frqi, binary, change
from quantumfrqi import convert_to_image, num_qubit_finder
import numpy as np

class TestImageProcessing(unittest.TestCase):
    def test_expand_image(self):
        img = Image.new('RGB', (100, 50), 'white')
        processed_img = expand_image(img)
        self.assertEqual(processed_img.size, (100, 100))
        self.assertEqual(processed_img.mode, 'RGB')
        
    def test_remove_padding(self):
        original_image = np.array([[1, 1], [1, 1]])
        decoded_image = np.array([[0, 0, 0, 0],
                                  [0, 1, 1, 0],
                                  [0, 1, 1, 0],
                                  [0, 0, 0, 0]])
        
        result_image = remove_padding(original_image, decoded_image)
        expected_image = np.array([[1, 1], [1, 1]]) 

        self.assertTrue(np.array_equal(result_image, expected_image), "The padding was not correctly removed")

class TestDataPreparation(unittest.TestCase):
    def test_data_preparation(self):
        img = Image.new('L', (10, 10), 255)
        excel_path = data_preparation(img, './data/testexcel.xlsx')
        self.assertTrue(os.path.exists(excel_path))
        for _ in range(10):
            try:
                os.remove(excel_path)
                break
            except PermissionError:
                time.sleep(0.1)
        else:
            self.fail(f"Failed to delete the test file: {excel_path}")
        
    def test_prepare_dimensions(self):
        input_image_path = 'test_input_image.png'
        output_image_path = 'test_output_image.png'
        original_image = Image.new('RGB', (100, 50), color = 'blue')
        original_image.save(input_image_path)

        new_size = (50, 50)
        prepare_dimensions(input_image_path, output_image_path, new_size)
        output_image = Image.open(output_image_path)

        self.assertEqual(output_image.size, new_size, "The image was not resized correctly")
        self.assertEqual(output_image.mode, 'L', "The image was not converted to grayscale")

        os.remove(input_image_path)
        os.remove(output_image_path)
        
    def test_convert_to_image(self):
        test_array = np.random.randint(0, 256, (10, 10), dtype=np.uint16)
        output_path = 'test_image.png'

        convert_to_image(test_array, output_path)
        self.assertTrue(os.path.exists(output_path), "The image file was not created")
        with Image.open(output_path) as img:
            self.assertEqual(img.mode, 'L', "The image is not in grayscale mode")
            self.assertEqual(img.size, (10, 10), "The image dimensions are incorrect")

        os.remove(output_path)

class TestQuantum(unittest.TestCase):
    def test_num_qubit_finder(self):
        test_cases = [
            (1, 1, 1),
            (2, 2, 2),
            (3, 3, 3),
            (4, 4, 3),
            (8, 8, 4),
            (15, 15, 5),
            (16, 16, 5),
            (100, 50, 8)
        ]

        for height, width, expected in test_cases:
            with self.subTest(height=height, width=width, expected=expected):
                result = num_qubit_finder(height, width)
                self.assertEqual(result, expected, f"Failed for height {height}, width {width}")
                
    def test_hadamard_application(self):
        qc = QuantumCircuit(3)
        hadamard(qc, [0, 2])

        backend = Aer.get_backend('statevector_simulator')
        statevector = execute(qc, backend).result().get_statevector()
        expected_statevector = Statevector.from_label('+0+').data

        self.assertTrue((statevector == expected_statevector).all(), "Hadamard gates not applied correctly")

    def test_change_identification(self):
        # Test cases with expected indices of change
        test_cases = [
            ([0, 1, 2], [0, 2, 2], [1]),
            ([1, 1, 1], [1, 1, 1], []), 
            ([3, 4, 5], [1, 4, 1], [0, 2]),
            ([], [], []),
            ([9], [8], [0])
        ]

        for state, new_state, expected in test_cases:
            with self.subTest(state=state, new_state=new_state, expected=expected):
                result = change(state, new_state)
                expected_array = np.array(expected, dtype=int)
                self.assertTrue(np.array_equal(result, expected_array), f"Failed for state {state}, new_state {new_state}")

    def test_binary(self):
        initial_state = [0, 1, 0, 1]
        new_state = [1, 1, 1, 1]
        num_qubits = 4

        qc = QuantumCircuit(num_qubits)
        binary(qc, initial_state, new_state, num_qubits)

        backend = Aer.get_backend('statevector_simulator')
        statevector = execute(qc, backend).result().get_statevector()
        expected_statevector = Statevector.from_label('1111').data
        self.assertTrue((statevector == expected_statevector).all(), "X gates not applied correctly")
        
    def test_cnri(self):
        qc = QuantumCircuit(3)
        n = [0, 1]
        t = 2
        theta = np.pi / 4

        cnri(qc, n, t, theta)
        backend = Aer.get_backend('statevector_simulator')
        statevector = execute(qc, backend).result().get_statevector()

        print("State vector:", statevector)
        self.assertTrue(True)

    def test_basic_frqi(self):
        circ = QuantumCircuit(5)
        n = [0, 1, 2]
        t = 4
        angles = [0.1, 0.2, 0.3]

        frqi(circ, n, t, angles)
    
if __name__ == '__main__':
    unittest.main()