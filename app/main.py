import argparse
import os
import sys
import json

from openai import OpenAI

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")

def parse_json_args(f_args):
    f_args=f_args.strip()
    if not f_args:
        return {}
    parsed=json.loads(f_args)
    return parsed

def exec_func(f_name,f_args):
    args_map=parse_json_args(f_args)
    if f_name=="Read":
        file_path=args_map["file_path"]
        with open(file_path, "r", encoding="utf-8") as f:
            contents = f.read()
        return contents

def standardize(content,tool_id):
    return {
        "role": "tool",
        "tool_call_id": tool_id,
        "content": content,
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    msg = [{"role": "user", "content": args.p}]

    while True:

        chat = client.chat.completions.create(
            model="anthropic/claude-haiku-4.5",
            messages=msg,
            tools=[{
                "type": "function",
                "function": {
                    "name": "Read",
                    "description": "Read and return the contents of a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The path to the file to read"
                            }
                        },
                    "required": ["file_path"]
                    }
                }        
            },],
        )

        if not chat.choices or len(chat.choices) == 0:
            raise RuntimeError("no choices in response")
            
        msg.append(chat)

        # You can use print statements as follows for debugging, they'll be visible when running tests.
        print("Logs from your program will appear here!", file=sys.stderr)
    
        # TODO: Uncomment the following line to pass the first stage
        if ((not chat.choices[0].message.tool_calls) or (len(chat.choices[0].message.tool_calls) == 0)):
            print(chat.choices[0].message.content)
            break
        else:
            tool_arr=chat.choices[0].message.tool_calls
            for i in range(len(tool_arr)):
                tool_id=tool_arr[i].id
                first_tool_func=tool_arr[i].function
                func_name=first_tool_func.name
                func_args=first_tool_func.arguments
                res=exec_func(func_name,func_args)
                openai_api_format_tool_response=standardize(res,tool_id)
                msg.append(openai_api_format_tool_response)

if __name__ == "__main__":
    main()
