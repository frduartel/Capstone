# Archivo: listar_voces.py
import pyttsx3

try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    print(f"Se encontraron {len(voices)} voces en tu sistema:")
    print("-" * 40)

    for i, voice in enumerate(voices):
        print(f"Voz #{i}:")
        print(f"  ID: {voice.id}")
        print(f"  Nombre: {voice.name}")
        
        languages = []
        try:
            # Intentar decodificar los idiomas si son bytes
            languages = [lang.decode('utf-8').lower() for lang in voice.languages]
        except AttributeError: # Si no son bytes o no tienen 'decode'
            languages = [str(lang).lower() for lang in voice.languages]
        except Exception as e_lang: # Otro error
            languages = [f"Error al leer idioma: {e_lang}"]

        print(f"  Idiomas: {languages}")
        print(f"  Género: {voice.gender}")
        print(f"  Edad: {voice.age}")
        print("-" * 20)

except Exception as e:
    print(f"Ocurrió un error al inicializar pyttsx3 o al obtener las voces: {e}")
    print("Asegúrate de tener pyttsx3 instalado y los drivers de voz de tu sistema funcionando.")