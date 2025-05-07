import os
from dotenv import load_dotenv
from crewai import Agent
from litellm import completion


load_dotenv()
os.environ["MISTRAL_API_KEY"] = os.getenv("MISTRAL_API_KEY")

class MistralLLM:
    def __init__(self, model: str = "mistral/mistral-large-latest"):
        self.model = model

    def _call(self, prompt: str, stop=None, run_manager=None, **kwargs) -> str:
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            api_key=os.getenv("MISTRAL_API_KEY")
        )
        return response["choices"][0]["message"]["content"]

    @property
    def _llm_type(self) -> str:
        return "mistral-via-litellm"

mistral_llm = MistralLLM()


learning_designer_agent = Agent(
    role="Learning Designer",
    goal="Design a complete learning path with structured modules and summaries",
    backstory="You are a specialist in instructional design. Your job is to outline modules for any learning topic.",
    verbose=True,
    llm=mistral_llm
)

course_creator_agent = Agent(
    role="Course Creator",
    goal="Create detailed lessons, exercises, and resources from a structured learning outline",
    backstory="You're a skilled educator who turns outlines into full course materials with engaging and actionable content.",
    verbose=True,
    llm=mistral_llm
)
