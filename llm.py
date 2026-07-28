import json
from typing import Any, Dict

from openai import OpenAI

from config import (
    BASE_URL,
    CEREBRAS_API_KEY,
    MODEL,
)


class LLM:
    """
    Cerebras LLM Wrapper

    Features
    --------
    - Plain text chat
    - JSON responses
    - Helpful debugging
    - Safe handling of empty responses
    """

    def __init__(self):

        if not CEREBRAS_API_KEY:
            raise ValueError(
                "CEREBRAS_API_KEY not found in environment variables."
            )

        self.client = OpenAI(
            api_key=CEREBRAS_API_KEY,
            base_url=BASE_URL,
        )

        print(f"✅ Connected to Cerebras ({MODEL})")

    # ---------------------------------------------------------
    # Internal Chat
    # ---------------------------------------------------------

    def _chat(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
    ) -> str:

        print("\n" + "=" * 70)
        print("🤖 Cerebras")
        print("=" * 70)
        print(f"Model       : {MODEL}")
        print("Sending request...")

        response = self.client.chat.completions.create(
            model=MODEL,
            temperature=temperature,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        print("✅ Response received.\n")

        message = response.choices[0].message

        # -----------------------------------------------------
        # Normal Text Response
        # -----------------------------------------------------

        if message.content:

            return message.content.strip()

        # -----------------------------------------------------
        # Debug Information
        # -----------------------------------------------------

        print("⚠️ Model returned no text.\n")

        print("=" * 70)
        print("Raw Response")
        print("=" * 70)
        print(response)
        print("=" * 70)

        raise RuntimeError(
            "Model returned no text content. "
            "See raw response above."
        )

    # ---------------------------------------------------------
    # Plain Chat
    # ---------------------------------------------------------

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
    ) -> str:

        try:

            return self._chat(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=temperature,
            )

        except Exception as e:

            print("\n❌ LLM Error")
            print(e)

            raise

    # ---------------------------------------------------------
    # JSON Chat
    # ---------------------------------------------------------

    def chat_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.1,
    ) -> Dict[str, Any]:

        response = self.chat(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
        )

        response = response.strip()

        # Remove markdown fences

        if response.startswith("```json"):

            response = response[7:]

        if response.startswith("```"):

            response = response[3:]

        if response.endswith("```"):

            response = response[:-3]

        response = response.strip()

        # Sometimes models say:
        # "Here is the JSON:"
        if "{" in response and not response.startswith("{"):

            response = response[response.index("{"):]

        if "}" in response:

            response = response[: response.rfind("}") + 1]

        try:

            return json.loads(response)

        except json.JSONDecodeError:

            print("\n❌ Invalid JSON Returned\n")
            print(response)

            raise ValueError(
                "Model did not return valid JSON."
            )


# ---------------------------------------------------------
# Singleton
# ---------------------------------------------------------

llm = LLM()


# ---------------------------------------------------------
# Compatibility Wrapper
# ---------------------------------------------------------

def ask_llm(prompt: str) -> str:

    return llm.chat(
        system_prompt="You are an expert software engineer.",
        user_prompt=prompt,
    )