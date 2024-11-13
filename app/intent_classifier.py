import json
from dotenv import load_dotenv
from functools import partial
import os

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)

load_dotenv(f"{parentdir}/.env")

from openai import AzureOpenAI
import os

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-07-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

uq_intents = """['100_NIGHT_TRIAL_OFFER', 'ABOUT_SOF_MATTRESS', 'CANCEL_ORDER', 'CHECK_PINCODE', 'COD', 'COMPARISON', 'DELAY_IN_DELIVERY', 'DISTRIBUTORS', 'EMI', 'ERGO_FEATURES', 'LEAD_GEN', 'MATTRESS_COST', 'OFFERS', 'ORDER_STATUS', 'ORTHO_FEATURES', 'PILLOWS', 'PRODUCT_VARIANTS', 'RETURN_EXCHANGE', 'SIZE_CUSTOMIZATION', 'WARRANTY', 'WHAT_SIZE_TO_ORDER']"""

example_str = """\
"What is the 100-night offer": "100_NIGHT_TRIAL_OFFER"
"Tell me about SOF mattresses": "ABOUT_SOF_MATTRESS"
"Cancel order": "CANCEL_ORDER"
"Is delivery possible on this pincode": "CHECK_PINCODE"
"Can pay later on delivery ": "COD"
"Product comparison": "COMPARISON"
"It's delayed": "DELAY_IN_DELIVERY"
"Nearby Show room": "DISTRIBUTORS"
"I want it on 0% interest": "EMI"
"Ergo features": "ERGO_FEATURES"
"Interested in buying": "LEAD_GEN"
"Mattress cost": "MATTRESS_COST"
"Give me some discount": "OFFERS"
"Track order": "ORDER_STATUS"
"What are the key features of the SOF Ortho mattress": "ORTHO_FEATURES"
"Pillows": "PILLOWS"
" Which mattress is best": "PRODUCT_VARIANTS"
"Looking to exchange": "RETURN_EXCHANGE"
"Can mattress size be customised?": "SIZE_CUSTOMIZATION"
"Does mattress cover is included in warranty": "WARRANTY"
"King Size": "WHAT_SIZE_TO_ORDER"\
"""


def get_intent_openai_few_shot(user_query, uq_intents, examples_str):
    output_json_schema = {"intent": "string"}

    system_message = "You are a helpful customer service representative."
    user_message = """Your job is to indentify the intent of the customer query.
The company is in the business of {company_bussiness}.
Pick only one intent from the list of intents provided below.
List of intents:
{uq_intents}

Here are some example sentece and intent pairs:
{examples}


Provide the answer in the JSON format below:
{output_json_schema}

User Query:
{user_query}

Intent:
"""
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {
                "role": "user",
                "content": user_message.format(
                    company_bussiness="selling mattress",
                    uq_intents=uq_intents,
                    examples=examples_str,
                    user_query=user_query,
                    output_json_schema=output_json_schema,
                ),
            },
        ],
        response_format={"type": "json_object"},
    )

    res = json.loads(completion.choices[0].message.content).get("intent") or "UNKNOWN"
    return res


get_intent_openai_few_shot_partial = partial(
    get_intent_openai_few_shot, uq_intents=uq_intents, examples_str=example_str
)
