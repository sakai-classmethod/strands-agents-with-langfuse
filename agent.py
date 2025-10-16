from dotenv import load_dotenv
from strands import Agent
from strands.models import BedrockModel
from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp.mcp_client import MCPClient
import argparse
import os
import base64
from strands.telemetry import StrandsTelemetry
import uuid

load_dotenv()

LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST")

LANGFUSE_AUTH = base64.b64encode(
    f"{LANGFUSE_PUBLIC_KEY}:{LANGFUSE_SECRET_KEY}".encode()
).decode()

os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = LANGFUSE_HOST + "/api/public/otel"
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"

strands_telemetry = StrandsTelemetry().setup_otlp_exporter()

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
    session_id = str(uuid.uuid4())

    with aws_knowledge_mcp_client:
        aws_knowledge_mcp = aws_knowledge_mcp_client.list_tools_sync()
        tools = aws_knowledge_mcp

        agent = Agent(
            model=bedrock_model,
            tools=tools,
            trace_attributes={
                "session.id": session_id,
                "user.id": "test-user@example.com",
                "langfuse.tags": ["Strands-Agent"],
            },
        )

        agent(args.query)
