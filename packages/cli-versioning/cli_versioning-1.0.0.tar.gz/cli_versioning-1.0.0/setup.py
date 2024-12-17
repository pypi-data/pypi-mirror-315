from setuptools import setup

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='cli-versioning',
    version='1.0.0',
    license='MIT License',
    author='Jeferson Lopes',
    long_description=readme,
    long_description_content_type='text/markdown',
    author_email='jefersonlopes.sjn@gmail.com',
    keywords='control version system',
    description='Version control of your system',
    packages=['version_system'],
    entry_points={
        'console_scripts': [
            'vsg = version_system.__main__:main',
            ],
        },
    install_requires=[
        'colorama',
    ],
)
