import base64
import os
import fitz  # PyMuPDF for PDF handling
import requests
from PIL import Image
from openai import OpenAI
from typing import Optional


class InterRailVision:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    @staticmethod
    def download_file(url: str, output_path: str) -> str:
        """
        Download a file from a URL.
        """
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(output_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return output_path
        else:
            raise ValueError(f"Failed to download the file. Status code: {response.status_code}")

    @staticmethod
    def convert_pdf_to_image(pdf_path: str, output_image_path: str, dpi: int = 300) -> str:
        """
        Convert the first page of a PDF to an image.
        """
        pdf_document = fitz.open(pdf_path)
        page = pdf_document[0]
        pix = page.get_pixmap(dpi=dpi)
        pix.save(output_image_path)
        return output_image_path

    @staticmethod
    def encode_image_to_base64(image_path: str) -> str:
        """
        Encode an image file to a base64 string.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def read(self, url: str, user_prompt: str) -> Optional[str]:
        """
        Read content from an image or PDF at the given URL.
        """
        # Download the file
        local_path = "downloaded_file"
        downloaded_file = self.download_file(url, local_path)

        # Determine if it's a PDF or image
        if url.endswith(".pdf"):
            # Convert the first page of the PDF to an image
            image_path = "output_image.png"
            self.convert_pdf_to_image(downloaded_file, image_path)
            encoded_image = self.encode_image_to_base64(image_path)
            os.remove(image_path)
        else:
            # Encode the image directly
            encoded_image = self.encode_image_to_base64(downloaded_file)

        # Delete the downloaded file
        os.remove(downloaded_file)

        # Use the encoded image in the OpenAI API
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
                        },
                    ],
                }
            ],
        )

        return response.choices[0]['message']['content']
