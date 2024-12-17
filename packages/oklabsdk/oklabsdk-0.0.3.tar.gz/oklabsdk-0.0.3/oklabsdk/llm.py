import os
from openai import OpenAI, AzureOpenAI
from helpers import pdf_to_images, process_images_to_markdown

use_azure = os.getenv("USE_AZURE") == "1"
model_name = None

model = None
if use_azure:
    model = AzureOpenAI()
    model_name = os.getenv("AZURE_DEPLOYMENT_NAME")
else:
    model = OpenAI()
    model_name = os.getenv("OPENAI_MODEL_NAME")


def get_response(prompt, max_tokens=4096, system_message=None):
    """Returns the completion from the LLM model. High time consumption."""
    messages=[{"role": "user", "content": prompt}],
    if(system_message):
        messages.insert(0, {"role": "system", "content": system_message})

    return (
        (
            model.chat.completions.create(
                model=model_name,
                max_tokens=max_tokens,
                messages=messages
            )
        )
        .choices[0]
        .message.content
    )






def convert_to_markdown(path, ouput_folder="ouput_page_markdowns"):
    """(beta) Converts a PDF file to markdown format. Currently only supports Azure deployments with Vision."""
    if(not use_azure):
        raise Exception("This function is only supported with Azure deployments.")
    pdf_to_images(path)
    process_images_to_markdown(model, model_name, image_folder=path, output_folder=ouput_folder)
    print("Conversion complete.")
    
   

# def upload_file(file_path):
#     """Uploads a file to the LLM model."""
#     print("Uploading file...")
#     print(file_path)
#     with open(file_path, "rb") as f:
#         print(f.read())
#         return model.files.create(file=f, purpose="assistants")

if __name__ == "__main__":
    # print(get_response("Hello, what is in this file?", file_path="requirements-dev.txt"))
    # convert_to_markdown("requirements-ac.html")
    pdf_to_images("holubec_cv.pdf")
    process_images_to_markdown(model, model_name)
 