################################################################################
# polymath/pair.py: Pair subclass of PolyMath Vector
################################################################################

from __future__ import division
import numpy as np
import numbers

from polymath.qube   import Qube
from polymath.scalar import Scalar
from polymath.vector import Vector

class Pair(Vector):
    """A PolyMath subclass containing coordinate pairs or 2-vectors.
    """

    NRANK = 1           # the number of numerator axes.
    NUMER = (2,)        # shape of the numerator.

    FLOATS_OK = True    # True to allow floating-point numbers.
    INTS_OK = True      # True to allow integers.
    BOOLS_OK = False    # True to allow booleans.

    UNITS_OK = True     # True to allow units; False to disallow them.
    DERIVS_OK = True    # True to allow derivatives and to allow this class to
                        # have a denominator; False to disallow them.

    DEFAULT_VALUE = np.array([1,1])

    #===========================================================================
    @staticmethod
    def as_pair(arg, recursive=True):
        """The argument converted to Pair if possible.

        If recursive is True, derivatives will also be converted.

        As a special case as_pair() of a single value returns a Pair with the
        value repeated.
        """

        # Pair: just return the input arg
        if isinstance(arg, Pair):
            if recursive:
                return arg
            return arg.wod

        # Qube (not Pair): convert to Pair if possible
        if isinstance(arg, Qube):

            # Collapse a 1x2 or 2x1 Matrix down to a Pair
            if arg._numer_ in ((1,2), (2,1)):
                return arg.flatten_numer(Pair, recursive=recursive)

            # For any suitable Qube, move numerator items to the denominator
            if arg.rank > 1 and arg._numer_[0] == 2:
                arg = arg.split_items(1, Pair)

            arg = Pair(arg._values_, arg._mask_, example=arg)
            if recursive:
                return arg
            return arg.wod

        # Single number: broadcast to Pair
        if isinstance(arg, numbers.Real):
            return Pair((arg,arg))

        # Everything else
        return Pair(arg)

    #===========================================================================
    @staticmethod
    def from_scalars(x, y, recursive=True, readonly=False):
        """A Pair constructed by combining two scalars.

        Inputs:
            args        any number of Scalars or arguments that can be casted
                        to Scalars. They need not have the same shape, but it
                        must be possible to cast them to the same shape. A value
                        of None is converted to a zero-valued Scalar that
                        matches the denominator shape of the other arguments.

            recursive   True to include all the derivatives. The returned object
                        will have derivatives representing the union of all the
                        derivatives found amongst the scalars. Default is True.

            readonly    True to return a read-only object; False (the default)
                        to return something potentially writable.
        """

        return Qube.from_scalars(x, y, recursive=recursive, readonly=readonly,
                                       classes=[Pair])

    #===========================================================================
    def swapxy(self, recursive=True):
        """A pair object in which the first and second values are switched.

        If recursive is True, derivatives will also be swapped.
        """

        if not recursive:
            self = self.wod

        # Roll the array axis to the end
        lshape = len(self._values_.shape)
        new_values = np.rollaxis(self._values_, lshape - self._drank_ - 1,
                                                lshape)

        # Swap the axes
        new_values = new_values[..., ::-1]

        # Roll the axis back
        new_values = np.rollaxis(new_values, -1, lshape - self._drank_ - 1)

        # Construct the object
        obj = Pair(new_values, self._mask_, example=self)

        # Fill in the derivatives if necessary
        if recursive:
            for (key, deriv) in self._derivs_.items():
                obj.insert_deriv(key, deriv.swapxy(False))

        return obj

    #===========================================================================
    def rot90(self, recursive=True):
        """A pair object rotated 90 degrees from the origin, (x,y) -> (y,-x).

        If recursive is True, derivatives will also be rotated.
        """

        # Roll the array axis to the end
        lshape = len(self._values_.shape)
        new_values = np.rollaxis(self._values_, lshape - self._drank_ - 1,
                                                lshape)

        # Swap the axes and negate the new y
        new_values = new_values[..., ::-1]

        # Roll the axis back
        new_values = np.rollaxis(new_values, -1, lshape - self._drank_ - 1)

        # Construct the object
        new_values[...,1] = -new_values[...,1]      # negate the new y-axis
        obj = Pair(new_values, self._mask_, example=self)

        # Fill in the derivatives if necessary
        if recursive:
            for (key, deriv) in self._derivs_.items():
                obj.insert_deriv(key, deriv.rot90(False))

        return obj

    #===========================================================================
    def angle(self, recursive=True):
        """Polar angle of this Pair as measured from the X-axis toward the
        Y-axis.

        The returned value will always fall between zero and 2*pi.

        Inputs:
            recursive   True to include the derivatives. Default is True.
        """

        (x, y) = self.to_scalars(recursive=recursive)
        return y.arctan2(x) % Scalar.TWOPI

    #===========================================================================
    def clip2d(self, lower, upper, remask=False):
        """A copy with values clipped to fall within 2D limits.

        Values get moved to the nearest location within a rectangle defined by
        the lower and upper limits.

        Optionally, the clipped values can also be masked.

        Inputs:
            lower           coordinates of the lower limit. None or masked value
                            to ignore.
            upper           coordinates of the upper limit (inclusive). None or
                            masked value to ignore.
            remask          True to include the new mask into the object's mask;
                            False to replace the values but leave them unmasked.
        """

        # Make sure the lower limit is either None or an unmasked Pair
        if lower is not None:
            lower = Pair.as_pair(lower)
            if lower._shape_:
                raise ValueError('Pair.clip2d() lower limit must contain '
                                 'exactly two values')
            if lower._mask_:
                lower = None

        # Make sure the upper limit is either None or an unmasked Pair
        if upper is not None:
            upper = Pair.as_pair(upper)
            if upper._shape_:
                raise ValueError('Pair.clip2d() upper limit must contain '
                                 'exactly two values')
            if upper._mask_:
                upper = None

        # Define the clipping limits
        if lower is None:
            lower0 = None
            lower1 = None
        else:
            (lower0, lower1) = lower.to_scalars()

        if upper is None:
            upper0 = None
            upper1 = None
        else:
            (upper0, upper1) = upper.to_scalars()

        # Clip...
        result = self
        result = result.clip_component(0, lower0, upper0, remask)
        result = result.clip_component(1, lower1, upper1, remask)
        return result

################################################################################
# Useful class constants
################################################################################

Pair.ZERO   = Pair((0.,0.)).as_readonly()
Pair.ZEROS  = Pair((0.,0.)).as_readonly()
Pair.ONES   = Pair((1.,1.)).as_readonly()
Pair.HALF   = Pair((0.5,0.5)).as_readonly()
Pair.XAXIS  = Pair((1.,0.)).as_readonly()
Pair.YAXIS  = Pair((0.,1.)).as_readonly()
Pair.MASKED = Pair((1,1), True).as_readonly()

Pair.IDENTITY = Pair([(1.,0.),(0.,1.)], drank=1).as_readonly()

Pair.INT00 = Pair((0,0)).as_readonly()
Pair.INT11 = Pair((1,1)).as_readonly()

################################################################################
# Once defined, register with Qube class
################################################################################

Qube.PAIR_CLASS = Pair

################################################################################
