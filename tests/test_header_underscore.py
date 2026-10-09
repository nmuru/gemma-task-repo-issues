from fastapi import FastAPI, Header
from fastapi.testclient import TestClient
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

class HeaderCollector(BaseModel):
    my_header: str | None = None

@app.get("/items/")
def read_items(headers: Annotated[HeaderCollector, Header()]):
    return headers.model_dump()

client = TestClient(app)

def test_header_smuggling_vulnerability():
    response = client.get("/items/", headers={"my_header": "sneaky_value"})
    body = response.json()
    
    print(f"\n=== APP RESPONSE ===\n{body}")
    
    # Assert it should be None. If it's not, the bug is active.
    assert body.get("my_header") is None, f"BUG ACTIVE: FastAPI accepted the smuggled header! {body}"
