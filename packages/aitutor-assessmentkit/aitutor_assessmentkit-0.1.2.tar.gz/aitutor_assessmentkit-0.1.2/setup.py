from setuptools import setup, find_packages

setup(
    name='aitutor_assessmentkit',  # Package name
    version='0.1.2',  # Package version
    packages=find_packages(),  # Automatically discover and include packages in the directory
    install_requires=[  # List of dependencies required for the package
        "numpy",               # Numerical computations
        "torch",                # PyTorch for deep learning tasks
        "pandas",               # Data manipulation
        "tqdm",                # Progress bars
        "scipy",               # Scientific computing
        "nltk",                 # Natural language processing
        "transformers",        # Transformer models
        "scikit-learn",         # Machine learning library
        "matplotlib",           # Plotting and visualization
        "seaborn",             # Statistical data visualization
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