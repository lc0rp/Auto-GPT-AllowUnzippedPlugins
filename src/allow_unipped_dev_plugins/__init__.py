import abc
import importlib
import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Tuple, TypeVar, TypedDict
from auto_gpt_plugin_template import AutoGPTPluginTemplate

PromptGenerator = TypeVar("PromptGenerator")


class Message(TypedDict):
    role: str
    content: str


def instantiate_plugin_class(module_path, class_name):
    module = importlib.import_module(module_path)
    plugin_class = getattr(module, class_name)
    print(f"Module: {module} Plugin class: {plugin_class}")
    instance = plugin_class()
    return instance


class AutoGPTAllowUnzippedPlugins(AutoGPTPluginTemplate):
    """
    This plugin allows developers to use unzipped plugins simplifying the plugin development process.
    """

    def __init__(self):
        super().__init__()
        self._name = "Auto-GPT-Allow-Unzipped-Plugins"
        self._version = "0.1.0"
        self._description = "This plugin allows developers to use unzipped plugins simplifying the plugin development process."
        
        self._plugins = self.load_unzipped_plugins()


    def load_unzipped_plugins(self):
        # Search for plugins in the plugins directory.
        # The plugins directory is three levels up from this file.
        unzipped_plugins = []
        from autogpt.config.config import Config
        cfg = Config()
        plugins_dir = Path(cfg.plugins_dir)
        
        # Find all dirs that contain a __init__.py file.
        for path in plugins_dir.rglob("__init__.py"):
            if "AllowUnzippedPlugins" in str(path):
                continue
            
            print(f"Found module '{path.name}' at: {path}")
            
            spec = importlib.util.spec_from_file_location(path.parent.name, str(path))
            loaded_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(loaded_module)
            sys.modules[path.parent.name] = loaded_module
            
            for key in dir(loaded_module):
                    if key.startswith("__"):
                        continue
                    a_module = getattr(loaded_module, key)
                    a_keys = dir(a_module)
                    if (
                        "_abc_impl" in a_keys
                        and a_module.__name__ != "AutoGPTPluginTemplate"
                    ):
                        unzipped_plugins.append(a_module())
        
        return unzipped_plugins
    
    def _can_handle(self, method):
        can_handle_method = f"can_handle_{method}"
        return any(hasattr(plugin, can_handle_method) and getattr(plugin, can_handle_method)() for plugin in self._plugins)
    
    def can_handle_on_response(self) -> bool:
        return self._can_handle("on_response")

    def on_response(self, response: str, *args, **kwargs) -> str:
        for plugin in self._plugins:
            if not plugin.can_handle_on_response():
                continue
            response = plugin.on_response(response, *args, **kwargs)
        return response

    def can_handle_post_prompt(self) -> bool:
        return self._can_handle("post_prompt")

    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        for plugin in self._plugins:
            if not plugin.can_handle_post_prompt():
                continue
            prompt = plugin.post_prompt(prompt)
        return prompt

    def can_handle_on_planning(self) -> bool:
        """On Planning is not supported by this plugin."""
        return False

    def on_planning(
        self, prompt: PromptGenerator, messages: List[Message]
    ) -> Optional[str]:
        pass  
    
    def can_handle_post_planning(self) -> bool:
        return self._can_handle("post_planning")

    def post_planning(self, response: str) -> str:
        for plugin in self._plugins:
            if not plugin.can_handle_post_planning():
                continue
            response = plugin.post_planning(response)
        return response

    def can_handle_pre_instruction(self) -> bool:
        return self._can_handle("pre_instruction")

    def pre_instruction(self, messages: List[Message]) -> List[Message]:
        for plugin in self._plugins:
            if not plugin.can_handle_pre_instruction():
                continue
            if plugin_messages := plugin.pre_instruction(messages):
                messages.extend(iter(plugin_messages))
        return messages

    def can_handle_on_instruction(self) -> bool:
        return self._can_handle("on_instruction")

    def on_instruction(self, messages: List[Message]) -> Optional[str]:
        for plugin in self._plugins:
            if not plugin.can_handle_on_instruction():
                continue
            if plugin_result := plugin.on_instruction(messages):
                sep = "\n" if i else ""
                plugins_reply = f"{plugins_reply}{sep}{plugin_result}"
        return plugins_reply

    def can_handle_post_instruction(self) -> bool:
        return self._can_handle("post_instruction")

    def post_instruction(self, response: str) -> str:
        for plugin in self._plugins:
            if not plugin.can_handle_post_instruction():
                continue
            response = plugin.post_instruction(response)
        return response

    def can_handle_pre_command(self) -> bool:
        return self._can_handle("pre_command")
    
    def pre_command(
        self, command_name: str, arguments: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        for plugin in self._plugins:
            if not plugin.can_handle_pre_command():
                continue
            command_name, arguments = plugin.pre_command(
                command_name, arguments
            )
        return command_name, arguments

    def can_handle_post_command(self) -> bool:
        return self._can_handle("post_command")

    def post_command(self, command_name: str, response: str) -> str:
        for plugin in self._plugins:
            if not plugin.can_handle_post_command():
                continue
            result = plugin.post_command(command_name, result)
        return result

    def can_handle_chat_completion(
        self, messages: Dict[Any, Any], model: str, temperature: float, max_tokens: int
    ) -> bool:
        """Not supported by this plugin."""
        return False

    def handle_chat_completion(
        self, messages: List[Message], model: str, temperature: float, max_tokens: int
    ) -> str:
        pass