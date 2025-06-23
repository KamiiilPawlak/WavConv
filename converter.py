from pydub import AudioSegment
import os

Format_audio = ['wav', 'mp3', 'm4a', 'flac', 'ogg', 'amr']

def convert_audio(input_path, output_path, output_format, **kwargs):
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Plik źródłowy nie istnieje: {input_path}")

    audio = AudioSegment.from_file(input_path)

    if output_format == "wav":
        if 'sample_rate' in kwargs:
            try:
                sample_rate = int(kwargs['sample_rate'])
                audio = audio.set_frame_rate(sample_rate)
            except ValueError:
                raise ValueError("Nieprawidłowa wartość sample_rate")

        if 'bit_depth' in kwargs:
            try:
                bit_depth = int(kwargs['bit_depth'])
                if bit_depth in [8, 16, 24, 32]:
                    audio = audio.set_sample_width(bit_depth // 8)
                else:
                    raise ValueError("Nieobsługiwana głębia bitowa")
            except ValueError:
                raise ValueError("Nieprawidłowa głębia bitowa")

    audio.export(output_path, format=output_format)
