<div align="center">

# 🚀 TaskFlow

**Gestión inteligente de proyectos y tareas**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![CI](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![License](https://img.shields.io/badge/Licencia-MIT-yellow?style=for-the-badge)](LICENSE)

TaskFlow es una API REST diseñada para que equipos de trabajo puedan organizar proyectos, asignar tareas, visualizar el progreso en un tablero Kanban y generar reportes de desempeño — todo desde un único backend moderno, rápido y escalable.

[Explorar docs »](#-documentación-interactiva) · [Endpoints »](#-endpoints-principales) · [Instalación »](#-instalación)

</div>

---

## 📑 Tabla de contenido

- [Sobre el proyecto](#-sobre-el-proyecto)
- [Funcionalidades](#-funcionalidades)
- [Arquitectura](#-arquitectura)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Variables de entorno](#-variables-de-entorno)
- [Endpoints principales](#-endpoints-principales)
- [Documentación interactiva](#-documentación-interactiva)
- [Docker](#-docker)
- [Testing](#-testing)
- [CI/CD](#-cicd)
- [Buenas prácticas](#-buenas-prácticas)
- [Estado del proyecto](#-estado-del-proyecto)
- [Autores](#-autores)
- [Licencia](#-licencia)

---

## 💡 Sobre el proyecto

### El problema

Coordinar equipos de trabajo sin una herramienta centralizada genera tareas duplicadas, falta de visibilidad sobre el progreso y dificultad para medir el desempeño real de cada integrante.

### La solución

**TaskFlow** ofrece una API que permite a cualquier equipo — desde startups hasta proyectos académicos — gestionar su trabajo de forma organizada:

- Cada proyecto tiene su propio espacio con miembros y tareas.
- Las tareas se asignan, priorizan y avanzan por estados (Kanban).
- Los líderes pueden ver reportes de desempeño en tiempo real.
- Toda acción queda registrada en un historial auditable.

### ¿Para quién es?

| Perfil | Uso |
|---|---|
| **Equipos de desarrollo** | Organizar sprints y tareas técnicas |
| **Gestores de proyecto** | Supervisar avance y generar reportes |
| **Estudiantes** | Coordinar trabajos grupales |
| **Startups** | Base para construir su propio gestor de tareas |

---

## ✨ Funcionalidades

| Característica | Descripción |
|---|---|
| 🔐 **Autenticación JWT** | Registro, login y protección de endpoints con tokens |
| 👥 **Gestión de usuarios** | Crear, editar, activar/desactivar y asignar roles |
| 📁 **Gestión de proyectos** | Crear proyectos, agregar miembros y definir propietarios |
| ✅ **Gestión de tareas** | Crear, asignar, priorizar y actualizar estado de tareas |
| 📊 **Tablero Kanban** | Vista por columnas (Pendiente, En progreso, Completada, Bloqueada) |
| 📈 **Reportes** | Desempeño por usuario, estado de tareas y resumen por proyecto |
| 📜 **Historial** | Registro automático de todas las acciones del sistema |
| 🔔 **Notificaciones** | Enviar avisos a usuarios específicos |
| 🐳 **Docker** | Despliegue con un solo comando |
| ⚙️ **CI/CD** | Pruebas automáticas con GitHub Actions |

---

## 🏗 Arquitectura

TaskFlow sigue una **arquitectura hexagonal** organizada por módulos de dominio. Cada módulo encapsula su propia lógica de negocio, datos y rutas, lo que permite escalar y mantener el proyecto de forma independiente.

### Principios clave

- **Feature-based:** Cada funcionalidad vive en su propio módulo.
- **Use Cases:** La lógica de negocio está aislada en casos de uso reutilizables.
- **Inyección de dependencias:** Los repositorios se inyectan vía FastAPI `Depends()`.
- **Separación de capas:** Entidades → Repositorios → Casos de uso → Servicios → Rutas.

### Estructura del proyecto

```
src/
├── main.py                       # Punto de entrada de la API
│
├── modules/
│   ├── auth/                     # 🔐 Autenticación
│   │   ├── routes/               #    Endpoints de login y registro
│   │   ├── schemas/              #    Validación de datos
│   │   ├── security/             #    Manejo de tokens
│   │   ├── services/             #    Orquestación
│   │   └── use_cases/            #    Lógica de negocio
│   │
│   ├── users/                    # 👥 Usuarios
│   ├── projects/                 # 📁 Proyectos
│   ├── tasks/                    # ✅ Tareas
│   ├── reports/                  # 📈 Reportes
│   ├── history/                  # 📜 Historial
│   ├── kanban/                   # 📊 Tablero Kanban
│   └── notifications/            # 🔔 Notificaciones
│
└── shared/
    ├── base/                     # Clases base (Repository, Service, Schemas)
    ├── config/                   # Configuración y variables de entorno
    ├── database/                 # Conexión y sesiones de BD
    ├── security/                 # JWT y hashing de contraseñas
    ├── exceptions/               # Excepciones de dominio y handlers
    ├── middleware/                # Inyección de dependencias y auth
    └── utils/                    # Mappers y utilidades
```

Cada módulo sigue la misma estructura interna: `entities/` → `repositories/` → `use_cases/` → `services/` → `routes/` → `schemas/`.

---

## 🛠 Tecnologías

| Categoría | Tecnología | Propósito |
|---|---|---|
| **Backend** | FastAPI | Framework web async de alto rendimiento |
| **Lenguaje** | Python 3.11+ | Tipado estático, async/await nativo |
| **Base de datos** | PostgreSQL | Base de datos relacional robusta |
| **ORM** | SQLAlchemy 2.0 (async) | Mapeo objeto-relacional con soporte async |
| **Autenticación** | python-jose + passlib | JWT tokens y hashing bcrypt |
| **Validación** | Pydantic v2 | Validación y serialización de datos |
| **Testing** | Pytest + pytest-asyncio | Pruebas unitarias asíncronas |
| **HTTP Client** | HTTPX | Cliente async para testing |
| **Contenedores** | Docker + Docker Compose | Despliegue reproducible |
| **CI/CD** | GitHub Actions | Integración continua automática |

---

## 📦 Instalación

### Requisitos previos

- Python 3.11 o superior
- PostgreSQL (o Docker para levantarlo automáticamente)
- Git

### Paso a paso

**1. Clonar el repositorio**

```bash
git clone https://github.com/tu-usuario/TaskFlow.git
cd TaskFlow
```

**2. Crear y activar el entorno virtual**

```bash
python -m venv venv
```

```bash
# Windows
venv\Scripts\Activate

# macOS / Linux
source venv/bin/activate
```

**3. Instalar dependencias**

```bash
pip install -r requirements.txt
```

**4. Configurar variables de entorno**

```bash
cp .env.example .env
```

Edita el archivo `.env` con los datos de tu base de datos (ver sección siguiente).

**5. Ejecutar la API**

```bash
uvicorn src.main:app --reload
```

La API estará disponible en **http://localhost:8000** 🎉

---

## 🔑 Variables de entorno

Crea un archivo `.env` en la raíz del proyecto basándote en `.env.example`:

| Variable | Descripción | Ejemplo |
|---|---|---|
| `APP_NAME` | Nombre de la aplicación | `TaskFlow API` |
| `APP_VERSION` | Versión actual | `1.0.0` |
| `SECRET_KEY` | Clave secreta para firmar tokens JWT | `mi_clave_super_secreta_123` |
| `ALGORITHM` | Algoritmo de encriptación JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Duración del token en minutos | `30` |
| `DB_SERVER` | Host del servidor de base de datos | `localhost` |
| `DB_NAME` | Nombre de la base de datos | `TaskFlow` |
| `DB_DRIVER` | Driver de conexión | `ODBC Driver 17 for SQL Server` |
| `DB_TRUSTED_CONNECTION` | Usar autenticación de Windows | `true` |
| `DB_USER` | Usuario de BD (si no usa Windows Auth) | `sa` |
| `DB_PASSWORD` | Contraseña de BD | `tu_password` |

> ⚠️ **Nunca subas el archivo `.env` al repositorio.** Ya está incluido en `.gitignore`.

---

## 🌐 Endpoints principales

### Autenticación

| Método | Endpoint | Descripción |
|---|---|---|
| `POST` | `/api/auth/register` | Registrar un nuevo usuario |
| `POST` | `/api/auth/login` | Iniciar sesión y obtener token |
| `GET` | `/api/auth/me` | Obtener perfil del usuario autenticado |

### Usuarios

| Método | Endpoint | Descripción |
|---|---|---|
| `POST` | `/api/users` | Crear usuario (admin) |
| `GET` | `/api/users` | Listar todos los usuarios |
| `GET` | `/api/users/{id}` | Obtener usuario por ID |
| `PUT` | `/api/users/{id}` | Actualizar usuario |
| `DELETE` | `/api/users/{id}` | Eliminar usuario |
| `PATCH` | `/api/users/{id}/role` | Cambiar rol de usuario |
| `PATCH` | `/api/users/{id}/status` | Activar/desactivar usuario |

### Proyectos

| Método | Endpoint | Descripción |
|---|---|---|
| `POST` | `/api/projects` | Crear proyecto |
| `GET` | `/api/projects` | Listar proyectos |
| `GET` | `/api/projects/{id}` | Obtener proyecto por ID |
| `PUT` | `/api/projects/{id}` | Actualizar proyecto |
| `DELETE` | `/api/projects/{id}` | Eliminar proyecto |
| `GET` | `/api/projects/{id}/members` | Listar miembros del proyecto |
| `POST` | `/api/projects/{id}/members` | Agregar miembro al proyecto |

### Tareas

| Método | Endpoint | Descripción |
|---|---|---|
| `POST` | `/api/tasks` | Crear tarea |
| `GET` | `/api/tasks` | Listar tareas |
| `GET` | `/api/tasks/{id}` | Obtener tarea por ID |
| `PUT` | `/api/tasks/{id}` | Actualizar tarea |
| `DELETE` | `/api/tasks/{id}` | Eliminar tarea |
| `PATCH` | `/api/tasks/{id}/status` | Cambiar estado de tarea |
| `PATCH` | `/api/tasks/{id}/assign` | Asignar tarea a usuario |

### Otros módulos

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/kanban/{project_id}` | Tablero Kanban del proyecto |
| `GET` | `/api/reports/performance` | Reporte de desempeño |
| `GET` | `/api/reports/projects` | Reporte de proyectos |
| `GET` | `/api/reports/tasks` | Reporte de tareas por estado |
| `GET` | `/api/reports/users` | Reporte de usuarios |
| `GET` | `/api/history` | Historial de actividades |
| `GET` | `/api/history/{user_id}` | Historial por usuario |
| `GET` | `/api/notifications` | Notificaciones del usuario |
| `POST` | `/api/notifications` | Crear notificación |
| `GET` | `/health` | Estado del servicio |

---

## 📖 Documentación interactiva

FastAPI genera documentación automática e interactiva. Una vez que la API esté corriendo:

| Herramienta | URL | Descripción |
|---|---|---|
| **Swagger UI** | http://localhost:8000/docs | Interfaz visual para probar endpoints |
| **ReDoc** | http://localhost:8000/redoc | Documentación en formato legible |
| **Health Check** | http://localhost:8000/health | Verificar que la API esté activa |

Desde Swagger puedes autenticarte con tu token JWT y probar todos los endpoints directamente desde el navegador.

---

## 🐳 Docker

Levanta todo el proyecto con un solo comando — sin instalar nada localmente:

```bash
docker compose up --build
```

Esto crea automáticamente:

- **SQL Server 2022** como base de datos
- **TaskFlow API** conectada y lista para usar

Para detener los servicios:

```bash
docker compose down
```

---

## 🧪 Testing

El proyecto incluye **135 pruebas unitarias** que cubren todos los módulos y casos de uso.

### Ejecutar las pruebas

```bash
python -m pytest tests/ --ignore=tests/test_health.py -v
```

### Estructura de pruebas

```
tests/
├── conftest.py                       # Fixtures y mocks compartidos
├── test_shared/                      # JWT, passwords, excepciones
├── test_auth/                        # Login y registro
├── test_users/                       # CRUD de usuarios
├── test_projects/                    # CRUD de proyectos y miembros
├── test_tasks/                       # CRUD, permisos y transiciones de estado
├── test_history/                     # Historial de actividades
├── test_kanban/                      # Tablero Kanban
├── test_notifications/               # Notificaciones
└── test_reports/                     # Reportes y estadísticas
```

### Cobertura por módulo

| Módulo | Tests | Qué se prueba |
|---|---|---|
| Shared | 12 | JWT, hashing, excepciones de dominio |
| Auth | 8 | Login, registro, validaciones |
| Users | 17 | CRUD completo, roles, permisos |
| Projects | 14 | CRUD, miembros, permisos por rol |
| Tasks | 25 | CRUD, asignación, transiciones de estado |
| History | 5 | Registro y consulta de historial |
| Kanban | 3 | Tablero con columnas por estado |
| Notifications | 6 | Crear y listar notificaciones |
| Reports | 5 | 4 tipos de reportes |

---

## ⚙️ CI/CD

El proyecto usa **GitHub Actions** para ejecutar las pruebas automáticamente en cada push o pull request.

El pipeline (`.github/workflows/ci.yml`) realiza:

1. Configura Python 3.12
2. Instala las dependencias
3. Verifica que la app importe correctamente
4. Ejecuta todas las pruebas con pytest

---

## 🧹 Buenas prácticas

Este proyecto fue desarrollado siguiendo estándares profesionales de ingeniería de software:

| Práctica | Implementación |
|---|---|
| **Clean Code** | Nombres descriptivos, funciones pequeñas, sin código muerto |
| **SOLID** | Responsabilidad única en cada use case y repositorio |
| **Async/Await** | Operaciones de BD completamente asíncronas |
| **Tipado estático** | Type hints en todo el código con Python 3.11+ |
| **Separación de capas** | Entities → Repos → Use Cases → Services → Routes |
| **Inyección de dependencias** | Vía FastAPI `Depends()` — sin acoplamiento directo |
| **Manejo de errores** | Excepciones de dominio mapeadas a HTTP status codes |
| **Auditoría** | Historial automático de todas las acciones |

---

## 📍 Estado del proyecto

🟢 **En desarrollo activo**

### Implementado

- [x] Autenticación JWT (login / registro)
- [x] CRUD completo de usuarios, proyectos y tareas
- [x] Sistema de roles y permisos (Admin, Líder, Usuario)
- [x] Tablero Kanban con transiciones de estado validadas
- [x] Reportes de desempeño, proyectos y tareas
- [x] Historial de actividades auditable
- [x] Notificaciones
- [x] Docker y Docker Compose
- [x] CI/CD con GitHub Actions
- [x] 135 pruebas unitarias

### Roadmap

- [ ] Refresh tokens y cierre de sesión
- [ ] Paginación avanzada con cursores
- [ ] Filtros y búsqueda en endpoints
- [ ] Websockets para notificaciones en tiempo real
- [ ] Dashboard frontend (React / Next.js)
- [ ] Despliegue en la nube (AWS / Azure)
- [ ] Documentación con ejemplos de request/response

---

## 👥 Autores

| Nombre | Rol |
|---|---|
| **Joan Sebastián Sosa Bedoya** | Desarrollo backend |
| **Alejandra Mejía Patiño** | Desarrollo backend |

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

<div align="center">

Hecho con ❤️ por el equipo TaskFlow

</div>
