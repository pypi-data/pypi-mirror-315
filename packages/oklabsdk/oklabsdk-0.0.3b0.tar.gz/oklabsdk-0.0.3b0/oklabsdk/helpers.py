import os
import pymupdf


def pdf_to_images(pdf_path, dpi=300, output_folder="page_jpegs"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    print(f"Converting PDF to images with DPI={dpi}...")
    pypdf = pymupdf.open(pdf_path)
    for page in pypdf:  # iterate through the pages
        pix = page.get_pixmap(dpi=dpi)  # render page to an image
        pix.save(f"./{output_folder}/page-{page.number}.png")
        
        
import os
import base64
import requests
from pathlib import Path

# Your OpenAI API Key
api_key = os.environ.get("OPENAI_API_KEY")

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')



def process_images_to_markdown(model, model_name, image_folder="page_jpegs", output_folder="page_markdowns"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    images = sorted(Path(image_folder).iterdir(), key=lambda x: x.stem)
    for image_path in images:
        print(f"Processing {image_path.name}...")
        base64_image = encode_image_to_base64(str(image_path))
        markdown_content = image_to_markdown(base64_image, model, model_name)
        print(markdown_content)
        output_path = Path(output_folder) / f"{image_path.stem}.md"
        with open(output_path, 'w', encoding="utf-8") as f:
            f.write(markdown_content)
            print(f"Markdown for {image_path.name} saved to {output_path}")


def image_to_markdown(base64_image, model, model_name):
    completion = model.chat.completions.create(
        messages= [{
            "role": "user",
            "content": [{
                "type": "text",
                "text": "Give me the markdown text output from this page in a PDF using formatting to match the structure of the page as close as you can get. Only output the markdown and nothing else. Do not explain the output, just return it. Do not use a single # for a heading. All headings will start with ## or ###. Convert tables to markdown tables. Describe charts as best you can. DO NOT return in a codeblock. Just return the raw text in markdown format."
            }, {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }]
        }],
        model=model_name,
        max_tokens=4096
    )
    
    return completion.choices[0].message.content
