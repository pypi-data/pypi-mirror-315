from setuptools import setup, find_packages

setup(
    name='humiris-ai',
    version='1.0.0',
    author='Hilario Houmey',
    author_email='h.hilario@humiris.ai',
    description='Humiris is a library that allows developers to easily integrate AI capabilities into their applications.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/joeai-tech-org/humiris-pip-package',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # list your package dependencies here
    ],
)