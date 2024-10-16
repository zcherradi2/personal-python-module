from setuptools import setup


setup(
    name='PersonalModule',
    version='0.1.0',

    url='https://github.com/zcherradi2/personal-python-module',
    author='ziko',
    author_email='zcherradi2@gmail.com',

    py_modules=['PersonalModule'],
    # install_requires=[
    #     'requests','filelock',  # This will ensure requests is installed with your package
    # ],
    install_requires = [
        'requests','filelock',  # This will ensure requests is installed with your package
    ],
)