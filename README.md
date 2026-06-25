# Mundial 2026 - Backend

API FastAPI del simulador del Mundial 2026.

## Desarrollo local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
uvicorn main:app --host 127.0.0.1 --port 8000
```

API: `http://127.0.0.1:8000`

Swagger: `http://127.0.0.1:8000/docs`

## CI/CD

GitHub Actions ejecuta Ruff, 72 tests, cobertura, Quality Gate del 80 % y
validación de la imagen Docker.
