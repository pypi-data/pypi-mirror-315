import json
from dataclasses import dataclass, field
from typing import Optional, List, Iterator, Dict, Any, Union, Callable

from phi.model.base import Model
from phi.model.message import Message
from phi.model.response import ModelResponse
from phi.tools.function import Function, FunctionCall
from phi.tools import Tool, Toolkit
from phi.utils.log import logger
from phi.utils.timer import Timer
from phi.utils.tools import get_function_call_for_tool_call

try:
    import google.generativeai as genai
    from google.generativeai import GenerativeModel
    from google.generativeai.types.generation_types import GenerateContentResponse
    from google.generativeai.types.content_types import FunctionDeclaration, Tool as GeminiTool
    from google.ai.generativelanguage_v1beta.types.generative_service import (
        GenerateContentResponse as ResultGenerateContentResponse,
    )
    from google.protobuf.struct_pb2 import Struct
except ImportError:
    logger.error("`google-generativeai` not installed. Please install it using `pip install google-generativeai`")
    raise


@dataclass
class MessageData:
    response_content: str = ""
    response_block: Optional[GenerateContentResponse] = None
    response_role: Optional[str] = None
    response_parts: Optional[List] = None
    valid_response_parts: Optional[List] = None
    response_tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    response_usage: Optional[ResultGenerateContentResponse] = None


@dataclass
class Metrics:
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    time_to_first_token: Optional[float] = None
    response_timer: Timer = field(default_factory=Timer)

    def log(self):
        logger.debug("**************** METRICS START ****************")
        if self.time_to_first_token is not None:
            logger.debug(f"* Time to first token:         {self.time_to_first_token:.4f}s")
        logger.debug(f"* Time to generate response:   {self.response_timer.elapsed:.4f}s")
        logger.debug(f"* Tokens per second:           {self.output_tokens / self.response_timer.elapsed:.4f} tokens/s")
        logger.debug(f"* Input tokens:                {self.input_tokens}")
        logger.debug(f"* Output tokens:               {self.output_tokens}")
        logger.debug(f"* Total tokens:                {self.total_tokens}")
        logger.debug("**************** METRICS END ******************")


class Gemini(Model):
    """
    Gemini model class for Google's Generative AI models.

    Attributes:
        id (str): Model ID. Default is `gemini-2.0-flash-exp`.
        name (str): The name of this chat model instance. Default is `Gemini`.
        provider (str): Model provider. Default is `Google`.
        function_declarations (List[FunctionDeclaration]): List of function declarations.
        generation_config (Any): Generation configuration.
        safety_settings (Any): Safety settings.
        generative_model_kwargs (Dict[str, Any]): Generative model keyword arguments.
        api_key (str): API key.
        client (GenerativeModel): Generative model client.
    """

    id: str = "gemini-2.0-flash-exp"
    name: str = "Gemini"
    provider: str = "Google"

    # Request parameters
    function_declarations: Optional[List[FunctionDeclaration]] = None
    generation_config: Optional[Any] = None
    safety_settings: Optional[Any] = None
    generative_model_kwargs: Optional[Dict[str, Any]] = None

    # Client parameters
    api_key: Optional[str] = None
    client_params: Optional[Dict[str, Any]] = None

    # Gemini client
    client: Optional[GenerativeModel] = None

    def get_client(self) -> GenerativeModel:
        """
        Returns an instance of the GenerativeModel client.

        Returns:
            GenerativeModel: The GenerativeModel client.
        """
        if self.client:
            return self.client

        client_params: Dict[str, Any] = {}
        # Set client parameters if they are provided
        if self.api_key:
            client_params["api_key"] = self.api_key
        if self.client_params:
            client_params.update(self.client_params)
        genai.configure(**client_params)
        return genai.GenerativeModel(model_name=self.id, **self.request_kwargs)

    @property
    def request_kwargs(self) -> Dict[str, Any]:
        """
        Returns the request keyword arguments for the GenerativeModel client.

        Returns:
            Dict[str, Any]: The request keyword arguments.
        """
        request_params: Dict[str, Any] = {}
        if self.generation_config:
            request_params["generation_config"] = self.generation_config
        if self.safety_settings:
            request_params["safety_settings"] = self.safety_settings
        if self.generative_model_kwargs:
            request_params.update(self.generative_model_kwargs)
        if self.function_declarations:
            request_params["tools"] = [GeminiTool(function_declarations=self.function_declarations)]
        return request_params

    def format_messages(self, messages: List[Message]) -> List[Dict[str, Any]]:
        """
        Converts a list of Message objects to the Gemini-compatible format.

        Args:
            messages (List[Message]): The list of messages to convert.

        Returns:
            List[Dict[str, Any]]: The formatted_messages list of messages.
        """
        formatted_messages: List = []
        for message in messages:
            message_for_model = {}

            # Add role to the message for the model
            role = "model" if message.role == "system" else "user" if message.role == "tool" else message.role
            message_for_model["role"] = role

            # Add content to the message for the model
            content = message.content
            if not content or message.role in ["tool", "model"]:
                parts = message.parts  # type: ignore
            else:
                if isinstance(content, str):
                    parts = [content]
                elif isinstance(content, list):
                    parts = content
                else:
                    parts = [" "]
            message_for_model["parts"] = parts

            # Add images to the message for the model
            if message.images is not None and message.role == "user":
                for image in message.images:
                    if isinstance(image, str):
                        # Case 1: Image is a URL
                        if image.startswith("http://") or image.startswith("https://"):
                            try:
                                import httpx
                                import base64

                                image_content = httpx.get(image).content
                                image_data = {
                                    "mime_type": "image/jpeg",
                                    "data": base64.b64encode(image_content).decode("utf-8"),
                                }
                                message_for_model["parts"].append(image_data)  # type: ignore
                            except Exception as e:
                                logger.warning(f"Failed to download image from {image}: {e}")
                                continue
                        # Case 2: Image is a path
                        else:
                            try:
                                from os.path import exists, isfile
                                import PIL.Image
                            except ImportError:
                                logger.error("`PIL.Image not installed. Please install it using 'pip install pillow'`")
                                raise

                            try:
                                if exists(image) and isfile(image):
                                    image_data = PIL.Image.open(image)  # type: ignore
                                else:
                                    logger.error(f"Image file {image} does not exist.")
                                    raise
                                message_for_model["parts"].append(image_data)  # type: ignore
                            except Exception as e:
                                logger.warning(f"Failed to load image from {image}: {e}")
                                continue

                    elif isinstance(image, bytes):
                        image_data = {"mime_type": "image/jpeg", "data": base64.b64encode(image).decode("utf-8")}
                        message_for_model["parts"].append(image_data)

            if message.videos is not None and message.role == "user":
                try:
                    for video in message.videos:
                        import time
                        from os.path import exists, isfile

                        video_file = None
                        if exists(video) and isfile(video):  # type: ignore
                            video_file = genai.upload_file(path=video)
                        else:
                            logger.error(f"Video file {video} does not exist.")
                            raise

                        # Check whether the file is ready to be used.
                        while video_file.state.name == "PROCESSING":
                            time.sleep(10)
                            video_file = genai.get_file(video_file.name)

                        if video_file.state.name == "FAILED":
                            raise ValueError(video_file.state.name)

                        message_for_model["parts"].insert(0, video_file)  # type: ignore

                except Exception as e:
                    logger.warning(f"Failed to load video from {message.videos}: {e}")
                    continue

            if message.audio is not None and message.role == "user":
                try:
                    from pathlib import Path
                    from os.path import exists, isfile

                    audio = message.audio.get("data")
                    if audio:
                        audio_file = None
                        if exists(audio) and isfile(audio):
                            audio_file = {"mime_type": "audio/mp3", "data": Path(audio).read_bytes()}
                        else:
                            logger.error(f"Audio file {audio} does not exist.")
                            raise
                        message_for_model["parts"].insert(0, audio_file)  # type: ignore

                except Exception as e:
                    logger.warning(f"Failed to load video from {message.videos}: {e}")
                    continue

            formatted_messages.append(message_for_model)
        return formatted_messages

    def format_functions(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts function parameters to a Gemini-compatible format.

        Args:
            params (Dict[str, Any]): The original parameters dictionary.

        Returns:
            Dict[str, Any]: The converted parameters dictionary compatible with Gemini.
        """
        formatted_params = {}
        for key, value in params.items():
            if key == "properties" and isinstance(value, dict):
                converted_properties = {}
                for prop_key, prop_value in value.items():
                    property_type = prop_value.get("type")
                    if isinstance(property_type, list):
                        # Create a copy to avoid modifying the original list
                        non_null_types = [t for t in property_type if t != "null"]
                        if non_null_types:
                            # Use the first non-null type
                            converted_type = non_null_types[0]
                        else:
                            # Default type if all types are 'null'
                            converted_type = "string"
                    else:
                        converted_type = property_type

                    converted_properties[prop_key] = {"type": converted_type}
                formatted_params[key] = converted_properties
            else:
                formatted_params[key] = value
        return formatted_params

    def add_tool(
        self,
        tool: Union["Tool", "Toolkit", Callable, dict, "Function"],
        strict: bool = False,
        agent: Optional[Any] = None,
    ) -> None:
        """
        Adds tools to the model.

        Args:
            tool: The tool to add. Can be a Tool, Toolkit, Callable, dict, or Function.
        """
        if self.function_declarations is None:
            self.function_declarations = []

        # If the tool is a Tool or Dict, log a warning.
        if isinstance(tool, Tool) or isinstance(tool, Dict):
            logger.warning("Tool of type 'Tool' or 'dict' is not yet supported by Gemini.")

        # If the tool is a Callable or Toolkit, add its functions to the Model
        elif callable(tool) or isinstance(tool, Toolkit) or isinstance(tool, Function):
            if self.functions is None:
                self.functions = {}

            if isinstance(tool, Toolkit):
                # For each function in the toolkit, process entrypoint and add to self.tools
                for name, func in tool.functions.items():
                    # If the function does not exist in self.functions, add to self.tools
                    if name not in self.functions:
                        func._agent = agent
                        func.process_entrypoint()
                        self.functions[name] = func
                        function_declaration = FunctionDeclaration(
                            name=func.name,
                            description=func.description,
                            parameters=self.format_functions(func.parameters),
                        )
                        self.function_declarations.append(function_declaration)
                        logger.debug(f"Function {name} from {tool.name} added to model.")

            elif isinstance(tool, Function):
                if tool.name not in self.functions:
                    tool._agent = agent
                    tool.process_entrypoint()
                    self.functions[tool.name] = tool
                    function_declaration = FunctionDeclaration(
                        name=tool.name,
                        description=tool.description,
                        parameters=self.format_functions(tool.parameters),
                    )
                    self.function_declarations.append(function_declaration)
                    logger.debug(f"Function {tool.name} added to model.")

            elif callable(tool):
                try:
                    function_name = tool.__name__
                    if function_name not in self.functions:
                        func = Function.from_callable(tool)
                        self.functions[func.name] = func
                        function_declaration = FunctionDeclaration(
                            name=func.name,
                            description=func.description,
                            parameters=self.format_functions(func.parameters),
                        )
                        self.function_declarations.append(function_declaration)
                        logger.debug(f"Function '{func.name}' added to model.")
                except Exception as e:
                    logger.warning(f"Could not add function {tool}: {e}")

    def invoke(self, messages: List[Message]):
        """
        Invokes the model with a list of messages and returns the response.

        Args:
            messages (List[Message]): The list of messages to send to the model.

        Returns:
            GenerateContentResponse: The response from the model.
        """
        return self.get_client().generate_content(contents=self.format_messages(messages))

    def invoke_stream(self, messages: List[Message]):
        """
        Invokes the model with a list of messages and returns the response as a stream.

        Args:
            messages (List[Message]): The list of messages to send to the model.

        Returns:
            Iterator[GenerateContentResponse]: The response from the model as a stream.
        """
        yield from self.get_client().generate_content(
            contents=self.format_messages(messages),
            stream=True,
        )

    def update_usage_metrics(
        self,
        assistant_message: Message,
        usage: Optional[ResultGenerateContentResponse] = None,
        metrics: Metrics = Metrics(),
    ) -> None:
        """
        Update the usage metrics.

        Args:
            assistant_message (Message): The assistant message.
            usage (ResultGenerateContentResponse): The usage metrics.
            stream_usage (Optional[StreamUsageData]): The stream usage metrics.
        """
        assistant_message.metrics["time"] = metrics.response_timer.elapsed
        self.metrics.setdefault("response_times", []).append(metrics.response_timer.elapsed)
        if usage:
            metrics.input_tokens = usage.prompt_token_count or 0
            metrics.output_tokens = usage.candidates_token_count or 0
            metrics.total_tokens = usage.total_token_count or 0

            if metrics.input_tokens is not None:
                assistant_message.metrics["input_tokens"] = metrics.input_tokens
                self.metrics["input_tokens"] = self.metrics.get("input_tokens", 0) + metrics.input_tokens
            if metrics.output_tokens is not None:
                assistant_message.metrics["output_tokens"] = metrics.output_tokens
                self.metrics["output_tokens"] = self.metrics.get("output_tokens", 0) + metrics.output_tokens
            if metrics.total_tokens is not None:
                assistant_message.metrics["total_tokens"] = metrics.total_tokens
                self.metrics["total_tokens"] = self.metrics.get("total_tokens", 0) + metrics.total_tokens
            if metrics.time_to_first_token is not None:
                assistant_message.metrics["time_to_first_token"] = metrics.time_to_first_token
                self.metrics["time_to_first_token"] = metrics.time_to_first_token

    def create_assistant_message(self, response: GenerateContentResponse, metrics: Metrics) -> Message:
        """
        Create an assistant message from the response.

        Args:
            response (GenerateContentResponse): The model response.
            response_timer (Timer): The response timer.

        Returns:
            Message: The assistant message.
        """
        message_data = MessageData()

        message_data.response_block = response.candidates[0].content
        message_data.response_role = message_data.response_block.role
        message_data.response_parts = message_data.response_block.parts
        message_data.response_usage = response.usage_metadata

        if message_data.response_parts is not None:
            for part in message_data.response_parts:
                part_dict = type(part).to_dict(part)

                # Extract text if present
                if "text" in part_dict:
                    message_data.response_content = part_dict.get("text")

                # Parse function calls
                if "function_call" in part_dict:
                    message_data.response_tool_calls.append(
                        {
                            "type": "function",
                            "function": {
                                "name": part_dict.get("function_call").get("name"),
                                "arguments": json.dumps(part_dict.get("function_call").get("args")),
                            },
                        }
                    )

        # -*- Create assistant message
        assistant_message = Message(
            role=message_data.response_role or "model",
            content=message_data.response_content,
            parts=message_data.response_parts,
        )

        # -*- Update assistant message if tool calls are present
        if len(message_data.response_tool_calls) > 0:
            assistant_message.tool_calls = message_data.response_tool_calls

        # -*- Update usage metrics
        self.update_usage_metrics(assistant_message, message_data.response_usage, metrics)
        return assistant_message

    def get_function_calls_to_run(
        self,
        assistant_message: Message,
        messages: List[Message],
    ) -> List[FunctionCall]:
        """
        Extracts and validates function calls from the assistant message.

        Args:
            assistant_message (Message): The assistant message containing tool calls.
            messages (List[Message]): The list of conversation messages.

        Returns:
            List[FunctionCall]: A list of valid function calls to run.
        """
        function_calls_to_run: List[FunctionCall] = []
        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                _function_call = get_function_call_for_tool_call(tool_call, self.functions)
                if _function_call is None:
                    messages.append(Message(role="tool", content="Could not find function to call."))
                    continue
                if _function_call.error is not None:
                    messages.append(Message(role="tool", content=_function_call.error))
                    continue
                function_calls_to_run.append(_function_call)
        return function_calls_to_run

    def format_function_call_results(
        self,
        function_call_results: List[Message],
        messages: List[Message],
    ):
        """
        Processes the results of function calls and appends them to messages.

        Args:
            function_call_results (List[Message]): The results from running function calls.
            messages (List[Message]): The list of conversation messages.
        """
        if function_call_results:
            combined_content: List = []
            combined_parts: List = []

            for result in function_call_results:
                s = Struct()
                s.update({"result": [result.content]})
                function_response = genai.protos.Part(
                    function_response=genai.protos.FunctionResponse(name=result.tool_name, response=s)
                )
                combined_content.append(result.content)
                combined_parts.append(function_response)
            messages.append(Message(role="tool", content=combined_content, parts=combined_parts))

    def handle_tool_calls(self, assistant_message: Message, messages: List[Message], model_response: ModelResponse):
        """
        Handle tool calls in the assistant message.

        Args:
            assistant_message (Message): The assistant message.
            messages (List[Message]): A list of messages.
            model_response (ModelResponse): The model response.

        Returns:
            Optional[ModelResponse]: The updated model response.
        """
        if assistant_message.tool_calls and self.run_tools:
            model_response.content = assistant_message.get_content_string() or ""
            function_calls_to_run = self.get_function_calls_to_run(assistant_message, messages)

            if self.show_tool_calls:
                if len(function_calls_to_run) == 1:
                    model_response.content += f"\n - Running: {function_calls_to_run[0].get_call_str()}\n\n"
                elif len(function_calls_to_run) > 1:
                    model_response.content += "\nRunning:"
                    for _f in function_calls_to_run:
                        model_response.content += f"\n - {_f.get_call_str()}"
                    model_response.content += "\n\n"

            function_call_results: List[Message] = []
            for _ in self.run_function_calls(
                function_calls=function_calls_to_run,
                function_call_results=function_call_results,
            ):
                pass

            self.format_function_call_results(function_call_results, messages)

            return model_response
        return None

    def response(self, messages: List[Message]) -> ModelResponse:
        """
        Send a generate cone content request to the model and return the response.

        Args:
            messages (List[Message]): The list of messages to send to the model.

        Returns:
            ModelResponse: The model response.
        """
        logger.debug("---------- Gemini Response Start ----------")
        self._log_messages(messages)
        model_response = ModelResponse()
        metrics = Metrics()

        # -*- Generate response
        metrics.response_timer.start()
        response: GenerateContentResponse = self.invoke(messages=messages)
        metrics.response_timer.stop()

        # -*- Create assistant message
        assistant_message = self.create_assistant_message(response=response, metrics=metrics)

        # -*- Add assistant message to messages
        messages.append(assistant_message)

        # -*- Log response and metrics
        assistant_message.log()
        metrics.log()

        # -*- Update model response with assistant message content
        if assistant_message.content is not None:
            model_response.content = assistant_message.get_content_string()

        # -*- Handle tool calls
        if self.handle_tool_calls(assistant_message, messages, model_response) is not None:
            response_after_tool_calls = self.response(messages=messages)
            if response_after_tool_calls.content is not None:
                if model_response.content is None:
                    model_response.content = ""
                model_response.content += response_after_tool_calls.content
            return model_response

        # -*- Remove parts from messages
        # for m in messages:
        #     if hasattr(m, "parts"):
        #         m.parts = None
        logger.debug("---------- Gemini Response End ----------")
        return model_response

    def handle_stream_tool_calls(self, assistant_message: Message, messages: List[Message]):
        """
        Parse and run function calls and append the results to messages.

        Args:
            assistant_message (Message): The assistant message containing tool calls.
            messages (List[Message]): The list of conversation messages.

        Yields:
            Iterator[ModelResponse]: Yields model responses during function execution.
        """
        if assistant_message.tool_calls and self.run_tools:
            function_calls_to_run = self.get_function_calls_to_run(assistant_message, messages)

            if self.show_tool_calls:
                if len(function_calls_to_run) == 1:
                    yield ModelResponse(content=f"\n - Running: {function_calls_to_run[0].get_call_str()}\n\n")
                elif len(function_calls_to_run) > 1:
                    yield ModelResponse(content="\nRunning:")
                    for _f in function_calls_to_run:
                        yield ModelResponse(content=f"\n - {_f.get_call_str()}")
                    yield ModelResponse(content="\n\n")

            function_call_results: List[Message] = []
            for intermediate_model_response in self.run_function_calls(
                function_calls=function_calls_to_run, function_call_results=function_call_results
            ):
                yield intermediate_model_response

            self.format_function_call_results(function_call_results, messages)

    def response_stream(self, messages: List[Message]) -> Iterator[ModelResponse]:
        """
        Send a generate content request to the model and return the response as a stream.

        Args:
            messages (List[Message]): The list of messages to send to the model.

        Yields:
            Iterator[ModelResponse]: The model responses
        """
        logger.debug("---------- Gemini Response Start ----------")
        self._log_messages(messages)
        message_data = MessageData()
        metrics = Metrics()

        metrics.response_timer.start()
        for response in self.invoke_stream(messages=messages):
            message_data.response_block = response.candidates[0].content
            message_data.response_role = message_data.response_block.role
            message_data.response_parts = message_data.response_block.parts

            if message_data.response_parts is not None:
                for part in message_data.response_parts:
                    part_dict = type(part).to_dict(part)

                    # -*- Yield text if present
                    if "text" in part_dict:
                        text = part_dict.get("text")
                        yield ModelResponse(content=text)
                        message_data.response_content += text
                        metrics.output_tokens += 1
                        if metrics.output_tokens == 1:
                            metrics.time_to_first_token = metrics.response_timer.elapsed
                    else:
                        message_data.valid_response_parts = message_data.response_parts

                    # -*- Skip function calls if there are no parts
                    if not message_data.response_block.parts and message_data.response_parts:
                        continue
                    # -*- Parse function calls
                    if "function_call" in part_dict:
                        message_data.response_tool_calls.append(
                            {
                                "type": "function",
                                "function": {
                                    "name": part_dict.get("function_call").get("name"),
                                    "arguments": json.dumps(part_dict.get("function_call").get("args")),
                                },
                            }
                        )
            message_data.response_usage = response.usage_metadata
        metrics.response_timer.stop()

        # -*- Create assistant message
        assistant_message = Message(
            role=message_data.response_role or "model",
            parts=message_data.valid_response_parts,
            content=message_data.response_content,
        )

        # -*- Update assistant message if tool calls are present
        if len(message_data.response_tool_calls) > 0:
            assistant_message.tool_calls = message_data.response_tool_calls

        # -*- Update usage metrics
        self.update_usage_metrics(assistant_message, message_data.response_usage, metrics)

        # -*- Add assistant message to messages
        messages.append(assistant_message)

        # -*- Log response and metrics
        assistant_message.log()
        metrics.log()

        if assistant_message.tool_calls is not None and len(assistant_message.tool_calls) > 0 and self.run_tools:
            yield from self.handle_stream_tool_calls(assistant_message, messages)
            yield from self.response_stream(messages=messages)

        # -*- Remove parts from messages
        # for m in messages:
        #     if hasattr(m, "parts"):
        #         m.parts = None
        logger.debug("---------- Gemini Response End ----------")
