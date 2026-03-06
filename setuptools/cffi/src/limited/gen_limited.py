from cffi import FFI

ffibuilder = FFI()

ffibuilder.set_source(
    "limited._limited",
    r"""
    #include <stdint.h>

    static int64_t add(int64_t a, int64_t b) {
        return a + b;
    }
    """,
    libraries=[],
)

ffibuilder.cdef(
    r"""
    int64_t add(int64_t a, int64_t b);
    """
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
