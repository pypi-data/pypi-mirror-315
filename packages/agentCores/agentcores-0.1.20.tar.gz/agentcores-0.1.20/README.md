# agentCores
<p align="center">
  <img src="https://raw.githubusercontent.com/Leoleojames1/agentCores/main/src/agentCores/data/agentCoresLogoFix.png" alt="agentCores logo" width="450"/>
</p>

# agentCores: Advanced AI Agent Management System
agentCoresLogoFix.png
agentCores is a powerful and flexible Python package designed to streamline the creation, management, and deployment of AI agents. It provides a robust framework for handling complex agent configurations, making it easier for developers and researchers to work with multiple AI models and agent types.

## What agentCores Does

1. **Agent Configuration Management**: 
   - Create, store, and manage AI agent configurations in a structured SQLite database.
   - Support for various agent types, from simple chatbots to complex multi-modal AI systems.

2. **Template-Based Agent Creation**:
   - Define and use templates for quick agent instantiation.
   - Easily create new agents based on existing templates with custom overrides.

3. **Versioning and Tracking**:
   - Maintain version history of agent configurations.
   - Generate unique identifiers (UIDs) for each agent instance.

4. **Flexible Database Integration**:
   - Store agent data, conversation histories, and knowledge bases in SQLite.
   - Customizable database paths and configurations for different project needs.

5. **Command-Line Interface**:
   - Intuitive CLI for managing agents, perfect for quick tweaks and testing.
   - Commands for listing, creating, modifying, and deleting agents.

6. **Model and Prompt Management**:
   - Configure and manage different AI models (e.g., language models, vision models).
   - Store and version control prompts and system messages.

7. **Extensibility and Customization**:
   - Easy integration with various AI libraries and APIs (e.g., Ollama, OpenAI).
   - Support for custom flags and agent-specific settings.

## Key Benefits

- **Centralized Management**: Keep all your AI agents organized in one place.
- **Rapid Prototyping**: Quickly create and test different agent configurations.
- **Scalability**: Easily manage multiple agents for complex AI systems or large-scale deployments.
- **Version Control**: Track changes and revert to previous configurations when needed.
- **Flexibility**: Adapt to various AI frameworks and model types.
- **Standardization**: Enforce consistent structure across different agent types.

## Ideal For

- **AI Researchers**: Experiment with different agent configurations and model combinations.
- **Chatbot Developers**: Manage multiple chatbots with different personalities or capabilities.
- **MLOps Teams**: Streamline the deployment and management of AI models in production.
- **Game Developers**: Create and manage diverse NPC behaviors and AI opponents.
- **Education Platforms**: Develop and maintain various AI tutors or educational assistants.

## Future-Ready Features

1. **JSON Template Support**: Easily export and import agent configurations.
2. **Embedding Integration**: Planned support for managing and utilizing embeddings.
3. **Advanced Analytics**: Track agent performance and usage statistics.
4. **Multi-Agent Orchestration**: Tools for managing interactions between multiple agents.
5. **pydantic & ollama agentCores**: Future agentCores built around ollama & pydantic agents. Unleashing flexible local agent dbs for advanced code splicing, and agent state monitoring.

agentCores provides a solid foundation for building sophisticated AI agent systems, offering the flexibility and scalability needed for both research and production environments. Whether you're working on a simple chatbot or a complex multi-agent system, agentCores simplifies the process of creating, managing, and deploying AI agents.
    
# installation
```bash
pip install agentCores
```

# quick start

# command-line interface

To access the command-line interface, run:

```shellscript
python -m agentCores
```
This will start the agentCores Management Interface where you can manage your agents using various commands.

Start by using the /help command:
```cmd
Enter commands to manage agent cores. Type '/help' for options.
    
> /help

Commands:
    /agentCores - List all agent cores.
    /showAgent <agent_id> - Show agents with the specified ID.
    /createAgent <template_id> <new_agent_id> - Mint a new agent.
    /createCustomAgent - Interactive custom agent creation.
    /createDatabase <name> <path> - Create a new database.
    /linkDatabase <agent_id> <name> <path> - Link database to agent.
    /storeAgent <file_path> - Store agentCore from json path.
    /exportAgent <agent_id> - Export agentCore to json.
    /deleteAgent <uid> - Delete an agent by UID.
    /resetAgent <uid> - Reset an agent to the base template.
    /chat <agent_id> - Start a chat session with an agent."
    /exit - Exit the interface."
```

Now to get the available agentCores:
```
> /agentCores

ID: default_agent, UID: ff22a0c1, Version: 1
ID: promptBase, UID: 6f18aba0, Version: 1
ID: speedChatAgent, UID: f1a7092c, Version: 1
ID: ehartfordDolphin, UID: 18556c0c, Version: 1
ID: minecraft_agent, UID: 25389031, Version: 1
ID: general_navigator_agent, UID: d1f12a46, Version: 1
```

Now to see an agentCore use the following command
```cmd
> /showAgent general_navigator_agent
```

The agentCore will now be displayed:
```json
{
    "agentCore": {
        "agent_id": "general_navigator_agent",
        "version": 1,
        "uid": "d1f12a46",
        "save_state_date": "2024-12-11",
        "models": {
            "large_language_model": null,
            "embedding_model": null,
            "language_and_vision_model": null,
            "yolo_model": null,
            "whisper_model": null,
            "voice_model": null
        },
        "prompts": {
            "user_input_prompt": "",
            "agentPrompts": {
                "llmSystemPrompt": "You are a helpful llm assistant, designated with with fulling the user's request, the user is communicating with speech recognition and is sending their screenshot data to the vision model for decomposition. Receive this destription and Instruct the user and help them fullfill their request by collecting the vision data and responding. ",
                "llmBoosterPrompt": "Here is the output from the vision model describing the user screenshot data along with the users speech data. Please reformat this data, and formulate a fullfillment for the user request in a conversational speech manner which will be processes by the text to speech model for output. ",
                "visionSystemPrompt": "You are an image recognition assistant, the user is sending you a request and an image please fullfill the request. ",
                "visionBoosterPrompt": "Given the provided screenshot, please provide a list of objects in the image with the attributes that you can recognize. "
            }
        },
        "commandFlags": {
            "TTS_FLAG": false,
            "STT_FLAG": true,
            "CHUNK_FLAG": false,
            "AUTO_SPEECH_FLAG": false,
            "LLAVA_FLAG": true,
            "SPLICE_FLAG": false,
            "SCREEN_SHOT_FLAG": false,
            "LATEX_FLAG": false,
            "CMD_RUN_FLAG": false,
            "AGENT_FLAG": true,
            "MEMORY_CLEAR_FLAG": false
        },
        "conversation": {
            "save_name": "defaultConversation",
            "load_name": "defaultConversation"
        }
    }
}
```

Now to export an agentCore to json execute the following:
```cmd
> /exportAgent general_navigator_agent
agentCore saved to general_navigator_agent_core.json
```

# core development methods

## __init__
```python
agentCores.__init__(db_path: str = "agent_matrix.db", db_config: Optional[Dict] = None, template: Optional[Dict] = None)
"""
Initialize the agentCores system with optional custom configuration.

    db_path: Path to the main agent matrix database.
    db_config: Custom database configuration.
    template: Custom agent template.

This method sets up the agentCores system, initializing the database and loading any custom configurations. 
It's the first method you should call when using the agentCores package.
"""
```

example usage:
```python
from agentCores import agentCores

# Initialize with default settings
core = agentCores()

# Initialize with custom database path
core = agentCores(db_path="/path/to/custom/agent_matrix.db")

# Initialize with custom database configuration
custom_db_config = {
    "system": {"agent_matrix": "/path/to/custom/matrix.db"},
    "agents": {"conversation": "/path/to/custom/conversations/{agent_id}.db"}
}
core = agentCores(db_config=custom_db_config)

# Initialize with custom template
custom_template = {
    "agentCore": {
        "models": {"large_language_model": "phi3"},
        "prompts": {"user_input_prompt": "You are the agentCores assistant..."}
    }
}
core = agentCores(template=custom_template)
```

## mintAgent

```python
agentCores.mintAgent(agent_id: str, db_config: Optional[Dict] = None, model_config: Optional[Dict] = None, prompt_config: Optional[Dict] = None, command_flags: Optional[Dict] = None) -> Dict
"""
Create a new agent with custom configuration.

    agent_id: Unique identifier for the new agent.
    db_config: Custom database configuration for the agent.
    model_config: Model configuration for the agent.
    prompt_config: Prompt configuration for the agent.
    command_flags: Command flags for the agent.


This method creates a new agent with the specified configurations. It returns the complete agent configuration as a dictionary.
"""
```

example usage:
```python
new_agent = core.mintAgent(
    agent_id="custom_assistant",
    model_config={"large_language_model": "phi3"},
    prompt_config={
        "user_input_prompt": "You are a helpful assistant.",
        "agentPrompts": {
            "llmSystemPrompt": "Provide clear and concise answers."
        }
    },
    command_flags={"STREAM_FLAG": True}
)
```

## loadAgentCore

```python
agentCores.loadAgentCore(agent_id: str) -> Optional[Dict[str, Any]]
"""
Load an agent configuration from the library.

    agent_id: ID of the agent to load.

This method retrieves the configuration of a previously stored agent. It returns the agent's configuration as a dictionary if found, or None if the agent doesn't exist.
"""
```

example usage:
```python
agent_config = core.loadAgentCore("ehartfordDolphin")
if agent_config:
    print(f"Loaded agent: {agent_config['agentCore']['agent_id']}")
else:
    print("Agent not found")
```

## storeAgentCore

```python
agentCores.storeAgentCore(agent_id: str, core_config: Dict[str, Any]) -> None
"""
Store an agent configuration in the matrix.

    agent_id: ID of the agent to store.
    core_config: Configuration of the agent to store.

This method saves or updates an agent's configuration in the database.
"""
```

example usage:
```python
agent_config = {
    "agentCore": {
        "agent_id": "custom_assistant",
        "models": {"large_language_model": "phi3"},
        "prompts": {"user_input_prompt": "You are a helpful assistant."}
    }
}
core.storeAgentCore("custom_assistant", agent_config)
```

## listAgentCores

```python
agentCores.listAgentCores() -> list
"""
List all available agent cores.

This method returns a list of all stored agent configurations, including their IDs, UIDs, and versions.
"""
```

example usage:
```python
all_agents = core.listAgentCores()
for agent in all_agents:
    print(f"ID: {agent['agent_id']}, UID: {agent['uid']}, Version: {agent['version']}")
```

## deleteAgentCore

```python
agentCores.deleteAgentCore(agent_id: str) -> None
"""
Remove an agent configuration from storage.

    agent_id: ID of the agent to delete.

This method deletes an agent's configuration from the database.
"""
```

example usage:
```python
core.deleteAgentCore("custom_assistant")
print("Agent deleted")
```

## saveToFile

```python
agentCores.saveToFile(agent_id: str, file_path: str) -> None
"""
Save an agent configuration to a JSON file.

    agent_id: ID of the agent to save.
    file_path: Path to save the JSON file.

This method exports an agent's configuration to a JSON file.
"""
```

example usage:
```python
core.saveToFile("custom_assistant", "custom_assistant_config.json")
print("Agent configuration saved to file")
```

## loadAgentFromFile

```python
agentCores.loadAgentFromFile(file_path: str) -> None
"""
Load an agent configuration from a JSON file and store in matrix.

    file_path: Path to the JSON file to load.

This method imports an agent configuration from a JSON file and stores it in the database.
"""
```

example usage:
```python
core.loadAgentFromFile("custom_assistant_config.json")
print("Agent configuration loaded from file and stored in database")
```

## importAgentCores

```python
agentCores.importAgentCores(import_db_path: str) -> None
"""
Import agent cores from another agent_matrix.db file into the current system.

    import_db_path: Path to the agent_matrix.db file to import from.
    
This method imports all agent configurations from another agent_matrix.db file into the current system. It will merge the imported agents with existing ones, updating any agents with matching IDs. Throws FileNotFoundError if the import database doesn't exist or Exception if there are issues during import.
"""
```

example usage:
```python
# Import agents from another agent_matrix.db
core = agentCores()

# Import from a specific database file
core.importAgentCores("path/to/other/agent_matrix.db")

# Import from a backup
core.importAgentCores("backups/agent_matrix_backup.db")

# Import from a shared team configuration
core.importAgentCores("team/shared_agent_matrix.db")

# Check the imported agents
agents = core.listAgentCores()
for agent in agents:
    print(f"ID: {agent['agent_id']}, UID: {agent['uid']}, Version: {agent['version']}")
```

## commandInterface

```python
agentCores.commandInterface()
"""
Start the command-line interface for managing agents.

This method launches an interactive command-line interface for managing agent cores.
"""
```

example usage:
```python
core.commandInterface()
```

### Additional Database Management

```bash
# Create a new database
> /createDatabase research_results research_results.db

# Link database to existing agent
> /linkDatabase advanced_research_agent citations citations.db
```

## Basic Ollama Usage Example

```python
from agentCores import agentCores
from ollama import chat

# Initialize agentCore
cores = agentCores()

# Create basic Ollama agent configuration
basic_config = {
    "agent_id": "basic_assistant",
    "models": {
        "large_language_model": "llama2",
        "embedding_model": "nomic-embed-text"
    },
    "prompts": {
        "user_input_prompt": "You are a helpful assistant using local models.",
        "agentPrompts": {
            "llmSystemPrompt": "Focus on providing clear, accurate responses. Break down complex topics into understandable explanations.",
            "llmBoosterPrompt": "Include relevant examples when possible and highlight key points for better understanding."
        }
    },
    "commandFlags": {
        "STREAM_FLAG": True,
        "LOCAL_MODEL": True
    }
}

# Create the agent
agent = core.mintAgent(
    agent_id="basic_assistant",
    model_config=basic_config["models"],
    prompt_config=basic_config["prompts"],
    command_flags=basic_config["commandFlags"]
)

# Basic chat function
def chat_with_agent(agent_config, prompt):
    system_prompt = (
        f"{agent_config['agentCore']['prompts']['user_input_prompt']} "
        f"{agent_config['agentCore']['prompts']['agentPrompts']['llmSystemPrompt']} "
        f"{agent_config['agentCore']['prompts']['agentPrompts']['llmBoosterPrompt']}"
    )
    
    stream = chat(
        model=agent_config["agentCore"]["models"]["large_language_model"],
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ],
        stream=True,
    )
    
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)

# Example usage
chat_with_agent(agent, "Explain how neural networks work")
```

# Advanced Ollama Chatbot Usage Example
We can now construct advanced local assistants with ollama agentCores, and embedded db filenames, for nested knowledgeBase architectures.

```python
from agentCores import agentCores
from ollama import chat

# Initialize agentCore
cores = agentCores()

# Create a coding assistant configuration
coding_config = {
    "agent_id": "coding_assistant",
    "models": {
        "large_language_model": "codellama",  # Using CodeLlama for coding tasks
        "embedding_model": "nomic-embed-text"  # For code embeddings and search
    },
    "prompts": {
        "user_input_prompt": "You are an expert programming assistant. Focus on writing clean, efficient, and well-documented code. Explain your implementation choices and suggest best practices.",
        "agentPrompts": {
            "llmSystemPrompt": "When analyzing code or programming problems, start by understanding the requirements, then break down the solution into logical steps. Include error handling and edge cases.",
            "llmBoosterPrompt": "Enhance your responses with: 1) Performance considerations 2) Common pitfalls to avoid 3) Testing strategies 4) Alternative approaches when relevant."
        }
    },
    "commandFlags": {
        "STREAM_FLAG": True,
        "LOCAL_MODEL": True,
        "CODE_MODE": True
    },
    "databases": {
        "conversation_history": "coding_assistant_chat.db",  # Dedicated chat history
        "python_knowledge": "pythonKnowledge.db",           # Python-specific knowledge
        "code_examples": "code_snippets.db"                 # Store useful code examples
    }
}

# Create the coding assistant
coding_agent = core.mintAgent(
    agent_id="coding_assistant",
    model_config=coding_config["models"],
    prompt_config=coding_config["prompts"],
    command_flags=coding_config["commandFlags"],
    db_config=coding_config["databases"]
)

# Stream chat function for code assistance
def stream_code_chat(agent_config, prompt):
    system_prompt = (
        f"{agent_config['agentCore']['prompts']['user_input_prompt']} "
        f"{agent_config['agentCore']['prompts']['agentPrompts']['llmSystemPrompt']} "
        f"{agent_config['agentCore']['prompts']['agentPrompts']['llmBoosterPrompt']}"
    )
    
    stream = chat(
        model=agent_config["agentCore"]["models"]["large_language_model"],
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ],
        stream=True,
    )
    
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)

# Usage examples
stream_code_chat(coding_agent, "Write a Python function to implement a binary search tree with insert and search methods")
```

Key changes made:
1. Changed to `coding_assistant` ID
2. Using `codellama` model
3. Added specialized coding-focused prompts
4. Created dedicated databases:
   - `coding_assistant_chat.db` for conversation history
   - `pythonKnowledge.db` for Python references
   - `code_snippets.db` for example storage
5. Added `CODE_MODE` flag
6. Updated prompts for programming focus

# agentCores Database Configuration Guide

agentCores provides flexible options for database configuration and customization. This guide covers all the ways you can customize your database setup.

## Basic Database Configuration

### Using base_path
Set a custom location for all databases:
```python
from agentCores import agentCores

# Put all databases in a custom location
core = agentCores(base_path="my/custom/path")
```

### Using Custom Database Paths
Override specific database paths:
```python
custom_paths = {
    "system": {
        "agent_matrix": "/path/to/my/matrix.db",
        "documentation": "/docs/store.db"
    },
    "agents": {
        "conversation": "/chats/{agent_id}.db"
    }
}

core = agentCore(db_config=custom_paths)
```

### Per-Agent Configuration
Specify custom paths when creating an agent:
```python
agent = core.mintAgent(
    agent_id="my_agent",
    db_config={
        "conversation": "/my/custom/chats/agent1.db",
        "knowledge": "/data/knowledge.db"
    }
)
```

## Template Configuration

### Using Base Template
Modify the base template:
```python
# Get base template first
cores = agentCores()
base = cores.getNewAgentCore()

# Modify the base template
base["agentCore"]["models"]["large_language_model"] = "my-custom-model"
base["agentCore"]["prompts"]["user_input_prompt"] = "My custom prompt"

# Create new core with modified template
custom_cores = agentCores(template=base)
```

### Custom Template
Create a completely new template:
```python
custom_template = {
    "agentCore": {
        "agent_id": None,
        "version": 1,
        "models": {
            "large_language_model": "codellama",
            "my_custom_model": "custom-model"
        },
        "prompts": {
            "user_input_prompt": "Custom assistant prompt",
            "agentPrompts": {
                "llmSystemPrompt": "Custom system prompt",
                "llmBoosterPrompt": "Custom booster"
            }
        },
        "commandFlags": {
            "CUSTOM_FLAG": True,
            "AGENT_FLAG": True
        }
    }
}

# Initialize with custom template
custom_core = agentCore(template=custom_template)
```

### Template Structure Requirements
```python
{
    "agentCore": {
        "agent_id": None,  # Required but can be None initially
        "version": None,   # Optional, defaults to 1
        "models": {
            # At least one model should be defined
            "large_language_model": None
        },
        "prompts": {
            # At least need a user_input_prompt
            "user_input_prompt": "",
            "agentPrompts": {}
        },
        "commandFlags": {
            # AGENT_FLAG is required
            "AGENT_FLAG": True
        }
    }
}
```

### Sharing Templates
```python
# Save template to file
core.saveToFile("my_template", "template.json")

# Load template in another script
new_core = agentCore()
new_core.loadAgentFromFile("template.json")
```

## Custom Agent Matrix Configuration

### Direct Path Specification
```python
# Create agent matrix in custom location
core = agentCore(db_path="/my/custom/path/agent_matrix.db")
```

### Using Configuration Dictionary
```python
custom_config = {
    "system": {
        "agent_matrix": "/my/custom/path/agent_matrix.db"
    }
}

core = agentCore(db_config=custom_config)
```

### Multiple Project Matrices
```python
# Project A with its own matrix
project_a = agentCore(db_path="/project_a/agents.db")

# Project B with different matrix
project_b = agentCore(db_path="/project_b/agents.db")
```

### Environment-Based Configuration
Set environment variables:
```bash
export AGENTCORE_MATRIX_PATH="/custom/path/agent_matrix.db"
export AGENTCORE_BASE_PATH="/custom/path/agentcore_data"
```

### Team Configuration Sharing
```python
# team_config.py
TEAM_DB_CONFIG = {
    "system": {
        "agent_matrix": "/shared/team/agent_matrix.db",
        "documentation": "/shared/team/docs.db"
    }
}

# usage.py
from team_config import TEAM_DB_CONFIG
core = agentCore(db_config=TEAM_DB_CONFIG)
```