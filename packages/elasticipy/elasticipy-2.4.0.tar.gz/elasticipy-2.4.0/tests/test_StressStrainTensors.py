import unittest
from pytest import approx
import numpy as np
from scipy.spatial.transform import Rotation

from Elasticipy.FourthOrderTensor import StiffnessTensor
import Elasticipy.StressStrainTensors as Tensors
from Elasticipy.SecondOrderTensor import SymmetricSecondOrderTensor


Cmat = [[231, 127, 104, 0, -18, 0],
        [127, 240, 131, 0, 1, 0],
        [104, 131, 175, 0, -3, 0],
        [0, 0, 0, 81, 0, 3],
        [-18, 1, -3, 0, 11, 0],
        [0, 0, 0, 3, 0, 85]]
C = StiffnessTensor(Cmat)


class TestStrainStressTensors(unittest.TestCase):
    def test_mult_by_stiffness(self):
        """
        Test Stiffness/Strain tensors product C*eps (which stands for C:E)
        """
        tensile_dir = [1, 0, 0]
        stress = Tensors.StressTensor([[1, 0, 0],
                                       [0, 0, 0],
                                       [0, 0, 0]])
        strain = C.inv()*stress
        eps_xx = strain.C[0, 0]
        eps_yy = strain.C[1, 1]
        eps_zz = strain.C[2, 2]
        E = C.Young_modulus.eval(tensile_dir)
        nu_y = C.Poisson_ratio.eval(tensile_dir, [0, 1, 0])
        nu_z = C.Poisson_ratio.eval(tensile_dir, [0, 0, 1])
        assert eps_xx == approx(1/E)
        assert eps_yy == approx(-nu_y / E)
        assert eps_zz == approx(-nu_z / E)

    def test_rotate_tensor(self, n_oris=100):
        """
        Test the rotation of a tensor

        Parameters
        ----------
        n_oris : int
            Number of random orientations to use
        """
        random_tensor = Tensors.SymmetricSecondOrderTensor(np.random.random((3, 3)))
        random_oris = Rotation.random(n_oris)
        eps_rotated = random_tensor * random_oris
        for i in range(n_oris):
            rot_mat = random_oris[i].as_matrix()
            eps_matrix_th = np.matmul(np.matmul(rot_mat.T, random_tensor.matrix), rot_mat)
            np.testing.assert_almost_equal(eps_matrix_th, eps_rotated[i].matrix)

    def test_transpose_array(self, shape=(1, 2, 3)):
        """
        Test transposing a tensor array

        Parameters
        ----------
        shape : tuple
            Shape of the tensor array to use
        """
        random_matrix = np.random.random(shape + (3, 3))
        random_tensor = Tensors.SymmetricSecondOrderTensor(random_matrix)
        transposed_tensor = random_tensor.transposeArray()
        for i in range(shape[0]):
            for j in range(shape[1]):
                for k in range(shape[2]):
                    sym_mat = 0.5 * (random_matrix[i, j, k] + random_matrix[i, j, k].T)
                    np.testing.assert_array_equal(sym_mat, transposed_tensor[k, j, i].matrix)

    def test_mul(self, shape=(4, 5)):
        """
        Test the element-wise product of tensors.

        Parameters
        ----------
        shape : tuple
            Shape of the tensor arrays to use.
        """
        shape = shape + (3, 3)
        matrix1 = np.random.random(shape)
        matrix2 = np.random.random(shape)
        tensor_prod = Tensors.SymmetricSecondOrderTensor(matrix1) * Tensors.SymmetricSecondOrderTensor(matrix2)
        for i in range(shape[0]):
            for j in range(shape[1]):
                sym_mat1 = 0.5 * (matrix1[i, j] + matrix1[i, j].T)
                sym_mat2 = 0.5 * (matrix2[i, j] + matrix2[i, j].T)
                mat_prod = np.matmul(sym_mat1, sym_mat2)
                np.testing.assert_array_equal(tensor_prod[i, j].matrix, mat_prod)

    def test_matmul(self, length1=3, length2=4):
        """
        Test the matrix-like product of tensor arrays

        Parameters
        ----------
        length1 : int
            Length of the first array
        length2 : int
            Length of the second array
        """
        matrix1 = np.random.random((length1, 3, 3))
        matrix2 = np.random.random((length2, 3, 3))
        rand_tensor1 = Tensors.SymmetricSecondOrderTensor(matrix1)
        rand_tensor2 = Tensors.SymmetricSecondOrderTensor(matrix2)
        cross_prod_tensor = rand_tensor1.matmul(rand_tensor2)
        for i in range(0, length1):
            sym_mat1 = 0.5 * (matrix1[i] + matrix1[i].T)
            for j in range(0, length2):
                sym_mat2 = 0.5 * (matrix2[j] + matrix2[j].T)
                mat_prod = np.matmul(sym_mat1, sym_mat2)
                np.testing.assert_array_equal(cross_prod_tensor[i, j].matrix, mat_prod)

    def test_matmul_rotation(self, m=5, n=100):
        random_tensor = SymmetricSecondOrderTensor(np.random.random((m,) + (3, 3)))
        random_oris = Rotation.random(n)
        array = random_tensor.matmul(random_oris)
        assert array.shape == (m, n)
        for i in range(m):
            for j in range(n):
                rot_mat = random_oris[j].as_matrix()
                matrix = np.matmul(np.matmul(rot_mat.T, random_tensor[i].matrix), rot_mat)
                np.testing.assert_almost_equal(matrix, array[i,j].matrix)

    def test_statistics(self, shape=(5, 4, 3, 2)):
        """
        Test the std, min and max functions for tensor arrays.

        Parameters
        ----------
        shape : tuple
            Shape of the tensor to use
        """
        matrix = np.random.random(shape + (3, 3))
        tensor = Tensors.SymmetricSecondOrderTensor(matrix)
        matrix = 0.5 *(matrix + np.swapaxes(matrix, -2, -1))
        mini = tensor.min()
        maxi = tensor.max()
        std = tensor.std()
        # First, check T.std()
        for i in range(0, 3):
            for j in range(0, 3):
                Cij = matrix[..., i, j].flatten()
                assert np.std(Cij) == approx(std.C[i, j])
                assert np.min(Cij) == approx(mini.C[i, j])
                assert np.max(Cij) == approx(maxi.C[i, j])
        # Then, check T.std(axis=...)
        for i in range(0, len(shape)):
            np.testing.assert_array_equal(tensor.std(axis=i).matrix, np.std(matrix, axis=i))
            np.testing.assert_array_equal(tensor.min(axis=i).matrix, np.min(matrix, axis=i))
            np.testing.assert_array_equal(tensor.max(axis=i).matrix, np.max(matrix, axis=i))

    def test_ddot(self, shape=(4, 3, 2)):
        """
        Test the ddot method.

        Parameters
        ----------
        shape : tuple
            shape of the tensor arrays to use
        """
        matrix1 = np.random.random(shape + (3, 3))
        matrix2 = np.random.random(shape + (3, 3))
        tens1 = Tensors.SymmetricSecondOrderTensor(matrix1)
        tens2 = Tensors.SymmetricSecondOrderTensor(matrix2)
        ddot = tens1.ddot(tens2)
        for i in range(0, shape[0]):
            for j in range(0, shape[1]):
                for k in range(0, shape[2]):
                    sym_mat1 = 0.5* (matrix1[i, j, k] + matrix1[i, j, k].T)
                    sym_mat2 = 0.5* (matrix2[i, j, k] + matrix2[i, j, k].T)
                    ddot_th = np.trace(np.matmul(sym_mat1, sym_mat2))
                    self.assertEqual(ddot_th, ddot[i, j, k])

    def test_vonMises_Tresca(self):
        """
        Check that the Tresca and von Mises methods work well for simple tension, simple shear and hydrostatic
        pressure.
        """
        matrix = np.zeros((3, 3, 3))
        matrix[0, 0, 0] = 1  # Simple tension
        matrix[1, 1, 0] = matrix[1, 0, 1] = 1  # Simple shear
        matrix[2, np.arange(3), np.arange(3)] = -1  # Hydrostatic pressure
        stress = Tensors.StressTensor(matrix)

        vM_stress = stress.vonMises()
        vm_th = np.array([1, np.sqrt(3), 0.0])
        np.testing.assert_array_equal(vM_stress, vm_th)

        Tresca_stress = stress.Tresca()
        Tresca_th = np.array([1, 2, 0.0])
        np.testing.assert_array_equal(Tresca_stress, Tresca_th)

    def test_rotation_stiffness(self, n_strain=50, n_ori=100):
        """
        Check that the two ways to compute stress from a rotated stiffness tensor are consistent.

        Parameters
        ----------
        n_strain : int
            Number of strain tensors to consider
        n_ori : int
            Number of random orientation to consider
        """
        matrix = np.random.random((n_strain, 3, 3))
        eps = Tensors.StrainTensor(matrix)
        ori = Rotation.random(n_ori)
        C_rotated = C * ori
        sigma = C_rotated * eps

        # Rotate stress and stress by their own
        eps_rot = eps.matmul(ori)
        sigma_rot2 = C * eps_rot
        sigma2 = sigma_rot2 * ori.inv()
        np.testing.assert_almost_equal(sigma.matrix, sigma2.transposeArray().matrix)

    def test_multidimensional_tensors(self, shape_strain=(5, 4, 3), n_ori=100):
        """
        Check that the shape of (C * rotations) * eps is (m, p, r, ...) if rotation.shape=(p, q,...) and
        len(rotations)=m.

        Parameters
        ----------
        shape_strain : tuple
            shape of tensor array
        n_ori : int
            number of orientations to consider
        """
        strain = Tensors.StrainTensor.ones(shape_strain)
        ori = Rotation.random(n_ori)
        C_rotated = C * ori
        stress = C_rotated * strain
        self.assertEqual(stress.shape, (n_ori,) + shape_strain)

    def test_Voigt_notation_strain(self):
        a = np.random.random((3, 4 , 6))
        strain = Tensors.StrainTensor.from_Voigt(a)
        for i in range(0, 3):
            for j in range(0, 4):
                for k in range(0, 6):
                    if k<3:
                        assert a[i,j,k] == strain[i,j].C[k,k]
                    elif k==3:
                        assert a[i,j,k] == 2*strain[i,j].C[1,2]
                    elif k==4:
                        assert a[i,j,k] == 2*strain[i,j].C[0,2]
                    else:
                        assert a[i,j,k] == 2*strain[i,j].C[0,1]

    def test_Voigt_notation_stress(self):
        a = np.random.random((3, 4 , 6))
        stress = Tensors.StressTensor.from_Voigt(a)
        for i in range(0, 3):
            for j in range(0, 4):
                for k in range(0, 6):
                    if k<3:
                        assert a[i,j,k] == stress[i,j].C[k,k]
                    elif k==3:
                        assert a[i,j,k] == stress[i,j].C[1,2]
                    elif k==4:
                        assert a[i,j,k] == stress[i,j].C[0,2]
                    else:
                        assert a[i,j,k] == stress[i,j].C[0,1]

if __name__ == '__main__':
    unittest.main()
