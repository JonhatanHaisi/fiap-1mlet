from infra.application import app

@app.get("/health")
def saudavel():
    return {"status": "ok"}
