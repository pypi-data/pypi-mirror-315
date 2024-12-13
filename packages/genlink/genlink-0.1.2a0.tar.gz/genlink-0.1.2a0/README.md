# Genlink

Genlink is a Python package that provides a unified interface for interacting with various Language Model (LLM) APIs. It simplifies the process of integrating and switching between different LLM providers in your applications.

## Features

- Unified interface for multiple LLM providers (OpenAI, Anthropic, Google's Gemini supported for now)
- Asynchronous support for efficient handling of multiple queries
- Built-in performance metrics and logging
- Support for function calling / tool use in compatible LLMs
- Configurable via YAML files or dictionaries
- Easy-to-use Agent system for managing LLM interactions

The package is still in development and more features will be added as soon as possible.

## Installation

You can install Genlink using pip:

```bash
pip install genlink
```


## Quick Start

Here's a basic example of how to use Genlink with OpenAI's GPT model:

```python
from genlink import GPTConnector, StandardAgent
from genlink.typedicts import LLMParameters, PromptParameters

# Initialize the connector
connector = GPTConnector.from_config(
    api_key="your-api-key-here",
    config_dict={
        "id": "gpt-connector",
        "type": "openai",
        "model": "gpt-3.5-turbo"
    }
)

# Connect to the API
connector.connect()

# Create an agent
agent = StandardAgent(
    id="my-agent",
    name="GPT Agent",
    description="A simple GPT agent",
    generation_parameters=LLMParameters(
        temperature=0.7,
        max_tokens=150
    ),
    prompt_parameters=PromptParameters(
        system_prompt="You are a helpful assistant."
    ),
    connector_list=[connector]
)

# Use the agent
messages = [
    {"role": "user", "content": "What is the capital of France?"}
]

response = agent.workflow(messages)
print(response[0]['content'])
```


## Asynchronous Usage
Genlink supports asynchronous operations for improved performance when handling multiple queries:

```python
import asyncio
from genlink import GPTConnector, StandardAgent

async def main():
    connector = GPTConnector.from_config(...)
    connector.connect()
    
    agent = StandardAgent(...)
    
    messages1 = [Message(role="user", content="Query 1")]
    messages2 = [Message(role="user", content="Query 2")]
    
    results = await asyncio.gather(
        agent.async_workflow(messages1),
        agent.async_workflow(messages2)
    )
    
    for result in results:
        print(result[0]['content'])

asyncio.run(main())
```

## Configuration
Genlink supports configuration via YAML files or dictionaries. Here's an example YAML configuration:

```yaml
id: my-agent
name: GPT Agent
description: A simple GPT agent
generation_parameters:
  temperature: 0.7
  max_tokens: 150
prompt_parameters:
  system_prompt: You are a helpful assistant.
connector_ids:
  - gpt-connector
```

```python
from genlink import StandardAgent

agent = StandardAgent.from_config(
    handler_dict={"gpt-connector": gpt_connector},
    yaml_path="path/to/config.yaml"
)
```

## Available Connectors

```python
# GPT Connector
gpt_connector = GPTConnector.from_config(
    api_key="your-api-key-here",
    config_dict={
        "id": "gpt-connector",
        "type": "openai",
        "model": "gpt-3.5-turbo"
    }
)

# Anthropic Connector
anthropic_connector = AnthropicConnector.from_config(
    api_key="your-anthropic-api-key-here",
    config_dict={
        "id": "anthropic-connector",
        "type": "anthropic",
        "model": "claude-2"
    }
)

# Gemini Connector
gemini_connector = GeminiConnector.from_config(
    api_key="your-gemini-api-key-here",
    config_dict={
        "id": "gemini-connector",
        "type": "gemini",
        "model": "gemini-pro"
    }
)
```

## Adding Custom Connectors
Genlink is designed to be extensible. You can create custom connectors for new LLM providers by subclassing the Connector class and implementing the required methods.

## License
Genlink is released under the MIT License. See the LICENSE file for more details.

## Support
If you encounter any issues or have questions, please file an issue on our GitHub issue tracker.

## Acknowledgements
Genlink was inspired by the need for a unified interface in the rapidly evolving landscape of large language models. We thank all the contributors and the open-source community for their valuable input and support.