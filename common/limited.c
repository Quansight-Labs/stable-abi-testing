#include <Python.h>

#ifndef Py_LIMITED_API
#error Py_LIMITED_API must be defined.
#endif

static PyObject *
add(PyObject * Py_UNUSED(self), PyObject *args) {
    long a, b;

    if (!PyArg_ParseTuple(args, "ll", &a, &b))
        return NULL;

    return PyLong_FromLong(a + b);
}

static struct PyMethodDef methods[] = {
    { "add", add, METH_VARARGS, NULL },
    { NULL, NULL, 0, NULL },
};

static PyModuleDef_Slot limited_module_slots[] = {
    {Py_mod_name, "limited"},
    {Py_mod_methods, methods},
#if PY_VERSION_HEX >= 0x030D0000
    {Py_mod_gil, Py_MOD_GIL_NOT_USED},
#endif
    {0}
};

PyMODEXPORT_FUNC PyModExport_limited(void) {
    return limited_module_slots;
}

PyMODINIT_FUNC PyInit_limited(void) {
    PyErr_SetString(PyExc_NotImplementedError, "legacy init not supported");
    return NULL;
}
