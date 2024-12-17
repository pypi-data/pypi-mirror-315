from typing import List, Any, Dict, Union, Optional

from dataclasses import dataclass

import json

from openai.types.chat import ChatCompletionToolParam
from openai.types.chat.chat_completion_tool_choice_option_param import (
    ChatCompletionNamedToolChoiceParam,
)

from qwen_agent.llm.schema import Message, FunctionCall, ContentItem
from qwen_agent.llm.fncall_prompts.qwen_fncall_prompt import FN_STOP_WORDS

from nexusflowai.types import (
    NexusflowAIChatCompletion,
    NexusflowAIChatCompletionMessage,
)
from nexusflowai.validators.base_input_validator import BOT_END

from nexusflowai.validators.create_with_tools.postprocess import (
    FunctionCallResponseTranslator,
    RavenFunctionCall,
)


@dataclass
class QwenMessageTranslator:
    def convert_request_to_qwen_params(
        self,
        request_dict: NexusflowAIChatCompletion,
    ) -> Dict[str, Any]:
        qwen_messages = []
        # pylint: disable=too-many-nested-blocks
        for turn, m in enumerate(request_dict["messages"]):
            if m["role"] == "tool":
                content = self._format_content_parts(m["content"])
                msg = {
                    "role": "function",
                    "content": content,
                }
                assert "tool_call_id" in m
                f = False
                for prev_turn in reversed(range(turn)):
                    if f:
                        break
                    if (
                        request_dict["messages"][prev_turn]["role"] == "assistant"
                        and "tool_calls" in request_dict["messages"][prev_turn]
                        and request_dict["messages"][prev_turn]["tool_calls"]
                        is not None
                    ):
                        for t in request_dict["messages"][prev_turn]["tool_calls"]:
                            if f:
                                break
                            if m["tool_call_id"] == t["id"]:
                                msg["name"] = t["function"]["name"]
                                f = True
                                break
                qwen_messages.append(Message(**msg))
            elif (
                m["role"] == "assistant"
                and "tool_calls" in m
                and m["tool_calls"] is not None
            ):
                for t in m["tool_calls"]:
                    content = self._format_content_parts(m["content"])
                    qwen_messages.append(
                        Message(
                            role=m["role"],
                            content=content,
                            function_call=FunctionCall(
                                name=t["function"]["name"],
                                arguments=t["function"]["arguments"],
                            ),
                        )
                    )
            else:
                content = self._format_content_parts(m["content"])
                qwen_messages.append(Message(role=m["role"], content=content))
        qwen_functions = (
            [self._format_function(t["function"]) for t in request_dict["tools"]]
            if request_dict.get("tools") is not None
            else None
        )

        request_dict["messages"] = qwen_messages
        request_dict["tools"] = qwen_functions

        return request_dict

    def _format_content_parts(
        self, content: Optional[Union[str, List[Dict[str, Any]]]]
    ) -> List[ContentItem]:
        """Format content str or ContentPartParams"""
        if not content:
            return None
        elif isinstance(content, str):
            return [ContentItem(text=content)]
        elif isinstance(content, list):
            contents = []
            for content_part in content:
                if "text" not in content_part:
                    raise NotImplementedError
                contents.append(ContentItem(text=content_part["text"]))
            return contents
        else:
            raise NotImplementedError

    def _format_function(self, function_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Format functions to be presentable to Qwen-Agent."""

        if "description" not in function_dict:
            # https://github.com/QwenLM/Qwen-Agent/blob/8fe8f09c2f43f768f334e7a9244b64d89fcb088b/qwen_agent/llm/fncall_prompts/qwen_fncall_prompt.py#L348
            function_dict["description"] = ""

        return function_dict

    def convert_qwen_messages_to_openai_message(
        self,
        messages: List[Message],
        tools: List[ChatCompletionToolParam],
        tool_choice: ChatCompletionNamedToolChoiceParam | None = None,
    ) -> NexusflowAIChatCompletionMessage:
        fcrt = FunctionCallResponseTranslator()

        contents = []

        tool_calls = []
        for message in messages:
            message_content = message.content
            if isinstance(message_content, list):
                message_content = "\n".join([m.text for m in message_content])

            function_call = message.function_call
            if function_call:
                message_content = ""

                fc_dict = function_call.model_dump(mode="json")
                raven_fc = RavenFunctionCall.from_tool_call({"function": fc_dict})
                raven_tool_calls, _, _ = fcrt.raw_response_to_tool_calls(
                    tools=tools, raw_response=repr(raven_fc), tool_choice=tool_choice
                )

                # We only take the first item since we know it's only one tool call.
                if raven_tool_calls:
                    tool_calls.append(raven_tool_calls[0])
                else:
                    fc_dict_to_output = {
                        "name": raven_fc.name,
                        "arguments": json.dumps(raven_fc.kwargs),
                    }
                    tool_calls.append(fcrt.create_tool_call(fc_dict_to_output))

            contents.append(message_content)

        tool_calls = tool_calls or None
        content = "".join(contents) or None

        return NexusflowAIChatCompletionMessage(
            content=content, role="assistant", tool_calls=tool_calls
        )

    def adjust_stop_words_for_qwen_agent(self, stop: List[str]) -> List[str]:
        if BOT_END in stop:
            stop.remove(BOT_END)
        stop = stop + [x for x in FN_STOP_WORDS if x not in stop]
        return stop
