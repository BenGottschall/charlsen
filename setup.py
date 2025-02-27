from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "chess_engine_cpp",
        ["chess_engine_cpp.cpp"],
        # Uncomment for performance boost:
        extra_compile_args=['-O3']
    ),
]

setup(
    name="chess_engine_cpp",
    version="0.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="C++ extension for chess engine",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.6",
)