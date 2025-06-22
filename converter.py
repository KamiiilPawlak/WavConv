from pydub import AudioSegment
import os


input_file = "audio_samples/test_c.m4a"


output_dir = "audio_conv"
name_convert_file = input("Nazwa pliku po konwercji: ")
name_format = input("Nazwa pliku po konwercji: ")
output_file = os.path.join(output_dir, f"{name_convert_file}.{name_format}")


if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Utworzono katalog wyjściowy: {output_dir}")

if not os.path.exists(input_file):
    print(f"Błąd: Plik źródłowy nie znaleziony: {input_file}")
    print("Upewnij się, że ścieżka do pliku jest poprawna i plik istnieje.")
    exit()
else:
    try:
        print(f"Ładowanie pliku: {input_file}")
        audio = AudioSegment.from_file(input_file)

        print(f"Konwertowanie pliku {input_file} do {name_format}...")
        audio.export(output_file, format=name_format)
        print(f"Konwersja zakończona pomyślnie: {output_file}")
    except Exception as e:
        print(f"Wystąpił błąd podczas konwersji: {e}")
        print("Upewnij się, że FFmpeg jest poprawnie zainstalowany i dostępny w PATH.")