# sage_setup: distribution = sagemath-modules
# Automatically generated by /tmp/build-env-fwmohsjr/lib/python3.9/site-packages/sage_setup/autogen/interpreters/internal/generator.py.  Do not edit!

from cpython.ref cimport PyObject

from sage.ext.fast_callable cimport Wrapper

from sage.rings.real_mpfr cimport RealField_class, RealNumber
from sage.libs.mpfr cimport *


cdef class Wrapper_rr(Wrapper):
    cdef RealField_class domain
    cdef int _n_args
    cdef mpfr_t* _args
    cdef int _n_constants
    cdef mpfr_t* _constants
    cdef object _list_py_constants
    cdef int _n_py_constants
    cdef PyObject** _py_constants
    cdef int _n_stack
    cdef mpfr_t* _stack
    cdef int _n_code
    cdef int* _code
    cdef object _domain
    cdef bint call_c(self,
                     mpfr_t* args,
                     mpfr_t result) except 0
