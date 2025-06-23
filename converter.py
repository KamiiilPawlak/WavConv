from pydub import AudioSegment
import os
import sys

input_file = "audio_samples/test_c.m4a"

Format_audio = ['wav', 'mp3', 'm4a', 'flac', 'aiff', 'ogg', 'amr']

output_dir = "audio_conv"
name_convert_file = input("Nazwa pliku po konwersji (bez rozszerzenia): ")

try:
    name_format = input("Do jakiego formatu przekonwertować: ").lower()

    if name_format not in Format_audio:
        raise ValueError(f"Format '{name_format}' nie jest obsługiwany.")

    output_file = os.path.join(output_dir, f"{name_convert_file}.{name_format}")
    print(f"Plik zostanie zapisany jako: {output_file}")

except ValueError as e:
    print("Błąd:", e)
    print(f"Dozwolone formaty to: {', '.join(Format_audio)}")
    sys.exit(1)



def convert_audio(input_path, output_path, output_format, **kwargs):
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

        if output_format == "wav":

            if 'sample_rate' in kwargs:
                try:
                    sample_rate = int(kwargs['sample_rate'])
                    audio = audio.set_frame_rate(sample_rate)
                    print(f"Ustawiono częstotliwość próbkowania na: {sample_rate} Hz")  # Poprawiona literówka
                except ValueError:
                    print("Ostrzeżenie: Nieprawidłowa częstotliwość próbkowania. Użyto domyślnej.")

            if 'bit_depth' in kwargs:
                try:
                    bit_depth = int(kwargs['bit_depth'])
                    bit_depth_value = [8,16,24,32]
                    if bit_depth in bit_depth_value:
                        audio = audio.set_sample_width(bit_depth // 8)
                        print(f"Ustawiono głębię bitową na: {bit_depth} bitów.")
                    else:
                        print(
                            f"Ostrzeżenie: Nieobsługiwana głębia bitowa ({bit_depth}). Dostępne: 8, 16, 24, 32.")
                except ValueError:
                    print("Ostrzeżenie: Nieprawidłowa głębia bitowa. Użyto domyślnej.")

        print(f"Konwertowanie pliku do formatu {output_format}...")
        audio.export(output_path, format=output_format)
        print(f"Konwersja zakończona pomyślnie: {output_path}")
    except Exception as e:
        print(f"Wystąpił błąd podczas konwersji: {e}")
        print("Upewnij się, że FFmpeg jest poprawnie zainstalowany i dostępny w PATH.")
        sys.exit(1)




if name_format == 'wav':

    sample_rate_input = input("Podaj częstotliwość próbkowania (np. 44100, pozostaw puste dla domyślnej): ")
    bit_depth_input = input("Podaj głębię bitową (np. 16, 24, 32, pozostaw puste dla domyślnej): ")

    wav_params = {}
    if sample_rate_input:
        wav_params['sample_rate'] = sample_rate_input
    if bit_depth_input:
        wav_params['bit_depth'] = bit_depth_input

    convert_audio(input_file, output_file, name_format, **wav_params)
else:
    convert_audio(input_file, output_file, name_format)