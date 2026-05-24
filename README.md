# Custom Claude Code Implementation

This project is a custom Claude Code-style coding assistant written in Python. It was developed as part of the CodeCrafters "Build Your Own Claude Code" challenge. The assistant mimics an agentic coding workflow by sending prompts to an LLM, handling tool calls, and feeding tool results back into the conversation loop.

## Features

- **Tool Calling Loop:** Supports iterative assistant-tool-assistant messaging until the model returns a final response.
- **File Reading:** Implements a `Read` tool for reading file contents from disk.
- **File Writing:** Implements a `Write` tool for creating or overwriting files.
- **Shell Command Execution:** Implements a `Bash` tool for running shell commands and capturing their output.
- **OpenRouter Integration:** Uses an OpenAI-compatible client configured for OpenRouter via `OPENROUTER_API_KEY` and `OPENROUTER_BASE_URL`.
- **JSON Argument Parsing:** Parses tool arguments from JSON before dispatching to the correct handler.
- **Extensible Tool Dispatch:** Keeps the tool execution logic centralized in a single dispatcher so more tools can be added easily.

## Key Design Aspects & Implementation Details

### 1. Agent Loop Orchestration
The main program follows the standard tool-calling agent pattern:
- Send the current conversation history to the model.
- Inspect the response for tool calls.
- Execute each tool locally.
- Convert tool outputs into the format expected by the chat API.
- Append those tool responses back into the message list and continue until the model stops requesting tools.

This makes the assistant behave like a lightweight coding agent rather than a one-shot chatbot.

### 2. Tool Dispatch Model
The `exec_func` function acts as the central dispatcher for tool execution.
- `Read` opens a file and returns its full contents.
- `Write` opens a file in write mode, which creates the file if it does not exist and overwrites it if it does.
- `Bash` executes a shell command using Python's subprocess capabilities and returns stdout/stderr output.

Keeping tool execution in one place makes the control flow easy to follow and simple to extend.

### 3. JSON Argument Handling
Tool arguments arrive as JSON strings from the model, so the implementation first normalizes them with `parse_json_args`.
- Empty arguments are treated as an empty object.
- JSON is parsed into a dictionary before execution.
- The dispatcher can then safely access the expected fields for each tool.

This keeps the tool layer close to the API contract used by OpenAI-compatible chat completions.

### 4. OpenRouter-Based Model Access
The assistant connects to OpenRouter using the OpenAI Python client.
- The API key is read from `OPENROUTER_API_KEY`.
- The base URL defaults to the OpenRouter API endpoint.
- The model is called through the chat completions interface with tool definitions included.

This makes the project portable across compatible models and easy to swap to another provider if needed.

## Prerequisites

- **Python:** Python 3.14 or newer.
- **Package Manager:** `uv` for local execution.
- **API Access:** A valid `OPENROUTER_API_KEY`.
- **OS:** Linux or macOS.

## Run Instructions

To run the assistant locally, use the provided wrapper script:

```bash
./your_program.sh -p "your prompt here"
```

You can also run the main module directly through `uv` if needed:

```bash
uv run --project . -m app.main -p "your prompt here"
```

To submit your solution to CodeCrafters:

```bash
codecrafters submit
```

# Thanks for Visting the Repo

<img src="https://raw.githubusercontent.com/sarthak-panda/codecrafters-shell-cpp/main/assets/6206076367057652854.jpg"/>

