import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_file_content,
        schema_get_files_info,
        schema_run_python_file,
        schema_write_file
    ]
)

function_map = {
    schema_get_file_content.name: get_file_content,
    schema_get_files_info.name: get_files_info,
    schema_run_python_file.name: run_python_file,
    schema_write_file.name: write_file,
}

def parse_args(argv):
    flags = {
        "verbose": False
    }
    positional = []

    for arg in argv[1:]:  # skip argv[0] which is script name
        if arg.startswith("--"):
            for key in flags.keys():
                if arg[2:] == key:
                    flags[key] = True
        else:
            positional.append(arg)

    user_prompt = " ".join(positional) if positional else None
    return user_prompt, flags

def is_verbose(flags):
    return flags["verbose"]

def call_function(function_call:types.FunctionCall, verbose=False):
    function_name = function_call.name
    function_args = function_call.args or {}
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    function_result = ""
    try:
        function_result = function_map[function_name]("./calculator", **function_args)
    except Exception as e:
        function_result = str(e)
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
    
def main(args):
    user_prompt, flags = parse_args(args)
    if not user_prompt:
        print("Error: no user prompt specified")
        sys.exit()
    
    print("Hello from agent-greg!")

    if is_verbose(flags):
        print(f"User prompt: {user_prompt}")
        
        
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    # Parse response
    for _ in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001", 
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], 
                    system_instruction=system_prompt
                )
            )
        except Exception as e:
            break
        
        for candidate in response.candidates:
            messages.append(candidate.content)
    
        # Display response
        if response.function_calls:
            for function_call in response.function_calls:
                function_result = call_function(function_call, is_verbose(flags))
                messages.append(types.Content(
                    role="tool",
                    parts=[function_result.parts[0]]  # already a Part from from_function_response
                ))
                if "result" in function_result.parts[0].function_response.response and is_verbose(flags):
                    print(f"->{function_result.parts[0].function_response.response["result"]}")
                if "error" in function_result.parts[0].function_response.response:
                    raise Exception(function_result.parts[0].function_response.response["error"])
        # If LLM returned final text (no function calls), print and exit
        elif hasattr(response, "text") and response.text:
            print(response.text)
            break
   
    # Display metadata
    if is_verbose(flags):
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main(sys.argv)
