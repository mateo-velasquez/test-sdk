from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import math

# Inicializamos la aplicación FastAPI
app = FastAPI(
    title="API de Cálculos Geométricos",
    description="Calcula el área de diferentes figuras geométricas (Triángulos y Cuadrados)."
)

# --- MODELOS DE ENTRADA (Validaciones con Pydantic) ---

class Triangulo(BaseModel):
    a: float = Field(..., gt=0, description="Longitud del lado A (debe ser mayor a 0)")
    b: float = Field(..., gt=0, description="Longitud del lado B (debe ser mayor a 0)")
    c: float = Field(..., gt=0, description="Longitud del lado C (debe ser mayor a 0)")

class Cuadrado(BaseModel):
    lado: float = Field(..., gt=0, description="Longitud del lado del cuadrado (debe ser mayor a 0)")


# --- ENDPOINTS (Rutas de la API) ---

@app.post("/calcular-area-triangulo/", tags=["Triángulos"])
def calcular_area_triangulo(triangulo: Triangulo):
    a = triangulo.a
    b = triangulo.b
    c = triangulo.c

    # Validación: Desigualdad triangular
    if (a + b <= c) or (a + c <= b) or (b + c <= a):
        raise HTTPException(
            status_code=400, 
            detail="Los lados proporcionados no forman un triángulo válido según la desigualdad triangular."
        )

    # Cálculo con Fórmula de Herón
    s = (a + b + c) / 2.0
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))

    return {
        "figura": "triangulo",
        "lados": {"a": a, "b": b, "c": c},
        "semiperimetro": s,
        "area": round(area, 4)
    }

@app.post("/calcular-area-cuadrado/", tags=["Cuadrados"])
def calcular_area_cuadrado(cuadrado: Cuadrado):
    lado = cuadrado.lado
    
    # El área de un cuadrado es lado al cuadrado (lado * lado)
    area = lado ** 2

    return {
        "figura": "cuadrado",
        "lado": lado,
        "area": round(area, 4)
    }