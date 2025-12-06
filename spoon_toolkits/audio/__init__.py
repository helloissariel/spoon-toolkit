# Spoon Toolkits - Audio module
"""Audio processing tools including ElevenLabs TTS, STT, voice cloning, and dubbing."""

from .elevenlabs_tools import (
    # Text-to-Speech
    ElevenLabsTextToSpeechTool,
    ElevenLabsTextToSpeechStreamTool,
    # Speech-to-Text
    ElevenLabsSpeechToTextTool,
    # Voice Design
    ElevenLabsVoiceDesignTool,
    ElevenLabsCreateVoiceFromPreviewTool,
    # Voice Clone
    ElevenLabsInstantVoiceCloneTool,
    # Dubbing
    ElevenLabsDubbingCreateTool,
    ElevenLabsDubbingStatusTool,
    ElevenLabsDubbingAudioTool,
    # Base class
    ElevenLabsToolBase,
)

__all__ = [
    # Text-to-Speech
    "ElevenLabsTextToSpeechTool",
    "ElevenLabsTextToSpeechStreamTool",
    # Speech-to-Text
    "ElevenLabsSpeechToTextTool",
    # Voice Design
    "ElevenLabsVoiceDesignTool",
    "ElevenLabsCreateVoiceFromPreviewTool",
    # Voice Clone
    "ElevenLabsInstantVoiceCloneTool",
    # Dubbing
    "ElevenLabsDubbingCreateTool",
    "ElevenLabsDubbingStatusTool",
    "ElevenLabsDubbingAudioTool",
    # Base class
    "ElevenLabsToolBase",
]

