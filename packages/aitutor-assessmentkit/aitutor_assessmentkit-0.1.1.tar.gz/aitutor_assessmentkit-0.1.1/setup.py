from setuptools import setup, find_packages

setup(
    name='aitutor_assessmentkit',  # Package name
    version='0.1.1',  # Package version
    packages=find_packages(),  # Automatically discover and include packages in the directory
    install_requires=[  # List of dependencies required for the package
        "numpy==1.24.0",               # Numerical computations
        "torch==2.1.0",                # PyTorch for deep learning tasks
        "pandas==2.1.0",               # Data manipulation
        "tqdm==4.65.0",                # Progress bars
        "scipy==1.11.0",               # Scientific computing
        "nltk==3.8.0",                 # Natural language processing
        "transformers==4.35.2",        # Transformer models
        "clean-text==0.6.0",           # Text cleaning utilities
        "openpyxl==3.1.2",             # Excel file handling
        "spacy==3.6.1",                # NLP library
        "gensim==4.3.2",               # Topic modeling and document similarity
        "num2words==0.5.10",           # Converts numbers to words
        "scikit-learn==1.2.2",         # Machine learning library
        "matplotlib==3.7.1",           # Plotting and visualization
        "seaborn==0.12.2",             # Statistical data visualization
    ],
    long_description=open('README.md').read(),  # Long description from README.md
    long_description_content_type='text/markdown',  # Content type for long description
    author='Kaushal Kumar Maurya',  # Author name
    author_email='Kaushal.Maurya@mbzuai.ac.ae',  # Author email
    description=(
        'Welcome to the `AITutor-AssessmentKit`! With the remarkable advancements in large '
        'language models (LLMs), there is growing interest in leveraging these models as AI-powered tutors. '
        'However, the field lacks robust evaluation methodologies and tools to systematically assess the '
        'pedagogical capabilities of such systems. The `AITutor-AssessmentKit` is the first open-source toolkit '
        'specifically designed to evaluate the pedagogical performance of AI tutors in *Student Mistake Remediation* tasks.'
    ),  # Brief description of the package
    url='https://github.com/kaushal0494/aitutor-assessmentkit',  # URL to the package repository
    classifiers=[  # PyPI classifiers to categorize the package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',
    ],
)