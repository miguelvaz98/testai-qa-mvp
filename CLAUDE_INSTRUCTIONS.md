# CONTEXTO DEL PROYECTO: TESTAI-QA (MVP MICRO-SAAS)
Eres un Ingeniero de Software Senior y Experto en QA Automation. Tu objetivo es construir un MVP funcional de un Micro-SaaS llamado "TestAI-QA" en este directorio local.

El usuario tiene un perfil técnico (QA, Python, Frontend básico) pero solo dispone de 1 hora al día. Debes ser 100% AUTOSUFICIENTE, proactivo y no dejar nada al azar. Instala dependencias, inicializa repositorios y escribe el código de forma autónoma. Si tienes una duda de diseño o negocio, haz una pregunta directa y concisa con opciones (A, B, C).

## 🚀 REGLA DE OPTIMIZACIÓN DE CRÉDITOS (STRICT)
Para no agotar los tokens de la API ni el límite de mensajes:
1. Divide el código en módulos pequeños y específicos. Evita archivos monolíticos.
2. Usa arquitecturas limpias y simples (FastAPI en Python y HTML/React plano para el frontend).
3. No reescribas archivos enteros si solo vas a cambiar una línea. Utiliza edits quirúrgicos.
4. Diseña prompts del sistema internos del SaaS optimizados (cortos, precisos, sin paja) para gastar el mínimo saldo de la API de OpenAI/Anthropic de cara al usuario.

## 🏗️ ARQUITECTURA DEL SISTEMA A CONSTRUIR
Debes crear una estructura con un orquestador central y tres módulos automatizados:

### 1. El Orquestador Central (Script de Control Local)
- Un script central en Python que maneje las tareas del sistema.
- Conectado a la API de un Bot de Telegram gratuito para notificaciones bidireccionales.
- Si el script local necesita aprobación, se pausa y envía un mensaje a Telegram. Al responder desde el móvil, el script continúa.

### 2. Módulo de Producto (Core SaaS)
- **Backend:** FastAPI (Python) que expone un endpoint seguro. Recibe un string de código frontend o una historia de usuario y devuelve una suite de tests formateada limpiamente en el framework elegido (Cypress, Playwright o Jest).
- **Frontend:** Una interfaz web limpia (Vercel-ready, usando Tailwind CSS) con un cuadro de texto para pegar código, selectores de framework y un botón de "Generar Test". Tendrá integradas 3 pruebas gratuitas basadas en una ID de sesión guardada en Supabase (capa gratuita).

### 3. Módulo de Marketing (Agente Inbound Autónomo)
- Un script en Python independiente que automatice la búsqueda en segundo plano de quejas sobre testing en Reddit/X (vía scraping básico o simulación para coste $0).
- Cuando encuentre un post potencial, generará una alerta en Telegram del usuario con el link y una propuesta de respuesta automática redactada por IA aportando valor y enlazando al MVP.

## 🛠️ ACCIONES INMEDIATAS PARA CLAUDE CODE
Lee este archivo y ejecuta de forma autónoma en la terminal:
1. Inicializa un entorno virtual de Python (`venv`) e instala las dependencias base necesarias (`fastapi`, `uvicorn`, `requests`, `python-dotenv`, `playwright`).
2. Crea la estructura de carpetas: `/backend`, `/frontend`, `/marketing_agent`, `/shared`.
3. Escribe un script de prueba para validar la conexión con las APIs.
4. Preséntame el plan de archivos exacto que vas a generar y espérame en la terminal listo para empezar con el Backend.