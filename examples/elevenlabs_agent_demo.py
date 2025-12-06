"""
ElevenLabs Audio Agent Demo

An AI agent using ElevenLabs audio tools for TTS, STT, and voice design.

Usage:
    export ELEVENLABS_API_KEY="your_key"
    python elevenlabs_agent_demo.py
"""

import asyncio
import base64
import os
import sys
import tempfile
from pathlib import Path

from pydantic import Field

from spoon_ai.agents.spoon_react import SpoonReactAI
from spoon_ai.chat import ChatBot
from spoon_ai.llm.manager import get_llm_manager
from spoon_ai.tools.tool_manager import ToolManager
from spoon_toolkits.audio import (
    ElevenLabsTextToSpeechTool,
    ElevenLabsTextToSpeechStreamTool,
    ElevenLabsSpeechToTextTool,
    ElevenLabsVoiceDesignTool,
)


class AudioAgent(SpoonReactAI):
    """AI Agent with ElevenLabs audio tools."""

    available_tools: ToolManager = Field(default_factory=lambda: ToolManager([]))

    def model_post_init(self, __context=None) -> None:
        super().model_post_init(__context)
        self.available_tools = ToolManager([
            ElevenLabsTextToSpeechTool(),
            ElevenLabsTextToSpeechStreamTool(),
            ElevenLabsSpeechToTextTool(),
            ElevenLabsVoiceDesignTool(),
        ])
        if hasattr(self, "_refresh_prompts"):
            self._refresh_prompts()


def build_agent() -> AudioAgent:
    """Create audio agent with OpenAI."""
    return AudioAgent(
        llm=ChatBot(
            llm_provider="openai",
            model_name="gpt-4.1-mini",
            enable_long_term_memory=False,
        ),
        system_prompt="You are an audio assistant with ElevenLabs tools.",
    )


async def main():
    if not os.getenv("ELEVENLABS_API_KEY"):
        print("Set ELEVENLABS_API_KEY environment variable")
        sys.exit(1)

    print("ElevenLabs Audio Agent Demo\n")

    try:
        agent = build_agent()
        tools = agent.available_tools
        print(f"Tools: {[t.name for t in tools.tools]}\n")

        # Demo 1: Text-to-Speech
        print("1. Text-to-Speech")
        result = await tools.execute(
            name="elevenlabs_text_to_speech",
            tool_input={
                "text": "Hello! I am your AI audio assistant.",
                "voice_id": "JBFqnCBsd6RMkjVDRZzb",
            },
        )
        out = result.output if hasattr(result, "output") else result
        if out.get("success"):
            audio = base64.b64decode(out["audio_base64"])
            path = Path(tempfile.gettempdir()) / "tts_demo.mp3"
            path.write_bytes(audio)
            print(f"   Generated {len(audio)} bytes -> {path}\n")
        else:
            print(f"   Error: {out.get('error')}\n")
            path = None

        # Demo 2: Speech-to-Text
        if path and path.exists():
            print("2. Speech-to-Text")
            result = await tools.execute(
                name="elevenlabs_speech_to_text",
                tool_input={"file_path": str(path), "model_id": "scribe_v1"},
            )
            out = result.output if hasattr(result, "output") else result
            if out.get("success"):
                print(f"   Transcription: {out['text']}\n")
            else:
                print(f"   Error: {out.get('error')}\n")

        # Demo 3: Streaming TTS
        print("3. Streaming TTS with Timestamps")
        result = await tools.execute(
            name="elevenlabs_text_to_speech_stream",
            tool_input={
                "text": "Streaming provides real-time audio with timing data.",
                "voice_id": "JBFqnCBsd6RMkjVDRZzb",
            },
        )
        out = result.output if hasattr(result, "output") else result
        if out.get("success"):
            print(f"   {out['audio_size_bytes']} bytes, {out['total_alignment_points']} alignment points")
            if out.get("alignment"):
                print(f"   Sample: {out['alignment'][:3]}\n")
        else:
            print(f"   Error: {out.get('error')}\n")

        print("Demo completed!")

    except ImportError as e:
        print(f"Import error: {e}")
        print("Install: pip install spoon-ai spoon-toolkits elevenlabs")
    finally:
        await get_llm_manager().cleanup()


if __name__ == "__main__":
    asyncio.run(main())
