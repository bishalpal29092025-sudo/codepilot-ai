import json
import time
from typing import Any, Dict

from openai import OpenAI
from openai import RateLimitError

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
    - Retry handling
    - Rate limit recovery
    - Debug logging
    - Safe JSON parsing
    """

    MAX_RETRIES = 3


    def __init__(self):

        if not CEREBRAS_API_KEY:
            raise ValueError(
                "CEREBRAS_API_KEY not found in environment variables."
            )


        self.client = OpenAI(
            api_key=CEREBRAS_API_KEY,
            base_url=BASE_URL,
        )


        print(
            f"✅ Connected to Cerebras ({MODEL})"
        )


    # ==========================================================
    # Internal Chat
    # ==========================================================

    def _chat(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
    ) -> str:


        print("\n" + "=" * 70)
        print("🤖 Cerebras")
        print("=" * 70)

        print(
            f"Model       : {MODEL}"
        )


        for attempt in range(
            1,
            self.MAX_RETRIES + 1,
        ):

            try:

                print(
                    f"Sending request... Attempt {attempt}/{self.MAX_RETRIES}"
                )


                response = (
                    self.client.chat.completions.create(
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
                )


                print(
                    "✅ Response received.\n"
                )


                message = response.choices[0].message


                if message.content:

                    return message.content.strip()



                raise RuntimeError(
                    "Model returned empty response."
                )


            except RateLimitError as e:


                if attempt == self.MAX_RETRIES:

                    print(
                        "\n❌ Cerebras rate limit exceeded."
                    )

                    raise e



                wait_time = attempt * 5


                print(
                    f"⚠️ Rate limited. Retrying after {wait_time}s..."
                )


                time.sleep(
                    wait_time
                )


            except Exception:

                raise



    # ==========================================================
    # Plain Chat
    # ==========================================================

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
    ) -> str:


        try:

            return self._chat(
                system_prompt,
                user_prompt,
                temperature,
            )


        except Exception as e:


            print(
                "\n❌ LLM Error"
            )

            print(e)

            raise



    # ==========================================================
    # JSON Chat
    # ==========================================================

    def chat_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.1,
    ) -> Dict[str, Any]:


        response = self.chat(
            system_prompt,
            user_prompt,
            temperature,
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



        # Extract JSON object

        if "{" in response and not response.startswith("{"):

            response = response[
                response.index("{"):
            ]


        if "}" in response:

            response = response[
                : response.rfind("}") + 1
            ]



        try:

            return json.loads(
                response
            )


        except json.JSONDecodeError:


            print(
                "\n❌ Invalid JSON Returned\n"
            )

            print(response)


            raise ValueError(
                "Model did not return valid JSON."
            )



# ==========================================================
# Singleton
# ==========================================================

llm = LLM()



# ==========================================================
# Compatibility Wrapper
# ==========================================================

def ask_llm(
    prompt: str,
) -> str:


    return llm.chat(
        system_prompt=(
            "You are an expert software engineer."
        ),
        user_prompt=prompt,
    )