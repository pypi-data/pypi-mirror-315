from setuptools import setup


setup(
        name='pyjson2dataclass',
        author='yinpeach',
        description='Parse json to dataclass',
        keywords=[
            'dataclass',
            'json',
            'yinpeach',
            'verssionhack'
            ],
        py_modules=[
            '__init__',
            '__main__',
            'utils',
            'test_dataclass',
            ],
        package_data={
            'sample': [
                '__init__.py',
                '__main__.py',
                'utils.py',
                'test_dataclass.py',
                'json/example1.json',
                'README.md',
                ],
            },
        )
