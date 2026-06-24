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

#if PY_VERSION_HEX >= 0x030F00A8
PyABIInfo_VAR(abi_info);
#endif

#if PY_VERSION_HEX >= 0x030F00B0

static PySlot limited_module_slots[] = {
    PySlot_STATIC_DATA(Py_mod_name, "limited"),
    PySlot_STATIC_DATA(Py_mod_methods, methods),
    PySlot_DATA(Py_mod_gil, Py_MOD_GIL_NOT_USED),
    PySlot_DATA(Py_mod_abi, &abi_info),
    PySlot_END,
};

#else

static PyModuleDef_Slot limited_module_slots[] = {
    {Py_mod_name, "limited"},
    {Py_mod_methods, methods},
#if PY_VERSION_HEX >= 0x030D0000
    {Py_mod_gil, Py_MOD_GIL_NOT_USED},
#endif
#if PY_VERSION_HEX >= 0x030F00A8
    {Py_mod_abi, &abi_info},
#endif
    {0}
};

#endif

PyMODEXPORT_FUNC PyModExport_limited(void) {
    return limited_module_slots;
}

PyMODINIT_FUNC PyInit_limited(void) {
    PyErr_SetString(PyExc_NotImplementedError, "legacy init not supported");
    return NULL;
}
