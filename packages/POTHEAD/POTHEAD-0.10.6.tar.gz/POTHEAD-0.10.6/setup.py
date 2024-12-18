import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

common_deps = ["psutil", "werkzeug>=2.1", "tblib", "setproctitle", "prometheus_client"]
test_deps = [*common_deps, "aiohttp", "timeout-decorator"]

setuptools.setup(
    name="POTHEAD",
    version="0.10.6",
    author="Ulrik Mikaelsson",
    author_email="ulrik.mikaelsson@gmail.com",
    description="A reverse-http proxy implementation for non-concurrent requests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/rawler/pothead",
    packages=setuptools.find_packages(),
    install_requires=[*common_deps],
    tests_require=test_deps,
    extras_require={
        "test": test_deps,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
