# INNOSOFT-API

![](https://github.com/enriquebarba97/innosoft_api/workflows/Django%20Tests/badge.svg)
[![Build Status](https://travis-ci.com/enriquebarba97/innosoft_api.svg?branch=develop)](https://travis-ci.com/enriquebarba97/innosoft_api)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/bac4b8376e0b427ba8763fe6c6ee7d6c)](https://app.codacy.com/gh/enriquebarba97/innosoft_api?utm_source=github.com&utm_medium=referral&utm_content=enriquebarba97/innosoft_api&utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/eaf00d3bd6aa41348b643b4a422243de)](https://www.codacy.com/gh/enriquebarba97/innosoft_api/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=enriquebarba97/innosoft_api&amp;utm_campaign=Badge_Coverage)


## INTRODUCCIÓN

Innosoft-api es un proyecto para la gestión y automatización del programa de las jornadas Innosoft Days de la Universidad de Sevilla a través de una API REST. El proyecto utiliza el framework Django y PostgreSQL.

## AUTORES

- [Adrián García Barroso](https://github.com/adrgrabar)
- [Carlos Cote Medina](https://github.com/Carcotmed)
- [Miguel Ángel Pantoja Bas](https://github.com/miguelpantoja89)
- [Moisés Pantión Loza](https://github.com/Moipanloz)
- [Enrique Barba Roque](https://github.com/enriquebarba97)
 
## INSTALACIÓN
 
Tanto la instalación como el despliegue del proyecto en todas sus formas se define en profundidad en el apartado [Gestión del despliegue](https://github.com/enriquebarba97/innosoft_api/wiki/Documento-del-Proyecto/_edit) del documento del proyecto.

## TEST DE ESTRÉS CON LOCUST

Para la ejecución de los test de estrés con locust, es necesario instalarlo de la siguiente forma:

	pip install locust
	
En el directorio de loadtest se encuentra el fichero locustfile.py que contiene las configuración a ejecutar. En nuestro caso tenemos dos ejemplos:

1. Visualizer: entra en el visualizador de las ponencias y de los ponentes.

       locust Visualizer
       
Al ejecutar este comando se abrirá un servidor que podremos ver en el navegador, el mismo comando nos dirá el puerto. Cuando se abra, nos preguntará cuantos usuarios queremos que hagan peticiones a la vez, y como queremos que vaya creciendo hasta llegar a ese número. Por ejemplo, si ponemos 100 y 5, estaremos creando 5 nuevos usuarios cada segundo hasta llegar a 100.

2. ShowPonente: utilizaremos ponentes previamente creados, y haremos una secuencia de peticiones: authorization y getPonenteById. Esto es lo que realizaría un usuario administrador para consultar un Ponente. Para que este script funcione necesitaremos tener instalado requests:

       pip install requests
       
Una vez instalado ejecutamos el script de población gen_ponentes.py:
       
       python gen_ponentes.py
       
Ahora ya podemos proceder con el test de estrés:

       locust ShowPonente
      
