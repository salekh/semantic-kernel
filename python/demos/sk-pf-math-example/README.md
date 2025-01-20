# Semantic Kernel PromptFlow Basic Example

![Semantic Kernel PromptFlow Example](https://learn.microsoft.com/en-us/semantic-kernel/media/prompt-flow-end-result.png)

## Description

In this project, we will set up a sample chat and evaluation flow for executing math problems via LLMs. This will demonstrate the use of SK skills and the PromptFlow framework.

## Table of Contents

- [Installation](#installation)
- [Serving](#serving)
- [Important Links](#important-links)
- [License](#license)

## Installation

1. Set up a new conda environment with Python 3.10 and install the required packages from the `requirements.txt` file.

    ```bash
    conda create -n math-copilot python=3.10
    conda activate math-copilot
    pip install -r requirements.txt
    ```

2. Create a new chat flow with the Promptflow CLI.

    ```bash
    pf flow init --flow math-copilot --type chat
    ```

## Serving

After the flow has been created, you can serve the flow using the following command:

    pf flow test --flow math-copilot --interactive                                                           ─╯
    pf flow serve --source ./math-copilot --port 8081 --host localhost

This will start an evaluation server through which this flow can be assessed.

For production use, the flow can also be deployed to Docker, Kubernetes or an Azure App Service. Through the Azure AI Studio, this flow can also be hosted using
an Azure ML Endpoint.

## Evaluation

![Semantic Kernel PromptFlow Evaluation](https://learn.microsoft.com/en-us/semantic-kernel/media/evaluating-batch-run-with-prompt-flow.png)

One of the main benefits of using PromptFlow is its unique ability to give us an avenue to bulk test LLM Flows. This can be done by submitting bulk jobs to the
PromptFlow server. The server will then evaluate the jobs and return the results.

To evaluate the flow, you can use the following command:

    pf run create --flow ./math-copilot --data ./math-copilot/data.jsonl --stream --name math-copilot-eval-10-1 --column-mapping chat_history='${data.chat_history}' question='${data.question}' 
    
    pf run show-details -n math-copilot-eval-10-1

## Important Links

- [PromptFlow Docs](https://microsoft.github.io/promptflow/how-to-guides/index.html)
- [Semantic Kernel Docs](https://learn.microsoft.com/en-us/semantic-kernel/)

## License

Information about the license of your project.
