"""
Tests for ElevenLabs Audio Tools

Run with: pytest toolkit/spoon_toolkits/audio/test_elevenlabs.py -v

These tests validate:
1. Tool initialization and parameter schemas
2. API key validation (graceful error when missing)
3. Input validation for required parameters
4. Integration tests (only run when ELEVENLABS_API_KEY is set)
"""

import os
import pytest
import asyncio

# Check if API key is available for integration tests
HAS_API_KEY = bool(os.getenv("ELEVENLABS_API_KEY"))

# Import tools
from .elevenlabs_tools import (
    ElevenLabsTextToSpeechTool,
    ElevenLabsTextToSpeechStreamTool,
    ElevenLabsSpeechToTextTool,
    ElevenLabsVoiceDesignTool,
    ElevenLabsCreateVoiceFromPreviewTool,
    ElevenLabsInstantVoiceCloneTool,
    ElevenLabsDubbingCreateTool,
    ElevenLabsDubbingStatusTool,
    ElevenLabsDubbingAudioTool,
    ELEVENLABS_API_KEY_ENV,
)


class TestToolInitialization:
    """Test that tools can be instantiated correctly."""

    def test_tts_tool_init(self):
        """Test TTS tool initialization."""
        tool = ElevenLabsTextToSpeechTool()
        assert tool.name == "elevenlabs_text_to_speech"
        assert "text" in tool.parameters["required"]

    def test_stt_tool_init(self):
        """Test STT tool initialization."""
        tool = ElevenLabsSpeechToTextTool()
        assert tool.name == "elevenlabs_speech_to_text"
        assert "file_path" in tool.parameters["required"]

    def test_voice_design_tool_init(self):
        """Test voice design tool initialization."""
        tool = ElevenLabsVoiceDesignTool()
        assert tool.name == "elevenlabs_voice_design"
        assert "voice_description" in tool.parameters["required"]

    def test_voice_clone_tool_init(self):
        """Test voice clone tool initialization."""
        tool = ElevenLabsInstantVoiceCloneTool()
        assert tool.name == "elevenlabs_instant_voice_clone"
        assert "name" in tool.parameters["required"]
        assert "files" in tool.parameters["required"]

    def test_dubbing_create_tool_init(self):
        """Test dubbing create tool initialization."""
        tool = ElevenLabsDubbingCreateTool()
        assert tool.name == "elevenlabs_dubbing_create"
        assert "file_path" in tool.parameters["required"]
        assert "target_lang" in tool.parameters["required"]


class TestApiKeyValidation:
    """Test API key validation behavior."""

    @pytest.fixture(autouse=True)
    def clear_api_key(self, monkeypatch):
        """Clear API key for these tests."""
        monkeypatch.delenv(ELEVENLABS_API_KEY_ENV, raising=False)

    @pytest.mark.asyncio
    async def test_tts_without_api_key(self):
        """Test TTS tool returns helpful error without API key."""
        tool = ElevenLabsTextToSpeechTool()
        result = await tool.execute(text="Test")

        # Should return error, not raise exception
        if hasattr(result, "error"):
            assert result.error is not None
            assert "ELEVENLABS_API_KEY" in result.error
        else:
            assert result.get("success") is False
            assert "ELEVENLABS_API_KEY" in result.get("error", "")

    @pytest.mark.asyncio
    async def test_stt_without_api_key(self):
        """Test STT tool returns helpful error without API key."""
        tool = ElevenLabsSpeechToTextTool()
        result = await tool.execute(file_path="/nonexistent.mp3")

        if hasattr(result, "error"):
            assert result.error is not None
            assert "ELEVENLABS_API_KEY" in result.error
        else:
            assert result.get("success") is False

    @pytest.mark.asyncio
    async def test_voice_design_without_api_key(self):
        """Test voice design tool returns helpful error without API key."""
        tool = ElevenLabsVoiceDesignTool()
        result = await tool.execute(voice_description="Test voice")

        if hasattr(result, "error"):
            assert result.error is not None
            assert "ELEVENLABS_API_KEY" in result.error
        else:
            assert result.get("success") is False


class TestInputValidation:
    """Test input validation for tools."""

    @pytest.fixture(autouse=True)
    def set_fake_api_key(self, monkeypatch):
        """Set a fake API key so we can test input validation."""
        monkeypatch.setenv(ELEVENLABS_API_KEY_ENV, "test_key_for_validation")

    @pytest.mark.asyncio
    async def test_stt_file_not_found(self):
        """Test STT tool handles missing file gracefully."""
        tool = ElevenLabsSpeechToTextTool()
        result = await tool.execute(file_path="/nonexistent/file.mp3")

        if hasattr(result, "error"):
            assert result.error is not None
            assert "not found" in result.error.lower() or "File not found" in result.error
        else:
            assert result.get("success") is False

    @pytest.mark.asyncio
    async def test_voice_clone_files_not_found(self):
        """Test voice clone tool handles missing files gracefully."""
        tool = ElevenLabsInstantVoiceCloneTool()
        result = await tool.execute(
            name="Test Voice",
            files=["/nonexistent1.mp3", "/nonexistent2.mp3"]
        )

        if hasattr(result, "error"):
            assert result.error is not None
            assert "not found" in result.error.lower()
        else:
            assert result.get("success") is False

    @pytest.mark.asyncio
    async def test_dubbing_file_not_found(self):
        """Test dubbing tool handles missing file gracefully."""
        tool = ElevenLabsDubbingCreateTool()
        result = await tool.execute(
            file_path="/nonexistent/video.mp4",
            target_lang="es"
        )

        if hasattr(result, "error"):
            assert result.error is not None
            assert "not found" in result.error.lower() or "File not found" in result.error
        else:
            assert result.get("success") is False


@pytest.mark.skipif(not HAS_API_KEY, reason="ELEVENLABS_API_KEY not set")
class TestIntegration:
    """Integration tests that require a real API key."""

    @pytest.mark.asyncio
    async def test_tts_basic(self):
        """Test basic TTS functionality."""
        tool = ElevenLabsTextToSpeechTool()
        result = await tool.execute(
            text="Hello, this is a test.",
            voice_id="JBFqnCBsd6RMkjVDRZzb"
        )

        if hasattr(result, "output") and result.output:
            assert result.output["success"] is True
            assert "audio_base64" in result.output
            assert result.output["audio_size_bytes"] > 0
        else:
            assert result.get("success") is True
            assert "audio_base64" in result

    @pytest.mark.asyncio
    async def test_voice_design_basic(self):
        """Test basic voice design functionality."""
        tool = ElevenLabsVoiceDesignTool()
        result = await tool.execute(
            voice_description="A friendly young American male voice",
            auto_generate_text=True
        )

        if hasattr(result, "output") and result.output:
            assert result.output["success"] is True
            assert result.output["preview_count"] > 0
        else:
            assert result.get("success") is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

