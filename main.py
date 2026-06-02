from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import math

# Inicializamos la aplicación FastAPI
app = FastAPI(
    title="API de Área de Triángulos",
    description="Calcula el área de un triángulo usando el Teorema de Herón."
)

# Definimos el modelo de datos de entrada con validación
class Triangulo(BaseModel):
    a: float = Field(..., gt=0, description="Longitud del lado A (debe ser mayor a 0)")
    b: float = Field(..., gt=0, description="Longitud del lado B (debe ser mayor a 0)")
    c: float = Field(..., gt=0, description="Longitud del lado C (debe ser mayor a 0)")

@app.post("/calcular-area/", tags=["Cálculos Geométricos"])
def calcular_area(triangulo: Triangulo):
    a = triangulo.a
    b = triangulo.b
    c = triangulo.c

    # Validación 1: Desigualdad triangular (la suma de dos lados debe ser mayor al tercero)
    if (a + b <= c) or (a + c <= b) or (b + c <= a):
        raise HTTPException(
            status_code=400, 
            detail="Los lados proporcionados no forman un triángulo válido según la desigualdad triangular."
        )

    # Cálculo del semiperímetro
    s = (a + b + c) / 2.0

    # Aplicación de la fórmula de Herón
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))

    return {
        "lados": {"a": a, "b": b, "c": c},
        "semiperimetro": s,
        "area": round(area, 4) # Redondeado a 4 decimales para mayor claridad
    }