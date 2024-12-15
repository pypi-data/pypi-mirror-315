import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sentence_concreteness",
    version="0.0.1",
    author="Marianne Aubin Le Quere",
    license="MIT", 
    author_email="msa258@cornell.edu",
    description="A function to tag sentences with a validated measure of sentence concreteness",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maubinle/sentence_concreteness.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['truecase','string', "typing_extensions==4.4.0", 'inflect', 'nltk', "numpy==1.21.0", "spacy==3.2.0"],
    extras_require={
        'spacy_models': ['en_core_web_sm']
    }
)