"""Entry point for the bot."""

import json
from typing import Union, cast

import chainlit as cl
import litellm
from litellm.types.utils import ModelResponse
from rich import inspect

from myproject.config import config

chat_history = []


@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages."""
    # Your custom logic goes here...

    ## rich debugging
    inspect(message)

    # Check if CHAT_MODEL is set
    chat_model = config("CHAT_MODEL", default=None)

    if chat_model:
        # Use litellm to send message to specified model
        try:
            chat_history.append({"role": "user", "content": message.content})
            completion_response = litellm.completion(
                model=str(chat_model),  # Cast to str to satisfy type checker
                messages=chat_history,
            )

            # Handle the response content based on its type
            if isinstance(completion_response, ModelResponse):
                # Handle dictionary response
                if isinstance(completion_response.choices[0], litellm.Choices):
                    response_content = completion_response.choices[0].message.content
                    chat_history.append({"role": "assistant", "content": response_content})
                else:
                    response_content = str(completion_response)
            else:
                # Handle object response
                response_content = str(completion_response)

        except Exception as e:
            response_content = f"Error using model: {e!s}"
    else:
        # Default behavior - return json of input
        response_content = f"Received: {json.dumps(message.to_dict())}"

    # Ensure we have a valid string response
    if not response_content:
        response_content = "No response generated"

    # Send a response back to the user
    await cl.Message(
        content=response_content,
    ).send()
