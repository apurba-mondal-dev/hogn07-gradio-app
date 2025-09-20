import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception as e:
    print("Error initializing Groq client. Make sure your API key is set in the .env file.")
    client = None
def normalize_code_comments(source_code: str) -> str:
    """
    Uses the Llama 3 model via Groq to normalize comments in a source code string.

    Args:
        source_code: A string containing the source code to be processed.

    Returns:
        A string containing the source code with normalized comments,
        or an error message if the API call fails.
    """
    if not client:
        return "Error: Groq client not initialized. Please check your API key."

    system_prompt = (
        "You are an expert code comment normalizer. Your task is to analyze a source code file "
        "and rewrite its comments to be clear, concise, and professional. Follow these rules:\n"
        "1.  **DO NOT change any of the code logic.** You must only modify the comments.\n"
        "2.  Rewrite comments to be complete sentences, starting with a capital letter and ending with a period.\n"
        "3.  Explain the 'why' behind the code, not just the 'what'.\n"
        "4.  Remove unhelpful or temporary comments (e.g., '# temp fix', '# TODO: fix this later').\n"
        "5.  Ensure the output is the complete, valid source code with the improved comments.\n"
        "6.  If the code has no comments or the comments are already perfect, return the original code without changes."
    )

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,},
                {
                    "role": "user",
                    "content": f"Please normalize the comments in the following source code:\n\n```\n{source_code}\n```",},
            ],
            model="llama-3.1-8b-instant", 
            temperature=0.2,
        )
        response_content = chat_completion.choices[0].message.content 
        if "```" in response_content:
            
            code_block = response_content[response_content.find("```")+3:response_content.rfind("```")]
            
            if code_block.lower().strip().startswith('python'):
                code_block = code_block.strip()[6:].strip()
            return code_block
        else:
            return response_content

    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Error processing file with the API: {e}"