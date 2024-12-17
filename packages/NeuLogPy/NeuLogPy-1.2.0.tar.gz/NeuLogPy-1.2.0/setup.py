from setuptools import setup, find_packages

with open('README.md','r', encoding='utf-8') as f:
    description = f.read()
    
setup(
    name='NeuLogPy',
    version='1.2.0',  # Bumped version for import fixes
    packages=find_packages(),
    install_requires=[
        'pydantic>=2.0.0',
        'requests>=2.25.0',
        'pyyaml>=5.4.0',
    ],
    author='Sustronics',
    author_email='info@sustronics.com',
    description='Python interface for NeuLog sensors',
    long_description=description,
    long_description_content_type="text/markdown",
    url='https://github.com/sustronics/neulogpy',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7',
)