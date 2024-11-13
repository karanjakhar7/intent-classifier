## Intent Classifier

### `experiments/` directory contains the code for the experiments:
- `llm_based.ipynb`: Contains the code for the LLM-based intent classifier.
- `rule_based.ipynb`: Contains the code for the rule based intent classifier with regex.

### `app/` directory contains the code for the web application:
- `intent_classifier.py`: Contains the latest code for the intent classifier using LLM.
- `main.py`: Contains the code for fastapi code.

### Setting up the server
1. The project uses Azure OpenAI models. If you need to use OpenAI models directly, please update the model in the `intent_classifier.py` file. To use AzureOpenAI models create the `.env` file with following environment variables:
    - AZURE_OPENAI_ENDPOINT
    - AZURE_OPENAI_API_KEY <br>
if you want to use some other model, please update the client accordingly.

2. Install uv if not already installed. [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)
3. Install all the dependencies: `uv sync`
4. Start the server `uv run fastapi run`
