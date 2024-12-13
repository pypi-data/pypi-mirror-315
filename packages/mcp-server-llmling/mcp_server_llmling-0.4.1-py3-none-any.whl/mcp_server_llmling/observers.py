"""Observer implementations for converting registry events to MCP notifications."""

from __future__ import annotations

from typing import TYPE_CHECKING

from llmling.config.models import BaseResource
from llmling.core.events import Event, EventType, RegistryEvents
from llmling.prompts.models import BasePrompt
from llmling.tools.base import LLMCallableTool

from mcp_server_llmling.log import get_logger


if TYPE_CHECKING:
    from mcp_server_llmling.server import LLMLingServer


logger = get_logger(__name__)


class ResourceObserver:
    """Converts resource registry events to MCP notifications."""

    def __init__(self, server: LLMLingServer) -> None:
        self.server = server
        self.events = RegistryEvents[str, BaseResource]()
        self.events.on_item_added = self._handle_resource_added
        self.events.on_item_modified = self._handle_resource_modified
        self.events.on_item_removed = self._handle_resource_removed
        self.events.on_list_changed = self._handle_resource_list_changed
        self.events.on_reset = self._handle_registry_reset

    def _handle_resource_added(self, key: str, resource: BaseResource) -> None:
        """Handle resource addition."""
        event = Event(
            type=EventType.RESOURCE_ADDED,
            source="resource_registry",
            name=key,
            data=resource,
        )
        self.server._create_task(self.server.runtime.emit_event(event))
        self.server._create_task(self.server.notify_resource_list_changed())

    def _handle_resource_modified(self, key: str, resource: BaseResource) -> None:
        """Handle resource modification."""
        event = Event(
            type=EventType.RESOURCE_MODIFIED,
            source="resource_registry",
            name=key,
            data=resource,
        )
        self.server._create_task(self.server.runtime.emit_event(event))
        loader = self.server.runtime.get_resource_loader(resource)
        uri = loader.create_uri(name=key)
        self.server._create_task(self.server.notify_resource_change(uri))

    def _handle_resource_removed(self, key: str, resource: BaseResource) -> None:
        """Handle resource removal."""
        event = Event(
            type=EventType.RESOURCE_REMOVED,
            source="resource_registry",
            name=key,
            data=resource,
        )
        self.server._create_task(self.server.runtime.emit_event(event))
        self.server._create_task(self.server.notify_resource_list_changed())

    def _handle_resource_list_changed(self) -> None:
        """Handle resource list changes."""
        event = Event(type=EventType.RESOURCE_LIST_CHANGED, source="resource_registry")
        self.server._create_task(self.server.runtime.emit_event(event))
        self.server._create_task(self.server.notify_resource_list_changed())

    def _handle_registry_reset(self) -> None:
        """Handle registry reset."""
        event = Event(type=EventType.REGISTRY_RESET, source="resource_registry")
        self.server._create_task(self.server.runtime.emit_event(event))
        self.server._create_task(self.server.notify_resource_list_changed())


class PromptObserver:
    """Converts prompt registry events to MCP notifications."""

    def __init__(self, server: LLMLingServer) -> None:
        self.server = server
        self.events = RegistryEvents[str, BasePrompt]()
        self.events.on_item_added = self._handle_prompt_added
        self.events.on_item_modified = self._handle_prompt_modified
        self.events.on_item_removed = self._handle_prompt_removed
        self.events.on_list_changed = self._handle_prompt_list_changed
        self.events.on_reset = self._handle_registry_reset

    def _handle_prompt_added(self, key: str, prompt: BasePrompt) -> None:
        """Handle prompt addition."""
        event = Event(
            type=EventType.PROMPT_ADDED,
            source="prompt_registry",
            name=key,
            data=prompt,
        )
        self.server._create_task(self.server.runtime.emit_event(event))
        self.server._create_task(self.server.notify_prompt_list_changed())

    def _handle_prompt_modified(self, key: str, prompt: BasePrompt) -> None:
        """Handle prompt modification."""
        event = Event(
            type=EventType.PROMPT_MODIFIED,
            source="prompt_registry",
            name=key,
            data=prompt,
        )
        self.server._create_task(self.server.runtime.emit_event(event))
        self.server._create_task(self.server.notify_prompt_list_changed())

    def _handle_prompt_removed(self, key: str, prompt: BasePrompt) -> None:
        """Handle prompt removal."""
        event = Event(
            type=EventType.PROMPT_REMOVED,
            source="prompt_registry",
            name=key,
            data=prompt,
        )
        self.server._create_task(self.server.runtime.emit_event(event))
        self.server._create_task(self.server.notify_prompt_list_changed())

    def _handle_prompt_list_changed(self) -> None:
        """Handle prompt list changes."""
        event = Event(type=EventType.PROMPT_LIST_CHANGED, source="prompt_registry")
        self.server._create_task(self.server.runtime.emit_event(event))
        self.server._create_task(self.server.notify_prompt_list_changed())

    def _handle_registry_reset(self) -> None:
        """Handle registry reset."""
        event = Event(type=EventType.REGISTRY_RESET, source="prompt_registry")
        self.server._create_task(self.server.runtime.emit_event(event))
        self.server._create_task(self.server.notify_prompt_list_changed())


class ToolObserver:
    """Converts tool registry events to MCP notifications."""

    def __init__(self, server: LLMLingServer) -> None:
        self.server = server
        self.events = RegistryEvents[str, LLMCallableTool]()
        self.events.on_item_added = self._handle_tool_added
        self.events.on_item_modified = self._handle_tool_modified
        self.events.on_item_removed = self._handle_tool_removed
        self.events.on_list_changed = self._handle_tool_list_changed
        self.events.on_reset = self._handle_registry_reset

    def _handle_tool_added(self, key: str, tool: LLMCallableTool) -> None:
        """Handle tool addition."""
        event = Event(
            type=EventType.TOOL_ADDED, source="tool_registry", name=key, data=tool
        )
        self.server._create_task(self.server.runtime.emit_event(event))
        self.server._create_task(self.server.notify_tool_list_changed())

    def _handle_tool_modified(self, key: str, tool: LLMCallableTool) -> None:
        """Handle tool modification."""
        event = Event(
            type=EventType.TOOL_MODIFIED, source="tool_registry", name=key, data=tool
        )
        self.server._create_task(self.server.runtime.emit_event(event))
        self.server._create_task(self.server.notify_tool_list_changed())

    def _handle_tool_removed(self, key: str, tool: LLMCallableTool) -> None:
        """Handle tool removal."""
        event = Event(
            type=EventType.TOOL_REMOVED, source="tool_registry", name=key, data=tool
        )
        self.server._create_task(self.server.runtime.emit_event(event))
        self.server._create_task(self.server.notify_tool_list_changed())

    def _handle_tool_list_changed(self) -> None:
        """Handle tool list changes."""
        event = Event(type=EventType.TOOL_LIST_CHANGED, source="tool_registry")
        self.server._create_task(self.server.runtime.emit_event(event))
        self.server._create_task(self.server.notify_tool_list_changed())

    def _handle_registry_reset(self) -> None:
        """Handle registry reset."""
        event = Event(type=EventType.REGISTRY_RESET, source="tool_registry")
        self.server._create_task(self.server.runtime.emit_event(event))
        self.server._create_task(self.server.notify_tool_list_changed())
