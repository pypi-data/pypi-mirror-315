################################################################################
# polymath/matrix.py: Matrix subclass ofse PolyMath base class
################################################################################

from __future__ import division, print_function
import numpy as np
import warnings

from polymath.qube    import Qube
from polymath.scalar  import Scalar
from polymath.boolean import Boolean
from polymath.vector  import Vector
from polymath.vector3 import Vector3
from polymath.units   import Units

class Matrix(Qube):
    """A Qube of arbitrary 2-D matrices."""

    NRANK = 2           # the number of numerator axes.
    NUMER = None        # shape of the numerator.

    FLOATS_OK = True    # True to allow floating-point numbers.
    INTS_OK = False     # True to allow integers.
    BOOLS_OK = False    # True to allow booleans.

    UNITS_OK = True     # True to allow units; False to disallow them.
    DERIVS_OK = True    # True to allow derivatives and to allow this class to
                        # have a denominator; False to disallow them.

    DEBUG = False       # Set to True for some debugging tasks
    DELTA = np.finfo(float).eps * 3     # Cutoff used in unary()

    #===========================================================================
    @staticmethod
    def as_matrix(arg, recursive=True):
        """The argument converted to Matrix if possible."""

        if type(arg) == Matrix:
            if recursive:
                return arg
            return arg.wod

        if isinstance(arg, Qube):

            # Convert a Vector with drank=1 to a Matrix
            if isinstance(arg, Vector) and arg._drank_ == 1:
                return arg.join_items([Matrix])

            arg = Matrix(arg._values_, arg._mask_, example=arg)
            if recursive:
                return arg
            return arg.wod

        return Matrix(arg)

    #===========================================================================
    def row_vector(self, row, recursive=True, classes=(Vector3,Vector)):
        """The selected row of a Matrix as a Vector.

        If the Matrix is M x N, then this will return a Vector of length N. By
        default, if N == 3, it will return a Vector3 object instead.

        Input:
            row         index of the row to return.
            recursive   True to return corresponding vectors of derivatives.
            classes     a list of classes; an instance of the first suitable
                        class is returned. Default is to return a Vector3 if
                        the length is 3, otherwise a Vector.
        """

        return self.extract_numer(0, row, classes, recursive=recursive)

    #===========================================================================
    def row_vectors(self, recursive=True, classes=(Vector3,Vector)):
        """A tuple of Vector objects, one for each row of this Matrix.

        If the Matrix is M x N, then this will return M Vectors of length N. By
        default, if N == 3, it will return Vector3 objects instead.

        Input:
            recursive   True to return corresponding vectors of derivatives.
            classes     a list of classes; instances of the first suitable
                        class are returned. Default is to return Vector3 objects
                        if the length is 3, otherwise a Vector.
        """

        vectors = []
        for row in range(self._numer_[0]):
            vectors.append(self.extract_numer(0, row, classes,
                                                      recursive=recursive))

        return tuple(vectors)

    #===========================================================================
    def column_vector(self, column, recursive=True, classes=(Vector3,Vector)):
        """The selected column of a Matrix as a Vector.

        If the Matrix is M x N, then this will return a Vector of length M. By
        default, if M == 3, it will return a Vector3 object instead.

        Input:
            column      index of the column to return.
            recursive   True to return corresponding vectors of derivatives.
            classes     a list of classes; an instance of the first suitable
                        class is returned. Default is to return a Vector3 if
                        the length is 3, otherwise a Vector.
        """

        return self.extract_numer(1, column, classes, recursive=recursive)

    #===========================================================================
    def column_vectors(self, recursive=True, classes=(Vector3,Vector)):
        """A tuple of Vector objects, one for each column of this Matrix.

        If the Matrix is M x N, then this will return N Vectors of length M. By
        default, if M == 3, it will return Vector3 objects instead.

        Input:
            recursive   True to return corresponding vectors of derivatives.
            classes     a list of classes; instances of the first suitable
                        class are returned. Default is to return Vector3 objects
                        if the length is 3, otherwise a Vector.
        """

        vectors = []
        for col in range(self._numer_[1]):
            vectors.append(self.extract_numer(1, col, classes,
                                                      recursive=recursive))

        return tuple(vectors)

    #===========================================================================
    def to_vector(self, axis, indx, classes=[], recursive=True):
        """One of the components of a Matrix as a Vector.

        Input:
            axis        axis index from which to extract vector.
            indx        index of the vector along this axis.
            classes     a list of the Vector subclasses to return. The first
                        valid one will be used. Default is Vector.
            recursive   True to extract the derivatives as well.
        """

        return self.extract_numer(axis, indx, list(classes) + [Vector],
                                  recursive=recursive)

    #===========================================================================
    def to_scalar(self, indx0, indx1, recursive=True):
        """One of the elements of a Matrix as a Scalar.

        Input:
            indx0       index along the first matrix axis.
            indx1       index along the second matrix axis.
            recursive   True to extract the derivatives as well.
        """

        vector = self.extract_numer(0, indx0, Vector, recursive=recursive)
        return vector.extract_numer(0, indx1, Scalar, recursive=recursive)

    #===========================================================================
    @staticmethod
    def from_scalars(*args, **keywords):
        """A Matrix or subclass constructed by combining scalars.

        Inputs:
            args        any number of Scalars or arguments that can be casted
                        to Scalars. They need not have the same shape, but it
                        must be possible to cast them to the same shape. A value
                        of None is converted to a zero-valued Scalar that
                        matches the denominator shape of the other arguments.

            recursive   True to include all the derivatives. The returned object
                        will have derivatives representing the union of all the
                        derivatives found amongst the scalars. Default is True.

            shape       The Matrix's item shape. If not specified but the number
                        of Scalars is a perfect square, a square matrix is
                        returned.

            classes     an arbitrary list defining the preferred class of the
                        returned object. The first suitable class in the list
                        will be used. Default is Matrix.

        Note that the 'recursive' and 'classes' inputs are handled as keyword
        arguments in order to distinguish them from the scalar inputs.
        """

        # Search for keyword "shape" and "classes"
        # Pass "recursive" to the next function
        item = None
        if 'shape' in keywords:
            item = keywords['shape']
            del keywords['shape']

        classes = []
        if 'classes' in keywords:
            classes = keywords['classes']
            del keywords['classes']

        # No other keyword is allowed
        if keywords:
          raise ValueError('Matrix.from_scalars() got an unexpected keyword '
                           'argument "%s"'
                           % (list(keywords.keys())[0]))

        # Create the Vector object
        vector = Vector.from_scalars(*args, **keywords)

        # Int matrices are disallowed
        if vector.is_int():
            raise TypeError('Matrix.from_scalars() requires objects with data '
                            'type float')

        # Determine the shape
        if item is not None:
            if len(item) != 2:
                raise ValueError('invalid Matrix shape: %s' % item)

            size = item[0] * item[1]
            if len(args) != item:
                raise ValueError('incorrect number of Scalars for '
                                 'Matrix.from_scalars() with shape %s'
                                 % item)
            item = tuple(item)

        else:
            dim = int(np.sqrt(len(args)))
            size = dim*dim
            if size != len(args):
                raise ValueError('incorrect number of Scalars for '
                                 'Matrix.from_scalars() with square shape')
            item = (dim, dim)

        return vector.reshape_numer(item, list(classes) + [Matrix],
                                    recursive=True)

    #===========================================================================
    def is_diagonal(self, delta=0.):
        """A Boolean equal to True where the matrix is diagonal.

        Masked matrices return True.

        Input:
            delta           the fractional limit on what can be treated as a
                            equivalent to zero in the off-diagonal terms. It is
                            scaled by the RMS value of all the elements in the
                            matrix.

        """

        size = self.item[0]
        if size != self.item[1]:
            raise ValueError('%s.is_diagonal() requires a square matrix; '
                             'shape is %s'
                             % (type(self).__name__, self._numer_))

        if self._drank_:
            raise ValueError('%s.is_diagonal() does not support denominators'
                             % type(self).__name__)

        # If necessary, calculate the matrix RMS
        if delta != 0.:
            # rms, scaled to be unity for an identity matrix
            rms = (np.sqrt(np.sum(np.sum(self._values_**2, axis=-1), axis=-1)) /
                                                                        size)

        # Flatten the value array
        values = self._values_.reshape(self._shape_ + (size*size,))

        # Slice away the last element
        sliced = values[...,:-1]

        # Reshape so that only elemenents in the first column can be nonzero
        reshaped = sliced.reshape(self._shape_ + (size-1, size+1))

        # Slice away the first column
        sliced = reshaped[...,1:]

        # Convert back to 1-D items
        reshaped = sliced.reshape(self._shape_ + ((size-1) * size,))

        # Compare
        if delta == 0:
            compare = (reshaped == 0.)
        else:
            compare = (np.abs(reshaped) <= (delta * rms)[...,np.newaxis])

        compare = np.all(compare, axis=-1)

        # Apply mask
        if np.shape(compare) == ():
            if self._mask_:
                compare = True
        elif np.shape(self._mask_) == ():
            if self._mask_:
                compare.fill(True)
        else:
            compare[self._mask_] = True

        return Boolean(compare)

    #===========================================================================
    def transpose(self, recursive=True):
        """Transpose of this matrix.

        Input:
            recursive   True to include the transposed derivatives; False to
                        return an object without derivatives.
        """

        return self.transpose_numer(0, 1, recursive=recursive)

    #===========================================================================
    @property
    def T(self):
        """Shorthand notation for the transpose of a rotation matrix."""

        return self.transpose_numer(0, 1, recursive=True)

    #===========================================================================
    def inverse(self, recursive=True, nozeros=False):
        """Inverse of this matrix.

        The returned object will have the same subclass as this object.

        Input:
            recursive   True to include the derivatives of the inverse.
            nozeros     False (the default) to mask out any matrices with zero-
                        valued determinants. Set to True only if you know in
                        advance that all determinants are nonzero.
        """

        # Validate array
        if self._numer_[0] != self._numer_[1]:
            raise ValueError('%s.inverse() requires a square matrix; '
                             'shape is %s'
                             % (type(self).__name__, self._numer_))

        if self._drank_:
            raise ValueError('%s.inverse() does not support denominators'
                             % type(self).__name__)

        # Check determinant if necessary
        if not nozeros:
            det = np.linalg.det(self._values_)

            # Mask out un-invertible matrices and replace with identify matrices
            mask = (det == 0.)
            if np.any(mask):
                self._values_[mask] = np.diag(np.ones(self._numer_[0]))
                new_mask = Qube.or_(self._mask_, mask)
            else:
                new_mask = self._mask_

        # Invert the array
        with warnings.catch_warnings():
            warnings.filterwarnings('error')
            try:
                new_values = np.linalg.inv(self._values_)
            except RuntimeWarning:
                raise ValueError('%s.inverse() input has determinant == 0'
                                 % type(self).__name__)

        # Construct the result
        obj = Matrix(new_values, new_mask,
                     units = Units.units_power(self._units_,-1))

        # Fill in derivatives
        if recursive and self._derivs_:
            new_derivs = {}

            # -M^-1 * dM/dt * M^-1
            for (key, deriv) in self._derivs_.items():
                new_derivs[key] = -obj * deriv * obj

            obj.insert_derivs(new_derivs)

        return obj

    #===========================================================================
    def unitary(self):
        """The nearest unitary matrix as a Matrix3."""

        # Algorithm from
        #    wikipedia.org/wiki/Orthogonal_matrix#Nearest_orthogonal_matrix

        MAX_ITERS = 10      # Adequate iterations unless convergence is failing

        m0 = self.wod
        if m0._drank_:
            raise ValueError('%s.unitary() does not support denominators'
                             % type(self).__name__)

        if m0._numer_ != (3,3):
            raise ValueError('%s.unitary() requires 3x3 matrix as input'
                             % type(self).__name__)

        # Iterate...
        next_m = m0
        for i in range(MAX_ITERS):
            m = next_m
            next_m = 2. * m0 * (m.inverse() * m0 + m0.T * m).inverse()
            rms = Qube.rms(next_m * next_m.T - Matrix.IDENTITY3)

            if Matrix.DEBUG:
                sorted = np.sort(rms._values_.ravel())
                print(i, sorted[-4:])

            if rms.max() <= Matrix.DELTA:
                break

        new_mask = (rms._values_ > Matrix.DELTA)
        if not np.any(new_mask):
            new_mask = self._mask_
        elif self._mask_ is not False:
            new_mask |= self._mask

        return Qube.MATRIX3_CLASS(next_m._values_, new_mask)

# Algorithm has been validated but code has not been tested
#     def solve(self, values, recursive=True):
#         """Solve for the Vector X that satisfies A X = B, for this square matrix
#         A and a Vector B of results."""
#
#         b = Vector.as_vector(values, recursive=True)
#
#         size = self.item[0]
#         if size != self.item[1]:
#             raise ValueError('solver requires a square Matrix')
#
#         if self._drank_:
#             raise ValueError('solver does not suppart a Matrix with a ' +
#                              'denominator')
#
#         if size != b.item[0]:
#             raise ValueError('Matrix and Vector have incompatible sizes')
#
#         # Easy cases: X = A-1 B
#         if size <= 3:
#             if recursive:
#                 return self.inverse(True) * b
#             else:
#                 return self.inverse(False) * b.wod
#
#         new_shape = Qube.broadcasted_shape(self._shape_, b._shape_)
#
#         # Algorithm is simpler with matrix indices rolled to front
#         # Also, Vector b's elements are placed after the elements of Matrix a
#
#         ab_vals = np.empty((size,size+1) + new_shape)
#         rolled = np.rollaxis(self._values_, -1, 0)
#         rolled = np.rollaxis(rolled, -1, 0)
#
#         ab_vals[:,:-1] = rolled
#         ab_vals[:,-1] = b._values_
#
#         for k in range(size-1):
#             # Zero out the leading coefficients from each row at each iteration
#             ab_saved = ab_vals[k+1:,k:k+1]
#             ab_vals[k+1:,k:] *= ab_vals[k,k:k+1]
#             ab_vals[k+1:,k:] -= ab_vals[k,k:] * ab_saved
#
#         # Now work backward solving for values, replacing Vector b
#         for k in range(size,0):
#             ab_vals[ k,-1] /= ab_vals[k,k]
#             ab_vals[:k,-1] -= ab_vals[k,-1] * ab_vals[:k,k]
#
#         ab_vals[0,-1] /= ab_vals[0,0]
#
#         x = np.rollaxis(ab_vals[:,-1], 0, len(shape))
#
#         x = Vector(x, self._mask_ | b._mask_, derivs={},
#                       units=Units.units_div(self._units_, b._units_))
#
#         # Deal with derivatives if necessary
#         # A x = B
#         # A dx/dt + dA/dt x = dB/dt
#         # A dx/dt = dB/dt - dA/dt x
#
#         if recursive and (self._derivs_ or b._derivs_):
#             derivs = {}
#             for key in self._derivs_:
#                 if key in b._derivs_:
#                     values = b._derivs_[key] - self._derivs_[key] * x
#                 else:
#                     values = -self._derivs_[k] * x
#
#             derivs[key] = self.solve(values, recursive=False)
#
#             for key in b._derivs_:
#                 if key not in self._derivs_:
#                     derivs[key] = self.solve(b._derivs_[k], recursive=False)
#
#             self.insert_derivs(derivs)
#
#         return x

    ############################################################################
    # Overrides of superclass operators
    ############################################################################

    def __abs__(self):
        Qube._raise_unsupported_op('abs()', self)

    def __floordiv__(self, arg):
        Qube._raise_unsupported_op('//', self, arg)

    def __rfloordiv__(self, arg):
        Qube._raise_unsupported_op('//', arg, self)

    def __ifloordiv__(self, arg):
        Qube._raise_unsupported_op('//=', self, arg)

    def __mod__(self, arg):
        Qube._raise_unsupported_op('%', self, arg)

    def __rmod__(self, arg):
        Qube._raise_unsupported_op('%', arg, self)

    def __imod__(self, arg):
        Qube._raise_unsupported_op('%=', self, arg)

    def identity(self):
        """An identity matrix of the same size and subclass as this."""

        size = self._numer_[0]

        if self._numer_[1] != size:
            raise ValueError('%s.identity() requires a square matrix; '
                             'shape is %s'
                             % (type(self).__name__, self._numer_))

        values = np.zeros((size,size))
        for i in range(size):
            values[i,i] = 1.

        obj = Qube.__new__(type(self))
        obj.__init__(values)

        return obj.as_readonly()

    ############################################################################
    # Overrides of arithmetic operators
    ############################################################################

    def reciprocal(self, recursive=True, nozeros=False):
        """An object equivalent to the reciprocal of this object.

        Input:
            recursive   True to return the derivatives of the reciprocal too;
                        otherwise, derivatives are removed.
            nozeros     False (the default) to mask out any zero-valued items in
                        this object prior to the divide. Set to True only if you
                        know in advance that this object has no zero-valued
                        items.
        """

        return self.inverse(recursive=recursive, nozeros=nozeros)

################################################################################
# Useful class constants
################################################################################

Matrix.IDENTITY2 = Matrix([[1,0,],[0,1,]]).as_readonly()
Matrix.IDENTITY3 = Matrix([[1,0,0],[0,1,0],[0,0,1]]).as_readonly()

Matrix.MASKED2 = Matrix([[1,1],[1,1]], True).as_readonly()
Matrix.MASKED3 = Matrix([[1,1,1],[1,1,1],[1,1,1]], True).as_readonly()

Matrix.ZERO33 = Matrix([[0,0,0],[0,0,0],[0,0,0]]).as_readonly()
Matrix.UNIT33 = Matrix([[1,0,0],[0,1,0],[0,0,1]]).as_readonly()

Matrix.ZERO3_ROW = Matrix([[0,0,0]]).as_readonly()
Matrix.XAXIS_ROW = Matrix([[1,0,0]]).as_readonly()
Matrix.YAXIS_ROW = Matrix([[0,1,0]]).as_readonly()
Matrix.ZAXIS_ROW = Matrix([[0,0,1]]).as_readonly()

Matrix.ZERO3_COL = Matrix([[0],[0],[0]]).as_readonly()
Matrix.XAXIS_COL = Matrix([[1],[0],[0]]).as_readonly()
Matrix.YAXIS_COL = Matrix([[0],[1],[0]]).as_readonly()
Matrix.ZAXIS_COL = Matrix([[0],[0],[1]]).as_readonly()

################################################################################
# Once defined, register with base class
################################################################################

Qube.MATRIX_CLASS = Matrix

################################################################################
