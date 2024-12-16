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
        data_files=[
            ('json', ['json/example1.json']),
            ],
        version='1.1',
        )
