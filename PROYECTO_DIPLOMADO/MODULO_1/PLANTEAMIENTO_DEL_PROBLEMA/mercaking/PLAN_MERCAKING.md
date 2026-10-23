# 🧭 PLAN MAESTRO — MercaKing
## Plataforma SaaS Multi-inquilino con Inteligencia Artificial Local para Minimercados

> **Estado de implementación:** Fase PLAN ✅ · Build MVP ✅ · Fase 3 (IA local) ✅ · Superadmin ✅ · Tests ✅
> **Stack elegido:** Python (FastAPI backend + Flask/Jinja2 frontend) + MySQL (phpMyAdmin)
> **Decisiones confirmadas:** BD = MySQL (phpMyAdmin) · Branding = MercaKing · Frontend = Python puro · Git = sí
> **Proyecto destino:** `C:\Users\melis\OneDrive\Desktop\PROYECTO_DIPLOMADO\mercaking`
> **Fuente de especificación:** `C:\Users\melis\Downloads\Plataforma_Minimercados_IA_Local (2).docx`
> **Análisis de plan:** `C:\Users\melis\OneDrive\Desktop\PROYECTO_DIPLOMADO\estr`
> **Prototipo de referencia:** `C:\Users\melis\OneDrive\Desktop\PROYECTO_DIPLOMADO\minimarket`
> **Fecha:** 2026-10-22

---

## 1. Propósito de este documento

Convertir la **especificación del documento** en un **plan ejecutable y fácil de entender**, antes de pasar a la fase de desarrollo (`build`).

Este plan responde a:
1. Qué problema resuelve y para quién.
2. Qué alcance tiene (incluye / excluye).
3. Qué requisitos definen el MVP (RF) y sus criterios.
4. Qué decisiones técnicas se tomaron en el plan original (Qwen, OpenCode Plan + Build).
5. **Cómo se ve la estructura final de carpetas** (simple y entendible, en Python).
6. Qué tareas componen el roadmap, con su DoD (Definition of Done).

---

## 2. Fuentes de verdad del proyecto

| # | Fuente | Ruta | Tipo |
|---|---|---|---|
| 1 | Documento de especificación | `C:\Users\melis\Downloads\Plataforma_Minimercados_IA_Local (2).docx` | Docx (Word) |
| 2 | Plan maestro Qwen | `C:\Users\melis\OneDrive\Desktop\PROYECTO_DIPLOMADO\estr\Qwen_markdown_20261022_1a3v49dz5.md` | Markdown |
| 3 | Tarea RF-14 (ejemplo) | `C:\Users\melis\OneDrive\Desktop\PROYECTO_DIPLOMADO\estr\Qwen_text_20261022_14h861gxn.txt` | Texto |
| 4 | Prototipo Next.js | `C:\Users\melis\OneDrive\Desktop\PROYECTO_DIPLOMADO\minimarket` | Código |
| 5 | Esquema BD original (PostgreSQL) | `C:\Users\melis\OneDrive\Desktop\PROYECTO_DIPLOMADO\supabase_schema.sql` | SQL |

---

## 3. Resumen del producto (del documento)

**MercaKing** es una plataforma **SaaS multi-inquilino** que permite a los minimercados colombianos digitalizar la gestión integral de **inventarios, ventas y proveedores**, con un modelo de **suscripción predecible**, garantizando el **aislamiento absoluto de datos por tenant** y ofreciendo **IA generativa local** como valor diferencial.

**Roles:** `platform_admin` (superadmin MercaKing), `store_owner` (propietario), `store_admin`, `cashier` (cajero), `inventory_manager` (encargado de bodega).

---

## 4. Planteamiento del problema (del documento)

Los minimercados de barrio operan con herramientas fragmentadas (cuadernos, hojas de cálculo, POS genéricos), lo que les impide controlar inventario, conocer rentabilidad y tomar decisiones basadas en datos. Las soluciones empresariales son costosas, complejas y obligan a enviar datos sensibles a la nube de terceros. La IA generativa queda fuera del alcance del pequeño comerciante.

**Formulación:** ¿Cómo diseñar y desarrollar MercaKing, una plataforma web SaaS multi-inquilino asistida por IA generativa local, que permita a los minimercados digitalizar inventarios, ventas y proveedores mediante suscripción predecible, garantizando aislamiento lógico absoluto de datos y onboarding automatizado?

---

## 5. Alcance

### 5.1 Alcance incluido (12 componentes)
1. Landing pública (info, planes, casos de uso, CTA).
2. Portal de suscripción (selección de plan, pasarela de pago, generación de credenciales).
3. Autenticación multi-inquilino (login por tenant, recuperación, sesiones).
4. Panel del administrador del minimercado (CRUD productos, categorías, proveedores, usuarios, config).
5. Módulo de inventario (entradas, salidas, ajustes, stock mínimo, alertas).
6. Módulo de ventas (POS ligero) (carrito, descuento de stock, recibos).
7. Reportes operativos (consolidados diarios/semanales/mensuales, top productos, alertas).
8. Asistente de IA generativa (consultas en lenguaje natural sobre stock/productos/proveedores vía RAG segregado).
9. Componente multimodal (carga de imágenes → OCR → sugerencia de nombre/categoría).
10. Panel del Superadmin MercaKing (suscriptores, planes, métricas, logs).
11. Aislamiento lógico (RLS) en BD.
12. Auditoría y trazabilidad (acciones críticas e interacciones IA).

### 5.2 Alcance NO incluido
- Facturación electrónica ante la DIAN.
- Integración con hardware POS físico.
- Apps móviles nativas.
- Predicciones financieras / ML predictivo.
- Compras automáticas a proveedores.
- Nómina o contabilidad fiscal.
- Marketplace entre minimercados.

---

## 6. Requerimientos funcionales (RF-01 … RF-20)

| ID | Nombre | Descripción | Prioridad | Rol |
|---|---|---|---|---|
| RF-01 | Landing pública | Página con info, planes y beneficios. | Alta | Visitante |
| RF-02 | Selección de plan | Elegir entre Básico/Pro/Empresarial. | Alta | Visitante |
| RF-03 | Pasarela de pago | PSE / tarjeta / Nequi. | Alta | Visitante |
| RF-04 | Activación automática de tenant | Tras pago exitoso, crear tenant y credenciales. | Alta | Sistema |
| RF-05 | Onboarding guiado | Configurar nombre, NIT, logo, primer producto. | Media | Admin |
| RF-06 | Autenticación multi-inquilino | Login vincula sesión al tenant_id. | Alta | Todos |
| RF-07 | Gestión de productos | CRUD con código, nombre, precio, categoría, imagen. | Alta | Admin/Inv |
| RF-08 | Gestión de proveedores | CRUD con datos de contacto. | Media | Admin/Inv |
| RF-09 | Gestión de usuarios internos | Crear cajeros/encargados con roles. | Alta | Admin |
| RF-10 | Registro de ventas (POS) | Carrito, descuento de stock, recibo. | Alta | Cajero |
| RF-11 | Control de inventario | Entradas, salidas, ajustes auditados. | Alta | Inventario |
| RF-12 | Alertas de stock | Aviso cuando cae bajo el mínimo. | Alta | Inventario |
| RF-13 | Reportes de ventas | Consolidados diarios/semanales/mensuales. | Alta | Admin |
| RF-14 | Asistente IA (RAG) | Consultas en lenguaje natural sobre stock/productos/proveedores. | Alta | Todos |
| RF-15 | Componente multimodal (OCR) | Imagen → texto → sugerencia de nombre/categoría. | Media | Admin/Inv |
| RF-16 | Panel Superadmin | Gestión de suscriptores, planes, uso IA, logs. | Alta | Superadmin |
| RF-17 | Gestión de suscripciones | Renovación, cancelación, cambio de plan. | Alta | Admin |
| RF-18 | Notificaciones por correo | Bienvenida, pago, alertas críticas. | Media | Sistema |
| RF-19 | Aislamiento CRUD (RLS) | Toda operación filtra por tenant_id a nivel BD. | Alta | Sistema |
| RF-20 | Auditoría e interacciones IA | Registro de prompts, respuestas, acciones críticas. | Alta | Sistema |

---

## 7. Requisitos no funcionales (RNF-01 … RNF-13)

| ID | Categoría | Métrica verificable |
|---|---|---|
| RNF-01 | Privacidad/aislamiento | 0 % de fuga en pruebas cruzadas entre tenants. |
| RNF-02 | Seguridad | Contraseñas con hash, variables de entorno, HTTPS. |
| RNF-03 | Seguridad de pago | Cumplimiento PCI-DSS vía pasarela certificada. |
| RNF-04 | Rendimiento web | CRUD < 500 ms. |
| RNF-05 | Rendimiento IA | < 4 s por consulta en GPU. |
| RNF-06 | Disponibilidad | Uptime ≥ 99.5 % mensual. |
| RNF-07 | Escalabilidad | 100+ tenants simultáneos. |
| RNF-08 | Mantenibilidad | TypeScript/Python tipado + componentes documentados. |
| RNF-09 | Trazabilidad | Logs de app/errores, conservación ≥ 30 días. |
| RNF-10 | Respaldo | Exportación de datos por tenant (CSV/JSON). |
| RNF-11 | Local-first IA | 0 llamadas a APIs externas (OpenAI/Anthropic). |
| RNF-12 | Usabilidad | Diseño responsive y accesible (1024×768 y móvil). |
| RNF-13 | IA responsable | Sin decisiones críticas autónomas; la IA no ejecuta escrituras sin confirmación humana. |

---

## 8. Criterios de aceptación (CE-01 … CE-10)

| ID | Criterio | Meta |
|---|---|---|
| CE-01 | Aislamiento de tenants | 0 registros de otros tenants (pruebas de inyección cruzada). |
| CE-02 | Flujo de suscripción completo | 100 % de pagos exitosos crean tenant. |
| CE-03 | Funcionalidad CRUD inventario | 100 % de movimientos correctos. |
| CE-04 | Latencia web | < 500 ms por clic (Lighthouse). |
| CE-05 | Latencia IA | < 4 s en GPU de prueba. |
| CE-06 | Calidad del RAG | Tasa de alucinación < 5 % en 50 preguntas. |
| CE-07 | Onboarding del admin | < 15 min desde el pago hasta primera venta. |
| CE-08 | Seguridad de credenciales | 0 claves en frontend o repos (auditoría SAST). |
| CE-09 | Disponibilidad | Uptime ≥ 99.5 % mensual. |
| CE-10 | Multimodal (OCR) | Precisión ≥ 85 % en 50 imágenes. |

---

## 9. Decisiones técnicas del plan original (Plan + Build), adaptadas a Python + MySQL

1. **Modelo de datos:** `tenant_id` en todas las tablas de negocio (aislamiento por inquilino).
2. **Seguridad:** RLS (Row Level Security) — en MySQL se implementa con vistas/filtros en la capa de servicio (FastAPI) + filtros por `tenant_id` en cada consulta. Alternativa: PostgreSQL si se desea RLS nativo.
3. **IA local:** Ollama + modelos GGUF cuantizados, RAG con embeddings por tenant (pgvector → en MySQL se puede usar tablas con vectores o una BD vectorial auxiliar). Agente de solo lectura (no ejecuta escrituras). Componente multimodal (OCR).
4. **Flujo de suscripción:** landing → pasarela (PSE/tarjeta/Nequi) → activación automática de tenant + generación de credenciales de admin.
5. **Onboarding:** el admin recibe usuario, contraseña temporal y link de acceso; configura tienda sin asistencia técnica.
6. **OpenCode Plan + Build:** Fase PLAN (este documento) → Fase BUILD (tareas atómicas por épica, revisión humana obligatoria en migraciones BD, RLS, endpoints de pago y prompts IA).

### 9.1 Adaptación a MySQL (phpMyAdmin)
El esquema original (`supabase_schema.sql`) está en PostgreSQL. Para MySQL/phpMyAdmin se adaptan los tipos:

| PostgreSQL | MySQL (phpMyAdmin) |
|---|---|
| `UUID` | `CHAR(36)` o `BINARY(16)` |
| `TIMESTAMPTZ` | `DATETIME` |
| `NUMERIC(12,2)` | `DECIMAL(12,2)` |
| `JSONB` | `JSON` |
| `ENUM` (tipo) | `ENUM(...)` |
| `gen_random_uuid()` | `UUID()` (MySQL 8+) o generar en Python |
| RLS nativo | Filtros por `tenant_id` en la capa de servicio (FastAPI) |

> **Recomendación:** Si quieres RLS nativo a nivel BD, considera mantener PostgreSQL y usar **pgAdmin** en lugar de phpMyAdmin. Si te quedas en phpMyAdmin/MySQL, el aislamiento se hace en la capa de servicio (FastAPI) — más simple pero requiere disciplina.

---

## 10. Estructura de carpetas final propuesta (fácil de entender)

```
mercaking/                                    # RAÍZ DEL PROYECTO
│
├── PLAN_MERCAKING.md                         # Este plan (fase PLAN)
├── README.md                                 # Cómo correr el proyecto
│
├── backend/                                  # ⚙️ PYTHON — API REST (FastAPI)
│   ├── app/
│   │   ├── main.py                           # Punto de entrada (uvicorn)
│   │   ├── api/                              # Routers (endpoints)
│   │   │   ├── auth.py
│   │   │   ├── tenants.py
│   │   │   ├── dashboard.py
│   │   │   ├── products.py
│   │   │   ├── categories.py
│   │   │   ├── suppliers.py
│   │   │   ├── inventory.py
│   │   │   ├── sales.py
│   │   │   ├── reports.py
│   │   │   ├── users.py
│   │   │   └── ai.py
│   │   ├── core/                             # Config, seguridad, BD
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── models/                           # SQLAlchemy (ORM)
│   │   ├── schemas/                          # Pydantic
│   │   └── services/                         # Lógica de negocio
│   │       ├── inventory_service.py
│   │       ├── pos_service.py
│   │       └── ...
│   └── requirements.txt                      # fastapi, uvicorn, sqlalchemy, pymysql, ...
│
├── database/                                 # 🗄️ MySQL (phpMyAdmin)
│   ├── schema.sql                            # Tablas + tipos + funciones
│   ├── seed.sql                              # Datos demo (2 minimercados)
│   └── README_DB.md                          # Cómo importar en phpMyAdmin
│
├── ai/                                       # 🤖 Módulo de IA local (Fase 3)
│   ├── rag/
│   │   └── retriever.py
│   ├── agent/
│   │   └── stock_agent.py
│   └── ocr/
│       └── ...
│
├── frontend/                                 # 🖥️ Python — Web (Flask + Jinja2 + HTMX)
│   ├── app.py                                # Punto de entrada (Flask)
│   ├── templates/                            # Plantillas Jinja2
│   │   ├── base.html
│   │   ├── index.html                        # Landing
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── productos.html
│   │   ├── inventario.html
│   │   ├── ventas.html
│   │   ├── reportes.html
│   │   ├── usuarios.html
│   │   └── minimercados.html
│   ├── static/                               # CSS, JS, imágenes
│   │   ├── css/
│   │   └── js/
│   └── requirements.txt                      # flask, jinja2, requests, ...
│
├── docs/                                     # Documentación
│   └── PLAN_MERCAKING.md
│
└── .env.example                              # Variables de entorno
```

### 10.1 Notas sobre la estructura
- **`backend/`** = API Python (FastAPI). Toda la lógica de negocio y acceso a BD.
- **`database/`** = scripts SQL para MySQL, importables desde phpMyAdmin.
- **`ai/`** = módulo de IA local (Ollama, RAG, OCR). Se añade en Fase 3.
- **`frontend/`** = Python puro (Flask + Jinja2 + HTMX), branding MercaKing.
- **`docs/`** = plan y documentación.

> **Decisión confirmada:** stack 100 % Python (FastAPI backend + Flask/Jinja2 frontend) + MySQL (phpMyAdmin). Sin Next.js.

---

## 11. Roadmap por épicas y tareas (con DoD)

### Épica 1 — Landing + selección de plan
- T1.1 Landing pública (info, planes, CTA). DoD: carga < 2 s, muestra 3 planes.
- T1.2 Selección de plan → redirige a checkout. DoD: redirección correcta.

### Épica 2 — Pasarela de pago + activación de tenant
- T2.1 Integración pasarela (PSE/tarjeta/Nequi). DoD: pago confirmado + comprobante.
- T2.2 Activación automática de tenant + credenciales admin. DoD: admin recibe correo con usuario/contraseña/link.

### Épica 3 — Autenticación multi-inquilino + onboarding
- T3.1 Login vinculado al tenant_id. DoD: usuario solo accede a su minimercado.
- T3.2 Onboarding guiado (nombre, NIT, logo, primer producto). DoD: dashboard muestra datos reales.

### Épica 4 — CRUD productos / proveedores / usuarios
- T4.1 CRUD productos (código, nombre, precio, categoría, imagen). DoD: guardado con tenant_id.
- T4.2 CRUD proveedores. DoD: solo el tenant creador los ve.
- T4.3 Gestión de usuarios internos (cajeros/encargados). DoD: roles con permisos diferenciados.

### Épica 5 — Inventario + POS ligero
- T5.1 Entradas/salidas/ajustes auditados. DoD: cada movimiento registra usuario, fecha, tipo.
- T5.2 Alertas de stock bajo. DoD: indicador visual en panel.
- T5.3 POS (carrito, descuento de stock, recibo). DoD: stock se actualiza en tiempo real.

### Épica 6 — Reportes
- T6.1 Consolidados diarios/semanales/mensuales. DoD: totales coinciden con transacciones.
- T6.2 Ranking de productos más vendidos + valoración de inventario. DoD: datos correctos.
- T6.3 Exportación CSV. DoD: archivo descargable.

### Épica 7 — Asistente IA (RAG + agente + OCR) — Fase 3
- T7.1 RAG segregado por tenant. DoD: 50 preguntas ≥ 95 % correctas; aislamiento probado.
- T7.2 Agente de solo lectura. DoD: no ejecuta escrituras.
- T7.3 OCR multimodal. DoD: precisión ≥ 85 % en 50 imágenes.

### Épica 8 — Panel Superadmin
- T8.1 Gestión de suscriptores, planes, uso IA, logs. DoD: solo equipo MercaKing accede.

### Épica 9 — Seguridad, RLS y auditoría
- T9.1 Aislamiento CRUD (RLS / filtros por tenant_id). DoD: 0 registros cruzados.
- T9.2 Auditoría e interacciones IA. DoD: trazabilidad completa por tenant y usuario.

---

## 12. Riesgos técnicos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Complejidad de IA local (GPU, Ollama) | Dejar IA para Fase 3; empezar con asistente de reglas (ya en prototipo). |
| Aislamiento de tenants | Filtros por `tenant_id` en cada consulta + pruebas cruzadas (CE-01). |
| Pasarela de pago (compliance) | Usar pasarela certificada (PCI-DSS), no guardar datos de tarjeta. |
| Migración PG → MySQL | Adaptar tipos (ver §9.1); mantener un solo motor. |
| Alucinación del LLM | RAG con contexto del tenant; respuesta "sin información" si no hay contexto. |
| Scope creep | MVP primero; IA y superadmin en Fase 3. |

---

## 13. Pendientes — RESUELTOS ✅

1. **Motor de BD:** ✅ MySQL (phpMyAdmin).
2. **Branding:** ✅ MercaKing.
3. **Frontend:** ✅ Python puro (Flask + Jinja2).
4. **Git:** ✅ Inicializar repo con ramas `main`/`develop`/`feature/*`.
5. **DoD por épica:** a definir antes de cada tarea.
6. **Credenciales demo y datos semilla:** 2 minimercados (El Ahorro, San Jorge).

---

## 14. Siguiente paso (Build) — INICIANDO

1. Inicializar repositorio git (`git init`) y ramas `main`/`develop`.
2. Crear la estructura de carpetas (`backend/`, `database/`, `ai/`, `frontend/`, `docs/`).
3. Crear `database/schema.sql` + `seed.sql` (adaptados a MySQL) e importar en phpMyAdmin.
4. Crear `backend/` con FastAPI (main.py, routers, models, schemas, services) + `requirements.txt`.
5. Crear `frontend/` con Flask + Jinja2 (plantillas base, landing, login).
6. Crear `README.md`, `.env.example`, `.gitignore`.
7. Implementar Épica 1 → 2 → 3 → 5 (MVP) antes de IA (Épica 7).

> **Nota:** Este documento es la Fase PLAN. El código se genera en la fase Build (ahora iniciando).
