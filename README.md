# JobConnect — Sistema de Gestión de Reclutamiento

## Descripción General

JobConnect es una plataforma básica de intermediación laboral desarrollada completamente en Python.

El sistema permite conectar candidatos y empleadores mediante la publicación de vacantes y la gestión de postulaciones.

Este proyecto fue diseñado como un MVP (Producto Mínimo Viable) utilizando una arquitectura modular sencilla, enfocada en:

- Organización clara del código
- Separación de responsabilidades
- Persistencia local con JSON
- Facilidad de mantenimiento
- Desarrollo rápido en equipo

---

# Objetivo del Proyecto

El propósito principal de JobConnect es centralizar el flujo básico de reclutamiento:

1. Los empleadores publican vacantes.
2. Los candidatos buscan empleos.
3. Los candidatos aplican a vacantes.
4. Los empleadores revisan postulaciones.
5. El sistema almacena toda la información localmente.

---

# Funcionalidades del Sistema

## Módulo de Candidatos

Los candidatos pueden:

- Crear perfil profesional
- Consultar vacantes disponibles
- Aplicar a empleos
- Ver el estado de sus postulaciones

---

## Módulo de Empleadores

Los empleadores pueden:

- Registrar su empresa
- Publicar vacantes
- Ver candidatos postulados
- Cerrar vacantes

---

# Reglas de Negocio

El sistema implementa las siguientes reglas:

## 1. Un candidato no puede aplicar dos veces a la misma vacante

Esto evita duplicidad de postulaciones.

---

## 2. Solo el creador de una vacante puede modificarla o cerrarla

Se garantiza integridad y control de autoría.

---

## 3. Todos los cambios se guardan automáticamente

La información se persiste en archivos JSON después de cada operación importante.

---

# Arquitectura del Proyecto

El sistema utiliza una arquitectura modular simple para facilitar el desarrollo rápido y el trabajo colaborativo.

## Estructura General

```plaintext
jobconnect/
│
├── main.py
├── requirements.txt
├── README.md
│
├── models/
├── services/
├── storage/
├── menus/
└── utils/