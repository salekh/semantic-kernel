import asyncio
from plugins.MathPlugin.Math import Math
from semantic_kernel.connectors.ai.open_ai import AzureTextCompletion, AzureChatCompletion
from semantic_kernel.planning.sequential_planner import SequentialPlanner
import semantic_kernel as sk
from promptflow import tool
from promptflow.connections import AzureOpenAIConnection


@tool
async def my_python_tool(
    input: str,
    deployment_type: str,
    deployment_name: str,
    AzureOpenAIConnection: AzureOpenAIConnection,
) -> str:
    # Initialize the kernel
    kernel = sk.Kernel(log=sk.NullLogger())

    # Add the chat service
    if deployment_type == "chat-completion":
        kernel.add_chat_service(
            "chat_completion",
            AzureChatCompletion(
                deployment_name,
                endpoint=AzureOpenAIConnection.api_base,
                api_key=AzureOpenAIConnection.api_key,
            ),
        )
    elif deployment_type == "text-completion":
        kernel.add_text_completion_service(
            "text_completion",
            AzureTextCompletion(
                deployment_name,
                endpoint=AzureOpenAIConnection.api_base,
                api_key=AzureOpenAIConnection.api_key,
            ),
        )

    # Import the native functions
    kernel.import_plugin(Math(), "MathPlugin")
    # First run without the chat plugin
    # This shows that the math plugin will be triggered no matter what
    # Limitation: Perfect Hallucination Scenario
    # kernel.import_semantic_plugin_from_directory("./plugins", "ChatPlugin")
    planner = SequentialPlanner(kernel=kernel)

    ask = "Answer the user's question with the available capabilities: " + input

    plan = await planner.create_plan(ask)

    # Execute the plan
    result = await plan.invoke()

    for step in plan._steps:
        print(step.description, ":", step._state.__dict__)
    print("Result: " + str(result))

    return str(result)
