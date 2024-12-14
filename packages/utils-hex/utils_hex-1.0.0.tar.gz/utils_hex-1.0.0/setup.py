from setuptools import setup
from setuptools.command.install import install
import os

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        script_path = os.path.join(os.path.dirname(__file__), 'post_install.py')
        if os.path.exists(script_path):
            print(f"[*] Exécution du script post-installation : {r"post_install.py"}")
            exec(open(script_path).read())
        else:
            print("[!] Le script post-installation n'a pas été trouvé.")

setup(
    name='utils_hex',
    version='1.0.0',
    description='Un exemple de package pour installer les hexs .',
    author='Harmless',
    cmdclass={
        'install': CustomInstallCommand,  
    },
)
