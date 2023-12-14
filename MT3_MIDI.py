import streamlit as st
import note_seq
from inference_model import InferenceModel
from pydub import AudioSegment
import io

st.title("Audio to MIDI Transcription with MT3")
# Load MT3 model
MODEL_OPTIONS = ["---", "ピアノ採譜モデル", "複数楽器採譜モデル"]
MODEL = st.selectbox("モデルを選択してください", MODEL_OPTIONS)

# モデルの選択に基づいてInferenceModelを初期化
if MODEL == "ピアノ採譜モデル":
    MODEL_TYPE = "ismir2021"
elif MODEL == "複数楽器採譜モデル":
    MODEL_TYPE = "mt3"
else:
    MODEL_TYPE = None
    inference_model =None

# モデルが選択されている場合のみモデルを初期化
if MODEL_TYPE is not None:
    CHECKPOINT_PATH = f'/app/checkpoints/{MODEL_TYPE}/'
    inference_model = InferenceModel(CHECKPOINT_PATH, MODEL_TYPE)

# File upload
uploaded_file = st.file_uploader("音声ファイルのアップロード", type=["wav", "mp3"])

def upload_audio(file):
    data = file.read()
    file_extension = file.name.split('.')[-1]
    if file_extension.lower() == 'mp3':
        print("mp3です")
        wav_data = mp3_to_wav(data)
        audio_samples = note_seq.audio_io.wav_data_to_samples_librosa(wav_data, sample_rate=inference_model.SAMPLE_RATE)
    else:
        audio_samples = note_seq.audio_io.wav_data_to_samples_librosa(data, sample_rate=inference_model.SAMPLE_RATE)
    return audio_samples

def mp3_to_wav(mp3_data):
    temp_mp3_file = "/app/temp.mp3"
    with open(temp_mp3_file, "wb") as f:
        f.write(mp3_data)
    audio = AudioSegment.from_mp3(temp_mp3_file)
    wav_data = audio.export(format="wav").read()
    return wav_data

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')

    # Perform transcription
    if inference_model is not None:
        if st.button("実行"):
            with st.spinner('Transcribing...'):
                audio_samples = upload_audio(uploaded_file)
                est_ns = inference_model(audio_samples)

    # Download MIDI button
    # if st.button("Download MIDI Transcription"):
    #     midi_filename = "/app/transcribed.mid"
    #     note_seq.sequence_proto_to_midi_file(est_ns, midi_filename)
    #     st.download_button("Download your transcription", midi_filename, file_name="transcribed.mid", key="transcription")
            midi_filename = "/app/transcribed.mid"
            note_seq.sequence_proto_to_midi_file(est_ns, midi_filename)
            with open(midi_filename, 'rb') as f:
                st.download_button("Download MIDI file", f.read(), file_name="transcribed.mid", key="transcription")
