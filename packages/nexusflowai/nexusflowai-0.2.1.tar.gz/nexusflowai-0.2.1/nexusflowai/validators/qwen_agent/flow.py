from copy import deepcopy

from dataclasses import dataclass

import json
from json import JSONDecodeError

import json_repair

from qwen_agent.llm.base import _postprocess_stop_words
from qwen_agent.llm.fncall_prompts.qwen_fncall_prompt import QwenFnCallPrompt
from qwen_agent.llm.function_calling import (
    validate_num_fncall_results,
    simulate_response_completion_with_chat,
)
from qwen_agent.llm.schema import Message, ContentItem, DEFAULT_SYSTEM_MESSAGE
from qwen_agent.utils.utils import format_as_text_message

from nexusflowai.types import (
    NexusflowAIChatCompletion,
    NexusflowAIChatCompletionCreateParams,
)
from nexusflowai.types.chat_completion import Choice as NexusflowAIChatCompletionChoice

from nexusflowai.validators.qwen_agent.qwen_message_translator import (
    QwenMessageTranslator,
)


@dataclass
class QwenAgentFlow:
    fncall_prompt = QwenFnCallPrompt()
    qwen_translator = QwenMessageTranslator()

    def preprocess(
        self, create_params: NexusflowAIChatCompletionCreateParams
    ) -> NexusflowAIChatCompletionCreateParams:
        if not create_params.get("tools") and not create_params.get("response_format"):
            return create_params

        create_params = deepcopy(create_params)
        messages = create_params["messages"]
        if create_params.get("response_format"):
            response_format_message = f"""Your aim is to process the given unstructured input data and return the output based on the instructions and the response_format schema provided. Provide only the raw output data in valid JSON format based on the given response_format. All values for JSON attributes should be on quotes and never give incomplete responses. Remember, your responses MUST be valid parsable JSON and MUST match the schema specified in response_format. Do not give any introduction in the front. Your response should ONLY contain the JSON
Response format: {create_params.get('response_format')}"""
            messages.insert(0, {"role": "system", "content": response_format_message})

        create_params = self.qwen_translator.convert_request_to_qwen_params(
            create_params
        )
        messages = create_params["messages"]

        if messages and messages[0].role != "system":
            messages = [
                Message(
                    role="system", content=[ContentItem(text=DEFAULT_SYSTEM_MESSAGE)]
                )
            ] + messages

        validate_num_fncall_results(messages, support_multimodal_input=False)
        messages = self.fncall_prompt.preprocess_fncall_messages(
            messages=messages,
            functions=create_params.get("tools") or [],
            lang="en",
            parallel_function_calls=create_params.get("parallel_tool_calls", True),
            function_choice=self._openai_tool_choice_to_qwen_function_choice(
                create_params
            ),
        )

        messages = [
            format_as_text_message(msg, add_upload_info=False) for msg in messages
        ]
        messages = simulate_response_completion_with_chat(messages)

        create_params["messages"] = [m.model_dump() for m in messages]

        create_params["stop"] = self.qwen_translator.adjust_stop_words_for_qwen_agent(
            create_params.get("stop", [])
        )

        create_params.pop("tools", None)
        create_params.pop("tool_choice", None)
        create_params.pop("parallel_tool_calls", None)

        return create_params

    @staticmethod
    def _openai_tool_choice_to_qwen_function_choice(
        create_params: NexusflowAIChatCompletionCreateParams,
    ) -> str:
        function_choice = create_params.get("tool_choice", "auto")
        if isinstance(function_choice, dict):
            function_choice = function_choice["function"]["name"]

        return function_choice

    def postprocess(
        self,
        create_params: NexusflowAIChatCompletionCreateParams,
        response: NexusflowAIChatCompletion,
    ) -> NexusflowAIChatCompletion:
        if not create_params.get("tools") and not create_params.get("response_format"):
            return response

        content = response.choices[0].message.content

        if create_params.get("response_format"):
            try:
                content = json.dumps(json_repair.loads(content))
            except JSONDecodeError:
                pass

        response_message = Message(
            role="assistant",
            content=[ContentItem(text=content)],
        )

        processed_messages = _postprocess_stop_words(
            messages=[response_message],
            stop=self.qwen_translator.adjust_stop_words_for_qwen_agent(
                create_params.get("stop", [])
            ),
        )

        messages = self.fncall_prompt.postprocess_fncall_messages(
            messages=processed_messages,
            parallel_function_calls=create_params.get("parallel_tool_calls", True),
            function_choice=self._openai_tool_choice_to_qwen_function_choice(
                create_params
            ),
        )
        chat_completion_message = (
            self.qwen_translator.convert_qwen_messages_to_openai_message(
                messages=messages,
                tools=create_params.get("tools"),
                tool_choice=create_params.get("tool_choice"),
            )
        )

        return NexusflowAIChatCompletion(
            id=response.id,
            choices=[
                NexusflowAIChatCompletionChoice(
                    finish_reason="tool_calls",
                    index=0,
                    message=chat_completion_message,
                )
            ],
            created=response.created,
            model=response.model,
            object="chat.completion",
            system_fingerprint=None,
            usage=response.usage,
        )
