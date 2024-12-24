# Ruta del fichero
file_path = "datos_players.txt"

# Leer y procesar el fichero
with open(file_path, "r") as file:
    formatted_data = []
    for line in file:
        if line.strip():  # Evitar líneas vacías
            # Dividir la línea en dos partes: jugador y equipo
            parts = line.split(",", 1)  # Divide solo en la primera coma
            if len(parts) == 2:
                player, team = map(str.strip, parts)
                formatted_data.append((player, team))
            else:
                print(f"⚠️ Formato incorrecto: {line.strip()}")

# Imprimir los datos en el formato requerido
for player_team in formatted_data:
    print(f'{player_team},')
