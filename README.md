# FastAPI Project Setup

To run the FastAPI server, follow the steps below.

---

## 1. Unzip the project archive

### macOS / Linux

```bash
unzip proj.zip
```

### Windows (PowerShell)

```powershell
Expand-Archive project.zip
```

---

## 2. Create and activate a virtual environment

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

---

## 3. Go to project folder

```bash
cd proj
cd project
```

---

## 4. Install required dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Start the FastAPI application

```bash
uvicorn main:app --reload
```

---

# Application URLs

After startup, the server will be available at:

- http://127.0.0.1:8000
- http://localhost:8000

---

# API Documentation

To view all available endpoints and methods, open:

- http://127.0.0.1:8000/docs

To access unavailable methods, that are locked behind username and password, enter
```bash
username: admin
password: 123admin
```

# Tasks are presented in root folder (out of "project" folder), you'll probably see it
```bash
tasks.py
```
