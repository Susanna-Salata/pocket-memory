from distutils.core import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
import uvicorn


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        config = uvicorn.Config("app:app",
                                port=8000,
                                log_level="info",
                                reload=True,
                                host="0.0.0.0")
        server = uvicorn.Server(config)
        server.run()


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        config = uvicorn.Config("app:app",
                                port=8000,
                                log_level="info",
                                reload=True,
                                host="0.0.0.0")
        server = uvicorn.Server(config)
        server.run()


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
        cmdclass={
                'develop': PostDevelopCommand,
                'install': PostInstallCommand,
    }
     )



