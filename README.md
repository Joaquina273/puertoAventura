# puertoAventura

Hola! este es el repositorio de nuestra pagina web puerto aventura, creada por León Felder, Nicolás Delgado, Ramiro Alvarez y Joaquina Saadi

Disclaimer: 
1) en lo posible cuando usen la consola utilicen pip3 (por las dudas porque es más nuevo y tiene otras funcionalidades)
2) preferentemente cuando se pongan a codear en sus ramas primero hagan un `git merge staging *tu rama*` para estar actualizado con los cambios
3) lo mismo cuando terminen de hacer sus actualizaciones usen `git merge *tu rama* staging` asi todos podemos ver los cambios realizados 


Cosas Joaquina
1) Para eliminar la base de datos se hace: `python manage.py migrate db zero` después `python manage.py makemigrations` y último `python manage.py migrate`
2) Para crear un usuario admin desde bash `winpty python manage.py createsuperuser`


##Instalación de paquetes:
Después de instalar un paquete (x ejemplo: `pip3 install paquetex`) hay que correr el comando `pip3 freeze > requirements.txt`

