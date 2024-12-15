from setuptools import setup, find_packages

setup(
    name='switchai',
    version='0.1.1',
    description='A unified library for interacting with various AI APIs through a standardized interface.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Yassine El Boudouri',
    author_email='boudouriyassine@gmail.com',
    url='https://github.com/yelboudouri/SwitchAI',
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.6',
)
