import gradio as gr
from normalizer import normalize_code_comments
from dotenv import load_dotenv  
load_dotenv()  
def process_file(uploaded_file):
    """
    Gradio wrapper function to handle file upload, processing, and returning the result.
    """
    if uploaded_file is None:
        return "// Please upload a file first."

    
    file_path = uploaded_file.name
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
 
        normalized_code = normalize_code_comments(source_code)
        return normalized_code   
    except Exception as e:
        return f"Error reading or processing file: {e}"
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🤖 HOGN07: AI Code Comment Normalizer
        Upload a source code file (`.py`, `.c`, `.cpp`) and the AI will rewrite the comments to be clear and professional.
        Powered by Llama 3 via Groq.
        """
    )    
    with gr.Row():
        
        file_input = gr.File(
            label="Upload Source Code File",
            file_types=[".py", ".c", ".cpp"],
            type="filepath")
        code_output = gr.Code(
            label="Normalized Code",
            language="python",
            interactive=False )
    normalize_button = gr.Button("✨ Normalize Comments", variant="primary")
    normalize_button.click(
        fn=process_file,
        inputs=file_input,
        outputs=code_output)
    gr.Markdown(
        """
        ---
        **Note:** The AI will only change comments, not your code logic. Always review the output before use.
        """)
if __name__ == "__main__":
    demo.launch()