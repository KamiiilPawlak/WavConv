from pydub import AudioSegment
import os
import sys

input_file = "audio_samples/test_c.m4a"

output_dir = "audio_conv"
name_convert_file = input("Nazwa pliku po konwersji (bez rozszerzenia): ")
name_format = input("Do jakiego formatu przekonwertować (np. mp3, wav, ogg): ").lower()
output_file = os.path.join(output_dir, f"{name_convert_file}.{name_format}")

def convert_audio(input_path, output_path, output_format):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Utworzono katalog wyjściowy: {output_dir}")

    if not os.path.exists(input_path):
        print(f"Błąd: Plik źródłowy nie znaleziony: {input_path}")
        print("Upewnij się, że ścieżka do pliku jest poprawna i plik istnieje.")
        sys.exit(1)

    try:
        print(f"Ładowanie pliku: {input_path}")
        audio = AudioSegment.from_file(input_path)

        print(f"Konwertowanie pliku do formatu {output_format}...")
        audio.export(output_path, format=output_format)
        print(f"Konwersja zakończona pomyślnie: {output_path}")
    except Exception as e:
        print(f"Wystąpił błąd podczas konwersji: {e}")
        print("Upewnij się, że FFmpeg jest poprawnie zainstalowany i dostępny w PATH.")


convert_audio(input_file, output_file, name_format)
