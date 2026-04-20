# Agent Creative — Text-to-Video Automation Pipeline

Pipeline otomatisasi konten yang mengubah script JSON menjadi video siap upload (YouTube Shorts / TikTok) secara otomatis menggunakan AI.

## Stack

| Layer | Library |
|---|---|
| CLI | `rich` |
| Text-to-Speech | `edge-tts` |
| Image Generation | Hugging Face Inference API (FLUX.1-schnell) |
| Video Assembly | `moviepy` |
| Config | `pydantic-settings` |

## Struktur Folder

```
agent_creative/
├── main.py
├── config.py
├── requirements.txt
├── .env                  ← buat dari .env.example
├── data/
│   ├── input/            ← letakkan file JSON di sini
│   │   └── _processed/   ← file JSON dipindah ke sini setelah render
│   ├── output/           ← hasil video .mp4
│   └── temp/             ← workspace sementara (otomatis dihapus)
└── src/
    ├── core/             ← entities, ports, exceptions
    ├── application/      ← render_use_case (orkestrator)
    ├── infrastructure/   ← adapter TTS, HuggingFace, MoviePy, LocalStorage
    └── interfaces/       ← CLI rich
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

Isi file `.env`:
```
HF_API_TOKEN=your_huggingface_token_here
```

## Jalankan

```bash
python main.py
```

## Alur Kerja

1. Letakkan file JSON (format dari `agent_director`) ke folder `data/input/`
2. Jalankan `python main.py`
3. Pilih file JSON → pilih script → atur suara (opsional) → render
4. Video `.mp4` tersimpan di `data/output/`
5. File JSON sumber dipindahkan otomatis ke `data/input/_processed/`