from funciones import (
    cargar_coleccion, guardar_coleccion, buscar_carta_api,
    extraer_datos_carta, agregar_a_coleccion, modificar_cantidad,
    calcular_valor_total, carta_mas_repetida, tipo_mas_frecuente,
    promedio_hp, validar_entero_positivo
)

def mostrar_menu():
    print("\n" + "="*45)
    print("      📇 POKÉDEX TCG - COLECCIÓN PERSONAL")
    print("="*45)
    print("1. Buscar carta en la API y agregar a la colección")
    print("2. Ver colección completa")
    print("3. Filtrar colección (por tipo o rareza)")
    print("4. Modificar cantidad o eliminar carta")
    print("5. Ver indicadores y estadísticas generales")
    print("6. Guardar y Salir")
    print("="*45)

def main():
    coleccion = cargar_coleccion()
    print(f"-> Colección cargada con éxito: {len(coleccion)} ítems distintos.")

    while True:
        mostrar_menu()
        opcion = input("Seleccioná una opción (1-6): ").strip()

        if opcion == "1":
            nombre = input("\nIngresá el nombre de la carta a buscar (en inglés, ej. Pikachu): ").strip()
            if not nombre:
                continue
            print("Buscando en la API de Pokémon TCG...")
            resultados = buscar_carta_api(nombre)

            if not resultados:
                print("❌ No se encontraron cartas con ese nombre o falló la conexión.")
                continue

            print(f"\nSe encontraron {len(resultados)} resultados (mostrando hasta 5):")
            for i, carta_raw in enumerate(resultados[:5]):
                c = extraer_datos_carta(carta_raw)
                precio_str = f"${c['precio_usd']:.2f} USD" if c['precio_usd'] > 0 else "Precio no disponible"
                print(f"[{i+1}] {c['nombre']} (ID: {c['id']}) | Set: {c['set']} | Rareza: {c['raraza']} | {precio_str}")

            sel = validar_entero_positivo("Ingresá el número de la carta que querés agregar (0 para cancelar): ")
            if 1 <= sel <= min(5, len(resultados)):
                carta_elegida = extraer_datos_carta(resultados[sel - 1])
                cant = validar_entero_positivo(f"¿Cuántas copias de '{carta_elegida['nombre']}' tenés?: ")
                if cant > 0:
                    coleccion = agregar_a_coleccion(coleccion, carta_elegida, cant)
                    guardar_coleccion(coleccion)
                    print(f"✅ ¡Agregadas {cant} copia(s) de {carta_elegida['nombre']} a tu colección!")

        elif opcion == "2":
            if not coleccion:
                print("\n📭 Tu colección está vacía.")
                continue
            print("\n--- TU COLECCIÓN ---")
            for c in coleccion:
                p_str = f"${c['precio_usd']:.2f}" if c['precio_usd'] > 0 else "N/D"
                print(f"• ID: {c['id']:<12} | {c['nombre']:<20} | Tipo: {c['tipo']:<10} | Cantidad: {c['cantidad']} | Precio c/u: {p_str}")

        elif opcion == "3":
            if not coleccion:
                print("\n📭 Tu colección está vacía.")
                continue
            criterio = input("Filtrar por (1) Tipo o (2) Rareza?: ").strip()
            if criterio == "1":
                tipo_buscado = input("Ingresá el tipo (ej. Fire, Water, Lightning): ").strip().lower()
                filtrados = [c for c in coleccion if c.get("tipo", "").lower() == tipo_buscado]
            elif criterio == "2":
                rareza_buscada = input("Ingresá la rareza (ej. Common, Rare, Rare Holo): ").strip().lower()
                filtrados = [c for c in coleccion if rareza_buscada in c.get("raraza", "").lower()]
            else:
                print("Opción inválida.")
                continue

            print(f"\nResultados encontrados ({len(filtrados)}):")
            for c in filtrados:
                print(f"• {c['nombre']} (ID: {c['id']}) - Tipo: {c['tipo']} - Rareza: {c['raraza']} - Copias: {c['cantidad']}")

        elif opcion == "4":
            if not coleccion:
                print("\n📭 Tu colección está vacía.")
                continue
            card_id = input("Ingresá el ID exacto de la carta a modificar (ej. base1-4): ").strip()
            nueva_cant = validar_entero_positivo("Ingresá la nueva cantidad de copias (0 para eliminarla): ")
            if modificar_cantidad(coleccion, card_id, nueva_cant):
                guardar_coleccion(coleccion)
                print("✅ Colección actualizada correctamente.")
            else:
                print("❌ No se encontró ninguna carta con ese ID en tu colección.")

        elif opcion == "5":
            if not coleccion:
                print("\n📭 Tu colección está vacía.")
                continue
            v_total = calcular_valor_total(coleccion)
            c_repetida = carta_mas_repetida(coleccion)
            t_frecuente = tipo_mas_frecuente(coleccion)
            prom_hp = promedio_hp(coleccion)

            print("\n--- INDICADORES DE TU COLECCIÓN ---")
            print(f"💰 Valor total estimado: ${v_total:.2f} USD")
            print(f"🔥 Tipo dominante: {t_frecuente}")
            print(f"❤️ Promedio de HP: {prom_hp:.1f}")
            if c_repetida:
                print(f"🃏 Carta más repetida: {c_repetida['nombre']} ({c_repetida['cantidad']} copias)")

        elif opcion == "6":
            guardar_coleccion(coleccion)
            print("\n💾 Colección guardada. ¡Hasta la próxima!")
            break

if __name__ == "__main__":
    main()