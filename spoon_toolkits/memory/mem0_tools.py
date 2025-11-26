"""Mem0-powered memory tools."""

import logging
from typing import Any, Dict, List, Optional

from pydantic import Field

from spoon_ai.memory.mem0_client import SpoonMem0
from spoon_ai.tools.base import BaseTool, ToolResult

logger = logging.getLogger(__name__)


class Mem0ToolBase(BaseTool):
    """Shared Mem0 tool wiring that supports client injection or config-based init."""

    mem0_config: Dict[str, Any] = Field(default_factory=dict, description="Mem0 client configuration")
    mem0_client: Optional[SpoonMem0] = Field(default=None, description="Optional injected SpoonMem0 client")
    default_user_id: Optional[str] = Field(
        default=None, description="Default user/agent id used when none is provided at call time"
    )

    def model_post_init(self, __context: Any = None) -> None:
        super().model_post_init(__context)
        if self.mem0_client is None:
            self.mem0_client = SpoonMem0(self.mem0_config)
        if self.default_user_id is None:
            self.default_user_id = (
                self.mem0_config.get("user_id")
                or self.mem0_config.get("agent_id")
                or (self.mem0_client.user_id if self.mem0_client else None)
            )

    def _resolve_user(self, user_id: Optional[str]) -> Optional[str]:
        return user_id or self.default_user_id

    def _get_client(self) -> Optional[SpoonMem0]:
        client = self.mem0_client
        if client and client.is_ready():
            return client
        return None


class AddMemoryTool(Mem0ToolBase):
    name: str = "add_memory"
    description: str = "Store text or conversation snippets in Mem0 for long-term recall."
    parameters: dict = {
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "Text to store as memory when not supplying structured messages",
            },
            "messages": {
                "type": "array",
                "description": "Optional list of role/content dicts to store together",
                "items": {
                    "type": "object",
                    "properties": {
                        "role": {"type": "string", "description": "Message role (e.g., user, assistant, system)"},
                        "content": {"type": "string", "description": "Message text"},
                    },
                },
            },
            "role": {
                "type": "string",
                "description": "Role tag used when content is provided directly",
                "default": "user",
            },
            "user_id": {
                "type": "string",
                "description": "Optional user/agent id override for this write",
            },
            "metadata": {
                "type": "object",
                "description": "Additional metadata to attach to the stored memory",
            },
        },
    }

    async def execute(
        self,
        content: Optional[str] = None,
        messages: Optional[List[Any]] = None,
        role: str = "user",
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ToolResult:
        client = self._get_client()
        if not client:
            return ToolResult(error="Mem0 client is not initialized; install mem0ai and set MEM0_API_KEY.")

        payload: List[Dict[str, str]] = []
        if messages:
            for message in messages:
                if isinstance(message, dict):
                    msg_role = str(message.get("role") or "user")
                    msg_content = message.get("content")
                else:
                    msg_role = "user"
                    msg_content = str(message)
                if msg_content:
                    payload.append({"role": msg_role, "content": str(msg_content)})

        if content:
            payload.append({"role": role or "user", "content": content})

        if not payload:
            return ToolResult(error="No memory content provided; pass content or messages.")

        try:
            active_user = self._resolve_user(user_id)
            client.add_memory(payload, user_id=active_user, metadata=metadata)
            return ToolResult(output={"status": "stored", "count": len(payload), "user_id": active_user})
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Failed to add memory via Mem0: %s", exc)
            return ToolResult(error=f"Failed to add memory: {exc}")


class SearchMemoryTool(Mem0ToolBase):
    name: str = "search_memory"
    description: str = "Search Mem0 for relevant stored memories using a natural language query."
    parameters: dict = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Natural language query describing what to recall from memory",
            },
            "user_id": {
                "type": "string",
                "description": "Optional user/agent id override for this search",
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of memories to return",
            },
        },
        "required": ["query"],
    }

    async def execute(
        self,
        query: str,
        user_id: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> ToolResult:
        client = self._get_client()
        if not client:
            return ToolResult(error="Mem0 client is not initialized; install mem0ai and set MEM0_API_KEY.")
        if not query:
            return ToolResult(error="Query is required to search memories.")

        try:
            memories = client.search_memory(query=query, user_id=self._resolve_user(user_id), limit=limit)
            return ToolResult(output={"memories": memories})
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Mem0 search failed: %s", exc)
            return ToolResult(error=f"Failed to search memories: {exc}")


class GetAllMemoryTool(Mem0ToolBase):
    name: str = "get_all_memory"
    description: str = "Fetch all stored memories for the configured or provided user."
    parameters: dict = {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "Optional user/agent id override for the retrieval",
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of memories to return",
            },
        },
    }

    async def execute(
        self,
        user_id: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> ToolResult:
        client = self._get_client()
        if not client:
            return ToolResult(error="Mem0 client is not initialized; install mem0ai and set MEM0_API_KEY.")

        try:
            memories = client.get_all_memory(user_id=self._resolve_user(user_id), limit=limit)
            return ToolResult(output={"memories": memories})
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Mem0 get_all failed: %s", exc)
            return ToolResult(error=f"Failed to fetch memories: {exc}")


__all__ = ["AddMemoryTool", "SearchMemoryTool", "GetAllMemoryTool"]
