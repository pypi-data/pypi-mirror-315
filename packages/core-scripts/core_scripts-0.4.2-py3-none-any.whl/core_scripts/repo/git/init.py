import os 
from core_commands import commands
def init(repo,opts):
    ruta_script = os.path.dirname(__file__)
    directorio_script = os.path.basename(ruta_script)
    gh = commands
    """
        crea el repositorio en github, y inicia el reopsitio con git, hace un commit y lo publica a github.
        * localizar el directorio donde se esta ejecutando el script, para determinar como se llama el repositorio y asi poder crearlo en github, esta es la manera por defecto de actuar, tambien se puede suministrar esa informacion por argumentos pero es opcional.
            # Obtener el directorio del script en ejecución
            directorio_script = os.path.dirname(__file__)
            print(directorio_script)
        * ejecutar un git init
        * crear el repositorio en github
        * crear la rama dev
        * hacer un commit
        * 
    """
    # Verifica que el repositorio no este vacio, ya que no podria hacer el primer commit.
    
    pass