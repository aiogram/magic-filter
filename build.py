import os

if not os.getenv("SKIP_CYTHON", None):
    try:
        from Cython.Build import cythonize
    except ImportError:
        cythonize = None
        ext_modules = None
    else:
        compiler_directives = {}
        if os.getenv("CYTHON_TRACE", False):
            compiler_directives["linetrace"] = True
        os.environ["CFLAGS"] = "-O3"
        ext_modules = cythonize(
            ["magic_filter/*.py", "magic_filter/operations/*.py"],
            exclude=[],
            nthreads=int(os.getenv("CYTHON_NTHREADS", 0)),
            language_level=3,
            compiler_directives=compiler_directives,
        )
else:
    ext_modules = None


def build(setup_kwargs):
    """
    This function is mandatory in order to build the extensions.
    """
    if ext_modules:
        setup_kwargs.update({"ext_modules": ext_modules})
