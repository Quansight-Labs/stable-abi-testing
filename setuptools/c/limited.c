#include <Python.h>

#ifndef Py_LIMITED_API
#error Py_LIMITED_API must be defined.
#endif

static PyObject *
hello(PyObject * Py_UNUSED(self), PyObject * Py_UNUSED(args)) {
    return PyUnicode_FromString("hello world");
}

static struct PyMethodDef methods[] = {
    { "hello", hello, METH_NOARGS, NULL },
    { NULL, NULL, 0, NULL },
};

static PyModuleDef_Slot limited_module_slots[] = {
    {Py_mod_name, "limited"},
    {Py_mod_methods, methods},
    {0}
};

PyMODEXPORT_FUNC PyModExport_limited(void) {
	return limited_module_slots;
}
