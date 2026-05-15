import os
import sys
import keyboard
from google import genai

# --- CONFIGURACIÓN DE TERMINAL (Para evitar errores de tildes) ---
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- CONFIGURACIÓN DE API ---
# RECUERDA: La llave debe estar "Restringida a Gemini API" en Google AI Studio
API_KEY = "TU_KEY" 
client = genai.Client(api_key=API_KEY)

def ejecutar_asistente():
    print("\n" + "="*40)
    print("ASISTENTE ACTIVO - ESPERANDO ORDEN")
    print("="*40)
    
    # Pedido por texto (El siguiente paso sería cambiar esto por Whisper/Voz)
    pedido = input("¿Qué quieres que haga el PC?: ")
    
    # Obtenemos rutas reales de tu Windows para dárselas a la IA
    user_path = os.path.expanduser("~")
    desktop_path = os.path.join(user_path, "Desktop")
    
    try:
        # Prompt optimizado para evitar errores de sintaxis en Windows
        prompt = (
            f"Eres un experto en CMD de Windows. El usuario quiere: {pedido}. "
            f"La ruta del escritorio es: {desktop_path}. "
            "Responde UNICAMENTE con el comando puro. "
            "Sin comillas, sin bloques de código, sin explicaciones."
        )
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt
        )
        
        # --- LIMPIEZA DE RESPUESTA ---
        # Quitamos los ```bash o ``` que a veces pone la IA por error
        comando = response.text.strip().replace("`", "").replace("'", "")
        
        # Si la IA usó barras de Linux (/), las pasamos a Windows (\)
        if "/" in comando and ":" in comando:
            comando = comando.replace("/", "\\")

        if comando:
            print(f"Ejecutando comando: {comando}")
            print("-" * 40)
            
            # Ejecución real en el sistema
            resultado = os.system(comando)
            
            if resultado == 0:
                print("-" * 40)
                print("¡Misión cumplida con éxito!")
            else:
                print("-" * 40)
                print("El comando se ejecutó pero el sistema devolvió un error.")
        else:
            print("La IA no generó un comando claro.")

    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    print("--------------------------------------------------")
    print("  ASISTENTE DE COMANDOS PARA WINDOWS (UTN 2026)   ")
    print("--------------------------------------------------")
    print("Instrucciones:")
    print("1. Presiona F8 para activar el asistente.")
    print("2. Escribe tu pedido (ej: 'crea una carpeta en escritorio').")
    print("3. ¡Mira cómo sucede la magia!")
    print("--------------------------------------------------")
    
    # Registrar el acceso directo
    keyboard.add_hotkey('f8', ejecutar_asistente)
    
    # Mantener el programa corriendo
    keyboard.wait()



    
