import base64
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from .prompts import EDA_PROMPT_2
from dotenv import load_dotenv

# loading variables from .env file
load_dotenv()


class ReportGenLLM:
    """
    Loads a Gemini API model, processes images and generates reports.
    """

    def __init__(self, model_name: str = "gemini-1.5-pro"):
        """
        Initializes the Gemini model with the provided API key.
        """
        self.model_name = model_name
        self._load_llm_model()

    def _load_llm_model(self):
        self.alive = True
        try:
            self.llm = ChatGoogleGenerativeAI(model=self.model_name)
        except Exception as e:
            self.alive = False

    def _load_image_from_local(self, image_path: str) -> str:
        """Loads an image from a local file path."""
        try:
            with open(image_path, "rb") as image_file:
                img_bytes = base64.b64encode(image_file.read()).decode("utf-8")
            return img_bytes
        except FileNotFoundError:
            raise FileNotFoundError(f"Image not found at path: {image_path}")
        except Exception as e:
            raise Exception(f"Error loading image: {e}")

    def generate_analysis(self, image_path: str = "./tmp.png") -> str:
        """
        Generates a report based on the image at the provided path.  Handles exceptions.
        """
        try:
            image_bytes = self._load_image_from_local(image_path)
            image_b64 = f"data:image/png;base64,{image_bytes}"
            message = HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": EDA_PROMPT_2,
                    },  # You can optionally provide text parts
                    {"type": "image_url", "image_url": image_b64},
                ]
            )
            report = self.llm.invoke([message])
            return report.content
        except Exception as e:
            return f"Error generating report: {e}"
