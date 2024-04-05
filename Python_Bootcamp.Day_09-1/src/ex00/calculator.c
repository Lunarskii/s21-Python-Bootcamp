#define PY_SSIZE_T_CLEAN
#include <Python.h>

static int parse_numbers(PyObject* args, double* number1, double* number2)
{
    if (!PyArg_ParseTuple(args, "dd", number1, number2))
    {
        PyErr_SetString(PyExc_TypeError, "Invalid arguments, expected two numbers.");
        return 0;
    }

    return 1;
}

static PyObject* add_func(PyObject* self, PyObject* args)
{
    double number1 = 0;
    double number2 = 0;

    if (parse_numbers(args, &number1, &number2))
    {
        return Py_BuildValue("d", number1 + number2);
    }

    return NULL;
}

static PyObject* sub_func(PyObject* self, PyObject* args)
{
    double number1 = 0;
    double number2 = 0;

    if (parse_numbers(args, &number1, &number2))
    {
        return Py_BuildValue("d", number1 - number2);
    }

    return NULL;
}

static PyObject* mul_func(PyObject* self, PyObject* args)
{
    double number1 = 0;
    double number2 = 0;

    if (parse_numbers(args, &number1, &number2))
    {
        return Py_BuildValue("d", number1 * number2);
    }

    return NULL;
}

static PyObject* div_func(PyObject* self, PyObject* args)
{
    double number1 = 0;
    double number2 = 0;

    if (parse_numbers(args, &number1, &number2))
    {
        if (number2 == 0)
        {
            PyErr_SetString(PyExc_ZeroDivisionError, "Cannot divide by zero");
            return NULL;
        }
        return Py_BuildValue("d", number1 / number2);
    }

    return NULL;
}

static PyMethodDef CalculatorFunctions[] =
{
    {"add", add_func, METH_VARARGS, "Addition of two numbers"},
    {"sub", sub_func, METH_VARARGS, "Subtraction of two numbers"},
    {"mul", mul_func, METH_VARARGS, "Multiplication of two numbers"},
    {"div", div_func, METH_VARARGS, "Division of two numbers"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef CalculatorModule =
{
    PyModuleDef_HEAD_INIT,
    "calculator",
    "A module with primitive logical operations in C",
    -1,
    CalculatorFunctions
};

PyMODINIT_FUNC
PyInit_calculator(void)
{
    return PyModule_Create(&CalculatorModule);
}