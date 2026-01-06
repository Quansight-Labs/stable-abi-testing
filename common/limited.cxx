#include <nanobind/nanobind.h>

long add(long a, long b) {
    return a + b;
}

NB_MODULE(limited, m) {
    m.def("add", &add);
}
