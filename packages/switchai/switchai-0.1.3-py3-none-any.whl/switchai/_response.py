from dataclasses import dataclass
from typing import List


@dataclass
class Function:
    name: str
    arguments: dict


@dataclass
class ChatMessage:
    role: str
    content: str


@dataclass
class ChatToolCall:
    id: str | None
    function: Function
    type: str = "function"


@dataclass
class ChatChoice:
    index: int
    message: ChatMessage
    finish_reason: str
    tool_calls: List[ChatToolCall] = None


@dataclass
class ChatUsage:
    input_tokens: int
    output_tokens: int
    total_tokens: int


@dataclass
class ChatResponse:
    id: str
    object: str
    model: str
    usage: ChatUsage
    choices: List[ChatChoice]

    def __repr__(self):
        return f"ChatResponse(id={self.id}, object={self.object}, model={self.model}, usage={self.usage}, choices={self.choices})"


class OpenAIChatResponseAdapter(ChatResponse):
    def __init__(self, response):
        super().__init__(
            id=response.id,
            object=response.object,
            model=response.model,
            usage=ChatUsage(
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            ),
            choices=[
                ChatChoice(
                    index=choice.index,
                    message=ChatMessage(role=choice.message.role, content=choice.message.content),
                    tool_calls=[
                        ChatToolCall(
                            id=tool.id, function=Function(name=tool.function.name, arguments=tool.function.arguments)
                        )
                        for tool in choice.message.tool_calls
                    ]
                    if choice.message.tool_calls is not None
                    else None,
                    finish_reason=choice.finish_reason,
                )
                for choice in response.choices
            ],
        )


class MistralChatResponseAdapter(ChatResponse):
    def __init__(self, response):
        super().__init__(
            id=response.id,
            object=response.object,
            model=response.model,
            usage=ChatUsage(
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            ),
            choices=[
                ChatChoice(
                    index=choice.index,
                    message=ChatMessage(role=choice.message.role, content=choice.message.content),
                    tool_calls=[
                        ChatToolCall(
                            id=tool.id, function=Function(name=tool.function.name, arguments=tool.function.arguments)
                        )
                        for tool in choice.message.tool_calls
                    ]
                    if choice.message.tool_calls is not None
                    else None,
                    finish_reason=choice.finish_reason,
                )
                for choice in response.choices
            ],
        )


class AnthropicChatResponseAdapter(ChatResponse):
    def __init__(self, response):
        super().__init__(
            id=response.id,
            object=None,
            model=response.model,
            usage=ChatUsage(
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
                total_tokens=response.usage.input_tokens + response.usage.output_tokens,
            ),
            choices=[
                ChatChoice(
                    index=0,
                    message=ChatMessage(role=response.role, content=response.content[0].text),
                    tool_calls=[
                        ChatToolCall(
                            id=response.content[1].id,
                            function=Function(name=response.content[1].name, arguments=response.content[1].input),
                        )
                    ]
                    if len(response.content) > 1
                    else None,
                    finish_reason=response.stop_reason,
                )
            ],
        )


class GoogleChatResponseAdapter(ChatResponse):
    def __init__(self, response):
        super().__init__(
            id=None,
            object=None,
            model=None,
            usage=ChatUsage(
                input_tokens=response.usage_metadata.prompt_token_count,
                output_tokens=response.usage_metadata.candidates_token_count,
                total_tokens=response.usage_metadata.total_token_count,
            ),
            choices=[
                ChatChoice(
                    index=choice.index,
                    message=ChatMessage(role="assistant", content=choice.content.parts[0].text),
                    tool_calls=[
                        ChatToolCall(
                            id=None,
                            function=Function(name=part.function_call.name, arguments=dict(part.function_call.args)),
                        )
                        for part in choice.content.parts
                        if "function_call" in part
                    ],
                    finish_reason=choice.finish_reason.name.lower(),
                )
                for choice in response.candidates
            ],
        )


@dataclass
class Embedding:
    index: int
    data: List[float]


@dataclass
class EmbeddingUsage:
    input_tokens: int | None
    total_tokens: int | None


@dataclass
class EmbeddingResponse:
    id: str
    object: str
    model: str
    usage: EmbeddingUsage
    embeddings: List[Embedding]

    def __repr__(self):
        return f"EmbeddingResponse(id={self.id}, object={self.object}, model={self.model}, usage={self.usage}, embeddings={self.embeddings})"


class OpenAIEmbeddingResponseAdapter(EmbeddingResponse):
    def __init__(self, response):
        super().__init__(
            id=None,
            object=response.object,
            model=response.model,
            usage=EmbeddingUsage(
                input_tokens=response.usage.prompt_tokens,
                total_tokens=response.usage.total_tokens,
            ),
            embeddings=[
                Embedding(
                    index=embedding.index,
                    data=embedding.embedding,
                )
                for embedding in response.data
            ],
        )


class MistralEmbeddingResponseAdapter(EmbeddingResponse):
    def __init__(self, response):
        super().__init__(
            id=response.id,
            object=response.object,
            model=response.model,
            usage=EmbeddingUsage(
                input_tokens=response.usage.prompt_tokens,
                total_tokens=response.usage.total_tokens,
            ),
            embeddings=[
                Embedding(
                    index=embedding.index,
                    data=embedding.embedding,
                )
                for embedding in response.data
            ],
        )


class GoogleEmbeddingResponseAdapter(EmbeddingResponse):
    def __init__(self, response):
        super().__init__(
            id=None,
            object=None,
            model=None,
            usage=EmbeddingUsage(
                input_tokens=None,
                total_tokens=None,
            ),
            embeddings=[
                Embedding(
                    index=index,
                    data=data,
                )
                for index, data in enumerate(response["embedding"])
            ],
        )
