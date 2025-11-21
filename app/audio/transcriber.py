import os
from typing import Literal, Optional

from faster_whisper import WhisperModel


class FastWhisperTranscriber:
    """
    faster-whisper 기반 음성 → 텍스트 변환기.

    - 프로세스 시작 시 한 번만 모델을 로드해서 재사용.
    - 기본 모델 크기: small (env로 조정 가능)
      - DEFAULT_WHISPER_MODEL_SIZE: tiny / base / small / medium / large 등
      - DEFAULT_WHISPER_DEVICE: "cpu" / "cuda" / "auto"
      - DEFAULT_WHISPER_COMPUTE_TYPE: "int8" / "int8_float16" / "float16" / "float32" 등
    """

    def __init__(self, model_size: str | None = None, device: Literal["cpu", "cuda", "auto"] = "cpu", compute_type: str = "float32"):
        self.model_size = model_size or os.getenv("DEFAULT_WHISPER_MODEL_SIZE", "small")
        self.device = os.getenv("DEFAULT_WHISPER_DEVICE", device)
        self.compute_type = os.getenv("DEFAULT_WHISPER_COMPUTE_TYPE", compute_type)

        print(
            f"[FastWhisperTranscriber] loading model='{self.model_size}', "
            f"device='{self.device}', compute_type='{self.compute_type}'"
        )

        self.model = WhisperModel(
            self.model_size,
            device=self.device,
            compute_type=self.compute_type,
        )

    def transcribe(self, audio_path: str, language: Optional[str] = None) -> str:
        segments, info = self.model.transcribe(
            audio_path,
            language=language,
            beam_size=5,
        )

        texts: list[str] = []
        for seg in segments:
            if seg.text:
                texts.append(seg.text.strip())

        full_text = " ".join(texts).strip()
        return full_text


transcriber = FastWhisperTranscriber()
