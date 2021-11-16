import setuptools
# https://packaging.python.org/tutorials/packaging-projects/

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysea-colabimport", # Replace with your own username
    version="0.0.110",
    author="Eugene Komissarov",
    author_email="ekom@cian.ru",
    description="Colab functions base",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ekomissarov@bitbucket.org/ekomissarov/colabimport.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Linux",
    ],
    python_requires='>=3.6',
    install_requires=[
        'matplotlib',
        'numpy',
        'pandas',
        'Pillow',
        'pyparsing',
        'python-dateutil',
        'pytz',
        'six',
        'cycler',
        'kiwisolver'
    ]
)