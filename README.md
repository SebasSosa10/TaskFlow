*# 🚀 TaskFlow API*



*TaskFlow es una API REST desarrollada con \*\*FastAPI\*\* para la gestión de proyectos y tareas en equipos de trabajo.*  

*La plataforma permite administrar usuarios, proyectos, tareas, seguimiento de actividades, tablero Kanban y reportes de desempeño, implementando arquitectura hexagonal, autenticación JWT y prácticas DevOps.*



*---*



*# 📌 Características*



*- 🔐 Autenticación con JWT*

*- 👥 Gestión de usuarios y roles*

*- 📁 Gestión de proyectos*

*- ✅ Gestión y seguimiento de tareas*

*- 📊 Reportes de desempeño*

*- 📋 Tablero Kanban*

*- 🕓 Historial de actividades*

*- 🐳 Contenerización con Docker*

*- 🧪 Pruebas automatizadas con Pytest*

*- ⚙️ Pipeline CI/CD con GitHub Actions*

*- 🏗️ Arquitectura Hexagonal*



*---*



*# 🛠️ Tecnologías Utilizadas*



*| Tecnología | Uso |*

*|------------|-----|*

*| Python 3.11 | Lenguaje backend |*

*| FastAPI | Framework API REST |*

*| MySQL | Base de datos |*

*| SQLAlchemy | ORM |*

*| Pydantic | Validaciones |*

*| JWT | Autenticación |*

*| Pytest | Pruebas unitarias |*

*| Docker | Contenerización |*

*| GitHub Actions | CI/CD |*



*---*



*# 📂 Estructura del Proyecto*



*```bash*

*TaskFlow/*

*│*

*├── src/*

*│   ├── domain/*

*│   ├── application/*

*│   ├── infrastructure/*

*│   ├── api/*

*│   └── main.py*

*│*

*├── tests/*

*│   └── unit/*

*│*

*├── .github/*

*│   └── workflows/*

*│*

*├── Dockerfile*

*├── docker-compose.yml*

*├── requirements.txt*

*├── pytest.ini*

*└── README.md*

*```*



*---*



*# ⚙️ Instalación*



*## 1. Clonar el repositorio*



*```bash*

*git clone https://github.com/SebasSosa10/TaskFlow.git*

*```*



*---*



*## 2. Entrar al proyecto*



*```bash*

*cd TaskFlow*

*```*



*---*



*## 3. Crear entorno virtual*



*```bash*

*python -m venv venv*

*```*



*### Activar entorno virtual*



*#### Windows*



*```bash*

*venv\\Scripts\\activate*

*```*



*#### Linux/Mac*



*```bash*

*source venv/bin/activate*

*```*



*---*



*## 4. Instalar dependencias*



*```bash*

*pip install -r requirements.txt*

*```*



*---*



*# ▶️ Ejecutar el proyecto*



*```bash*

*uvicorn src.main:app --reload*

*```*



*Servidor disponible en:*



*```text*

*http://127.0.0.1:8000*

*```*



*---*



*# 📘 Documentación Swagger*



*FastAPI genera documentación automática:*



*- Swagger UI*



*```text*

*http://127.0.0.1:8000/docs*

*```*



*- ReDoc*



*```text*

*http://127.0.0.1:8000/redoc*

*```*



*---*



*# 🧪 Ejecutar pruebas*



*```bash*

*pytest tests/unit/ -v*

*```*



*Con cobertura:*



*```bash*

*pytest --cov=src --cov-report=term-missing*

*```*



*---*



*# 🐳 Docker*



*## Construir contenedores*



*```bash*

*docker compose build*

*```*



*## Levantar servicios*



*```bash*

*docker compose up -d*

*```*



*---*



*# 🔑 Variables de Entorno*



*Crear archivo `.env`:*



*```env*

*DATABASE\_URL=mysql+pymysql://root:password@localhost/taskflow*

*SECRET\_KEY=your\_secret\_key*

*ALGORITHM=HS256*

*ACCESS\_TOKEN\_EXPIRE\_MINUTES=30*

*```*



*---*



*# 📌 Roles del Sistema*



*- Administrador*

*- Líder de Proyecto*

*- Usuario*



*---*



*# 📋 Estados de las tareas*



*- Pendiente*

*- En progreso*

*- Completada*

*- Bloqueada*



*---*



*# 👨‍💻 Autores*



*- Joan Sebastián Sosa Bedoya*

*- Alejandra Mejía Patiño*



*Institución Universitaria EAM*  

*Ingeniería de Software III – 2026*



*---*



*# 📄 Licencia*



*Proyecto académico desarrollado con fines educativos.*

