from pydantic import BaseModel
from typing import Optional

# Modelo base para cualquier colección
class BaseCollection(BaseModel):
    estado: int = 1  # 1 para activo, 0 para inactivo

# API Lugares
class LugarModel(BaseCollection):
    name: str
    description: Optional[str] = None
    direccion: str
    capacidad: int
    latitud: float
    longitud: float
    categoria: str
    codigo_postal: str
    ciudad: str
    pais: Optional[str] = None


# Modelo de Pizza - Ejemplo
class PizzaModel(BaseCollection):
    name: str
    description: Optional[str] = None
    ingredients: str
    size: str
    price: float
    is_vegetarian: bool

# Modelo de Bebida - Ejemplo
class DrinkModel(BaseCollection):
    name: str
    description: Optional[str] = None
    type: str
    volume_ml: int
    price: float
    is_alcoholic: bool