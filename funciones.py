import json
import os
from typing import Dict, List, Optional, Any
import requests

DATA_FILE = "datos.json"
API_URL = "https://api.pokemontcg.io/v2/cards"


# ---------------------------------------------------------
# PERSISTENCIA Y CARGA DE DATOS
# ---------------------------------------------------------
def cargar_coleccion(filepath: str = DATA_FILE) -> List[Dict[str, Any]]:
    """Carga la colección desde un archivo JSON. Retorna lista vacía si no existe o hay error."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"[Error] No se pudo leer {filepath}: {e}")
        return []


def guardar_coleccion(coleccion: List[Dict[str, Any]], filepath: str = DATA_FILE) -> bool:
    """Guarda la colección dada en formato JSON."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(coleccion, f, ensure_ascii=False, indent=4)
        return True
    except IOError as e:
        print(f"[Error] No se pudo guardar en {filepath}: {e}")
        return False


# ---------------------------------------------------------
# CONSULTAS A LA API
# ---------------------------------------------------------
def buscar_carta_api(nombre: str) -> List[Dict[str, Any]]:
    """Busca cartas por nombre en la API pública de Pokémon TCG."""
    try:
        response = requests.get(f"{API_URL}?q=name:\"{nombre}\"", timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
    except requests.RequestException as e:
        print(f"[Error de Conexión/API] {e}")
        return []


def extraer_datos_carta(carta_raw: Dict[str, Any]) -> Dict[str, Any]:
    """Extrae y normaliza los datos relevantes de la respuesta de la API."""
    card_id = carta_raw.get("id", "Desconocido")
    name = carta_raw.get("name", "Sin Nombre")
    types = carta_raw.get("types", ["Incoloro"])
    tipo_principal = types[0] if types else "Incoloro"
    rarity = carta_raw.get("rarity", "Desconocida")
    set_name = carta_raw.get("set", {}).get("name", "Desconocido")
    
    # Manejo defensivo de HP
    try:
        hp = int(carta_raw.get("hp", 0))
    except (ValueError, TypeError):
        hp = 0

    # Manejo defensivo de precios en tcgplayer
    price = 0.0
    try:
        prices = carta_raw.get("tcgplayer", {}).get("prices", {})
        # Buscar el primer tipo de acabado disponible (holofoil, normal, market, etc.)
        for price_type in prices.values():
            if "market" in price_type and price_type["market"] is not None:
                price = float(price_type["market"])
                break
            elif "mid" in price_type and price_type["mid"] is not None:
                price = float(price_type["mid"])
                break
    except (KeyError, ValueError, TypeError):
        price = 0.0

    image_url = carta_raw.get("images", {}).get("small", "")

    return {
        "id": card_id,
        "nombre": name,
        "tipo": tipo_principal,
        "raraza": rarity,
        "set": set_name,
        "hp": hp,
        "precio_usd": price,
        "imagen_url": image_url,
        "cantidad": 1
    }


# ---------------------------------------------------------
# GESTIÓN DE LA COLECCIÓN
# ---------------------------------------------------------
def agregar_a_coleccion(coleccion: List[Dict[str, Any]], carta_nueva: Dict[str, Any], cantidad: int) -> List[Dict[str, Any]]:
    """Agrega una carta a la colección o incrementa la cantidad si ya existe."""
    for carta in coleccion:
        if carta["id"] == carta_nueva["id"]:
            carta["cantidad"] += cantidad
            return coleccion
    
    carta_nueva["cantidad"] = cantidad
    coleccion.append(carta_nueva)
    return coleccion


def modificar_cantidad(coleccion: List[Dict[str, Any]], card_id: str, nueva_cantidad: int) -> bool:
    """Modifica la cantidad o elimina la carta si la nueva cantidad es <= 0."""
    for i, carta in enumerate(coleccion):
        if carta["id"].lower() == card_id.lower():
            if nueva_cantidad <= 0:
                coleccion.pop(i)
            else:
                carta["cantidad"] = nueva_cantidad
            return True
    return False


# ---------------------------------------------------------
# INDICADORES Y CÁLCULOS
# ---------------------------------------------------------
def calcular_valor_total(coleccion: List[Dict[str, Any]]) -> float:
    """Calcula el valor económico estimado total acumulado en la colección."""
    return sum(c.get("precio_usd", 0.0) * c.get("cantidad", 1) for c in coleccion)


def carta_mas_repetida(coleccion: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Devuelve la carta con mayor número de copias."""
    if not coleccion:
        return None
    return max(coleccion, key=lambda c: c.get("cantidad", 0))


def tipo_mas_frecuente(coleccion: List[Dict[str, Any]]) -> str:
    """Determina el tipo elemental con más cartas asociadas en total."""
    if not coleccion:
        return "N/A"
    conteo_tipos: Dict[str, int] = {}
    for c in coleccion:
        t = c.get("tipo", "Incoloro")
        conteo_tipos[t] = conteo_tipos.get(t, 0) + c.get("cantidad", 1)
    return max(conteo_tipos, key=conteo_tipos.get)


def promedio_hp(coleccion: List[Dict[str, Any]]) -> float:
    """Calcula el HP promedio ponderado de las cartas poseídas."""
    total_cartas = sum(c.get("cantidad", 1) for c in coleccion)
    if total_cartas == 0:
        return 0.0
    sumatoria_hp = sum(c.get("hp", 0) * c.get("cantidad", 1) for c in coleccion)
    return sumatoria_hp / total_cartas


# ---------------------------------------------------------
# VALIDACIONES DE USUARIO
# ---------------------------------------------------------
def validar_entero_positivo(mensaje: str) -> int:
    """Solicita un número entero positivo por consola de forma segura."""
    while True:
        try:
            val = int(input(mensaje))
            if val >= 0:
                return val
            print("[!] Por favor, ingresá un número positivo o cero.")
        except ValueError:
            print("[!] Entrada inválida. Debe ser un número entero.")