import setuptools

import chunjie


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
  name = "Spring_Festival",
  version = chunjie.__version__,
  description = chunjie.__doc__,
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = "qjzx",
  url = "https://github.com/QJZX/Spring_Festival",
  packages = setuptools.find_packages( exclude=["venv"])
)

