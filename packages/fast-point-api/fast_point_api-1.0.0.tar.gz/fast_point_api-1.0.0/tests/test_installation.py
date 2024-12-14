from fast_point_api.app_factory import create_app
from fast_point_api.schemas import PizzaModel

# Verificar que la app se inicializa correctamente
app = create_app(connection_url="http://admin:admin@localhost:5984")
print("Fast Point API initialized successfully.")

# Verificar que el modelo funciona correctamente
pizza = PizzaModel(
    name="Margarita",
    description="Pizza clásica",
    ingredients="Tomate, queso",
    size="Mediana",
    price=12.99,
    is_vegetarian=True,
)
print(f"Pizza creada: {pizza}")
