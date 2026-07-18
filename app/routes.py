import os
import json
from flask import jsonify, render_template
from openai import OpenAI

from app import app


def build_nba_prompt():
    prompt = (
        "<role> you are a perfect basketball fan who knows all the players and their rankings.</role>\n"
        "<context> we are making mini game which needs 24 random players but thei quality needs to be mixed.</context>\n"
        "<task> make a jason list of just names in [] the players has to be mixed,you need to have balance i chosing for example you can take 4-7 superstars.4-7 bad players and rest let it be average players. </task>\n"
        "<format> [\"james harden\",\"nikola jokic\", ..., \"alex caruso\"]</format>"
    )
    return prompt


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/nvidia", methods=["GET"])
def nvidia_ai():
    api_key = os.environ.get("NVIDIA_KEY")
    if not api_key:
        return jsonify({"error": "Missing NVIDIA_KEY in environment"}), 500

    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key,
    )

    prompt = build_nba_prompt()
    completion = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        top_p=0.95,
        max_tokens=2048,
        extra_body={
            "chat_template_kwargs": {"enable_thinking": True},
            "reasoning_budget": 16384,
        },
        stream=False,
    )

    response_message = completion.choices[0].message
    content = None
    if hasattr(response_message, "content"):
        content = response_message.content
    elif isinstance(response_message, dict):
        content = response_message.get("content", "")
    else:
        content = str(response_message)

    print("NVIDIA AI response:", content)

    try:
        parsed = json.loads(content)
    except Exception:
        parsed = {"raw_response": content}

    return jsonify(parsed)
