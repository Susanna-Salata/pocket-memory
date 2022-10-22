from distutils.core import setup

setup(name='Pocket Memory',
      version='1.0',
      description='Personal Assistant',
      author='Vadym Kuzik, Vladyslav Shumkov, Serhii Plys, Susanna Salata',
      author_email='email@python.net',
      packages=[
                ],
      entry_points={
          'console_scripts': [
              'pocket-memory = pocket-memory.app:app',
        ],
      },
     )
