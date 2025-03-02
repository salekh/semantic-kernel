# Copyright (c) Microsoft. All rights reserved.

import os
import asyncio
from dotenv import load_dotenv
from semantic_kernel.agents import AgentGroupChat
from azure.identity.aio import DefaultAzureCredential
from semantic_kernel.agents.azure_ai import AzureAIAgent, AzureAIAgentSettings
from azure.ai.projects.models import BingGroundingTool
from semantic_kernel.agents.strategies.termination.termination_strategy import (
    TerminationStrategy,
)
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

#####################################################################
# The following sample demonstrates how to create an OpenAI         #
# assistant using either Azure OpenAI or OpenAI, a chat completion  #
# agent and have them participate in a group chat to work towards   #
# the user's requirement.                                           #
#####################################################################


class ApprovalTerminationStrategy(TerminationStrategy):
    """A strategy for determining when an agent should terminate."""

    async def should_agent_terminate(self, agent, history):
        """Check if the agent should terminate."""
        return (
            "approved" in history[-1].content.lower()
            or "Approved" in history[-1].content.lower()
        )


CAREER_PLANNER_NAME = "CareerPlannerAgent"
CAREER_PLANNER_INSTRUCTIONS = """
You are a career planner agent. Your task is to analyze a candidate's skills, 
experiences, and interests, and suggest suitable career paths. Clearly list 
potential career options and briefly explain why each is suitable based on 
the candidate's skills. Once this is done, trigger the JobSearchAgent to find 
relevant job postings.

If recommendations are provided to adapt the career path, then use these
recommendations to refine the career path and provide the refined career path to the JobSearchAgent.
Whenever feedback is present, it is prefixed with the word Feedback:
"""

JOBFINDER_NAME = "JobSearchAgent"
JOBFINDER_INSTRUCTIONS = """
You are a job search agent who finds job postings in Munich, Germany matching the 
career paths suggested by the CareerPlannerAgent. 
You strictly use the Bing Web Search tool to do this. Do not provide job openings
from your memory. Provide links to actual job postings, clearly list job titles, companies, and key requirements.
Do not invent any details. This is deadly serious.

Assess the career path based on the job postings you find. Give a score between 1 and 10,
with 10 being the best. If the score is below 5, provide feedback to the CareerPlannerAgent.
Prefix feedback with the word Feedback:

If the score is more than 5, create a structured learning plan based on the career options 
provided by the CareerPlannerAgent, and the job postings.
You strictly use the Bing Web Search tool to do this.
Your plan should include:
- Recommended learning resources.
- Actionable preparation tips.
- Actionable interview preparation tips.
- Clear next steps.

Once the plan is complete:
- Provide it to the user, while using the word "Approved Plan" in the message. 
Do not use the word "approve" or "approved" unless you are giving approval.
"""


async def main():
    load_dotenv()
    ai_agent_settings = AzureAIAgentSettings.create()

    async with (
        DefaultAzureCredential() as creds,
        AzureAIAgent.create_client(
            credential=creds,
            conn_str=ai_agent_settings.project_connection_string.get_secret_value(),
        ) as client,
    ):
        # Get Bing Grounding Tool
        bing_connection = await client.connections.get(
            connection_name=os.environ["BING_CONNECTION_NAME"]
        )
        conn_id = bing_connection.id
        bing = BingGroundingTool(connection_id=conn_id)

        # Create the career planner agent definition
        career_planner_definition = await client.agents.create_agent(
            model=ai_agent_settings.model_deployment_name,
            name=CAREER_PLANNER_NAME,
            instructions=CAREER_PLANNER_INSTRUCTIONS,
        )
        agent_careerplanner = AzureAIAgent(
            client=client,
            definition=career_planner_definition,
        )

        # Create the job finder agent definition
        jobfinder_agent_definition = await client.agents.create_agent(
            model=ai_agent_settings.model_deployment_name,
            name=JOBFINDER_NAME,
            instructions=JOBFINDER_INSTRUCTIONS,
            tools=bing.definitions,
            headers={"x-ms-enable-preview": "true"},
        )
        agent_jobfinder = AzureAIAgent(
            client=client,
            definition=jobfinder_agent_definition,
            tools=bing.definitions,
            headers={"x-ms-enable-preview": "true"},
        )

        chat = AgentGroupChat(
            agents=[agent_careerplanner, agent_jobfinder],
            termination_strategy=ApprovalTerminationStrategy(
                agents=[agent_jobfinder], maximum_iterations=20
            ),
        )

        user_input = """I have skills in data analysis, Python programming, and environmental science. What career paths should I consider? Also find relevant jobs for me in the market."""

        try:
            await chat.add_chat_message(
                ChatMessageContent(role=AuthorRole.USER, content=user_input)
            )
            print(f"# {AuthorRole.USER}: '{user_input}'")

            async for content in chat.invoke():
                print(f"# {content.role} - {content.name or '*'}: '{content.content}'")

            print(f"# IS COMPLETE: {chat.is_complete}")

            print("*" * 60)
            print("Chat History (In Descending Order):\n")
            async for message in chat.get_chat_messages():
                print(f"# {message.role} - {message.name or '*'}: '{message.content}'")
        finally:
            print("Cleaning up...")
            await chat.reset()
            await client.agents.delete_agent(agent_careerplanner.id)
            await client.agents.delete_agent(agent_jobfinder.id)


if __name__ == "__main__":
    asyncio.run(main())
