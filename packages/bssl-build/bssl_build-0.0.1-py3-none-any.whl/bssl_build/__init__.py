from cffi import FFI
import importlib.resources as resources

def get_library_path(lib_name):
    return resources.path(__package__, lib_name)

def load_bssl_libraries(ffi: FFI):
    """
    Loads the BoringSSL libraries (libcrypto and libssl) using the provided FFI instance.
    This function assumes `ffi.cdef` has already been called by the user.
    """
    with get_library_path('libcrypto.so') as libcrypto_path, \
         get_library_path('libssl.so') as libssl_path:
        libcrypto = ffi.dlopen(str(libcrypto_path))
        libssl = ffi.dlopen(str(libssl_path))
    return libcrypto, libssl
