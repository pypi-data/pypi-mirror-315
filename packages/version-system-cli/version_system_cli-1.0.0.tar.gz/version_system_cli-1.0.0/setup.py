from setuptools import setup

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='version-system-cli',
    version='1.0.0',
    license='MIT License',
    author='Jeferson Lopes',
    long_description=readme,
    long_description_content_type='text/markdown',
    author_email='jefersonlopes.sjn@gmail.com',
    keywords='control version system',
    description='Version control of your system',
    packages=['version_system'],
    py_modules=['version_system'],
    entry_points={
        'console_scripts': [
            'version-system=version_system:main',
            ],
        },
    install_requires=[
        'colorama',
    ],
)
