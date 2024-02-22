# Semantic Kernel PromptFlow Basic Example

![Semantic Kernel PromptFlow Example](https://learn.microsoft.com/en-us/semantic-kernel/media/prompt-flow-end-result.png)

## Description

In this project, we will set up a sample chat and evaluation flow for executing math problems via LLMs. This will demonstrate the use of SK skills and the PromptFlow framework.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
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

## Usage

Instructions on how to use your project.

## Important Links

- [PromptFlow Docs](https://microsoft.github.io/promptflow/how-to-guides/index.html)

## License

Information about the license of your project.
