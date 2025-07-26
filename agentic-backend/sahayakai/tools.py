

from google.adk.tools import ToolContext
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.content_gen_agent import content_gen_agent
from .sub_agents.visual_aid_agent import visual_aid_agent



async def call_content_gen_agent(
    question: str,
    tool_context: ToolContext,
):
    """Tool to call content generation agent."""

    agent_tool = AgentTool(agent=content_gen_agent)

    content_gen_result = await agent_tool.run_async(
        args={"request": question}, tool_context=tool_context
    )
    tool_context.state["content_gen_agent_output"] = content_gen_result
    return content_gen_result


async def call_visual_aid_agent(
    question: str,
    tool_context: ToolContext,
):
    """Tool to call visual aid agent."""

    agent_tool = AgentTool(agent=visual_aid_agent)

    visual_aid_agent_output = await agent_tool.run_async(
        args={"request": question}, tool_context=tool_context
    )
    tool_context.state["visual_aid_agent_output"] = visual_aid_agent_output
    return visual_aid_agent_output