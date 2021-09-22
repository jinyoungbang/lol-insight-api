### Activate Virtualenv and install required dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### To run the server locally

```bash
cd app
uvicorn main:app --reload
```

### Freeze requirements before deploying.

```bash
pip freeze -l > requirements.txt 
```
