from dotenv import load_dotenv
from strands import Agent
from strands.models import BedrockModel
from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp.mcp_client import MCPClient
import argparse

load_dotenv()

bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-west-2",
)

aws_knowledge_mcp_client = MCPClient(
    lambda: streamablehttp_client("https://knowledge-mcp.global.api.aws")
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AWS Knowledge Agent")
    parser.add_argument("query", type=str, help="質問内容")
    args = parser.parse_args()

    with aws_knowledge_mcp_client:
        aws_knowledge_mcp = aws_knowledge_mcp_client.list_tools_sync()
        tools = aws_knowledge_mcp

        agent = Agent(
            model=bedrock_model,
            tools=tools,
        )

        agent(args.query)
