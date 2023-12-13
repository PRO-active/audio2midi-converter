import streamlit as st
import note_seq
from inference_model import InferenceModel
from pydub import AudioSegment
import io

# Load MT3 model
MODEL_OPTIONS = {"ピアノ採譜モデル": "ismir2021", "複数楽器採譜モデル": "mt3"}
selected_model = st.selectbox("モデルを選択してください", list(MODEL_OPTIONS.keys()))

MODEL = MODEL_OPTIONS[selected_model]
CHECKPOINT_PATH = f'/app/checkpoints/{MODEL}/'
inference_model = InferenceModel(CHECKPOINT_PATH, MODEL)

st.title("Audio to MIDI Transcription with MT3")

# File upload
uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3"])

def upload_audio(file):
    data = file.read()
    file_extension = file.name.split('.')[-1]
    if file_extension.lower() == 'mp3':
        wav_data = mp3_to_wav(data)
        audio_samples = note_seq.audio_io.wav_data_to_samples_librosa(wav_data, sample_rate=inference_model.SAMPLE_RATE)
    else:
        audio_samples = note_seq.audio_io.wav_data_to_samples_librosa(data, sample_rate=inference_model.SAMPLE_RATE)
    return audio_samples

def mp3_to_wav(mp3_data):
    audio = AudioSegment.from_mp3(io.BytesIO(mp3_data))
    wav_data = audio.raw_data
    # sample_rate = audio.frame_rate
    return wav_data

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')

    # Perform transcription
    with st.spinner('Transcribing...'):
        # Perform transcription
        audio_samples = upload_audio(uploaded_file)
        est_ns = inference_model(audio_samples)
    print("Predicted MIDI Data:")
    print(est_ns.notes[-1])

    # Download MIDI button
    # if st.button("Download MIDI Transcription"):
    #     midi_filename = "/app/transcribed.mid"
    #     note_seq.sequence_proto_to_midi_file(est_ns, midi_filename)
    #     st.download_button("Download your transcription", midi_filename, file_name="transcribed.mid", key="transcription")
    midi_filename = "/app/transcribed.mid"
    note_seq.sequence_proto_to_midi_file(est_ns, midi_filename)
    with open(midi_filename, 'rb') as f:
        st.download_button("Download your transcription", f.read(), file_name="transcribed.mid", key="transcription")
