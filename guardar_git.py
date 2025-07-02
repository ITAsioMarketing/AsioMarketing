from pathlib import Path

contenido = """📄 guia-git.txt – Guía paso a paso para usar Git y GitHub

🛠️ CONFIGURACIÓN INICIAL (una sola vez por computadora)

1. git config --global user.name "Tu Nombre"
   → Configura tu nombre de usuario para los commits.

2. git config --global user.email "tuemail@ejemplo.com"
   → Configura tu correo para los commits.

🚀 SUBIR UN PROYECTO LOCAL A GITHUB (desde el trabajo)

3. cd ruta/a/tu/proyecto
   → Entra a la carpeta de tu proyecto.

4. git init
   → Inicializa Git en esa carpeta.

5. git config user.name "Tu Nombre"
   → Configura nombre local (opcional si ya hiciste los pasos 1–2).

6. git config user.email "tuemail@ejemplo.com"
   → Configura correo local (opcional).

7. git add .
   → Agrega todos los archivos al área de preparación.

8. git commit -m "Primer respaldo del proyecto"
   → Crea un commit con mensaje (-m es para "message").

9. git branch -M main
   → Renombra la rama principal a main. (-M forza el cambio si ya existe otra).

10. git remote add origin https://github.com/tuusuario/mi-proyecto-python.git
    → Enlaza tu repositorio local con GitHub.

11. git push -u origin main
    → Sube el contenido. (-u enlaza la rama local con la remota para futuros git push).

🏠 TRABAJAR DESDE CASA CON RAMAS

12. git clone https://github.com/tuusuario/mi-proyecto-python.git
    → Clona el proyecto en tu computadora.

13. cd mi-proyecto-python
    → Entra al directorio clonado.

14. git config user.name "Tu Nombre"
    → Configura tu nombre (si es otra máquina).

15. git config user.email "tuemail@ejemplo.com"
    → Configura tu correo (si es otra máquina).

16. git checkout -b nueva-funcionalidad
    → Crea y cambia a una nueva rama (-b = "branch").

17. (Haz cambios en los archivos)

18. git add .
    → Prepara los archivos modificados.

19. git commit -m "Descripción de los cambios"
    → Crea un commit.

20. git push origin nueva-funcionalidad
    → Sube la nueva rama a GitHub.

🔁 OPCIONAL: FUSIONAR LA RAMA A MAIN

21. git checkout main
    → Cambia a la rama principal.

22. git pull origin main
    → Asegúrate de tener la última versión de main.

23. git merge nueva-funcionalidad
    → Une los cambios de tu rama a main.

24. git push origin main
    → Sube la rama principal actualizada a GitHub.
"""

# Guardar el archivo
archivo = Path("guia-git.txt")
archivo.write_text(contenido, encoding="utf-8")
