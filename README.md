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
 
Para instalar nuestra aplicación, en primer lugar se deberá clonar el proyecto en la ubicación deseada, tras esto, se instalarán los requisitos de este de la siguiente manera:

	pip install -r requirements.txt

Una vez instalados los requisitos se deberá ejecutar el archivo de setup con el siguiente comando:

	python .\manage.py setup

Tras realizar las pasos anteriores el proyecto ya estará listo para funcionar, a continuación se deberá usar el siguiente comando para que la aplicación sea accesible desde "localhost:8000":

	python .\manage.py runserver

## EJECUCIÓN CON DOCKER

Ejecucion con docker

## TEST DE ESTRÉS CON LOCUST

Test de estrés con locust
