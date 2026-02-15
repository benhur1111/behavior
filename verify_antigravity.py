import sys
import os
from unittest.mock import MagicMock
from app.api.schemas import AntigravityRequest

# Mock the Anthropic client before importing the service
sys.modules["anthropic"] = MagicMock()
from app.agents.antigravity import AntigravityAgent

def test_antigravity_agent():
    print("Testing AntigravityAgent...")
    
    # Mock the LLM service's client
    agent = AntigravityAgent()
    agent.llm.client = MagicMock()
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="Mocked Analysis Result")]
    agent.llm.client.messages.create.return_value = mock_message

    # Test data
    objective = "Stop postponing output"
    observations = "I feel keeping delaying the task despite knowing it is important."

    # Run analysis
    result = agent.analyze(objective, observations)

    # Verification
    print(f"Result: {result}")
    
    assert result == "Mocked Analysis Result"
    print("✅ Agent analysis test passed!")

    # Verify the prompt construction (indirectly, by checking call args if we wanted to be strict, but this is enough for now)
    call_args = agent.llm.client.messages.create.call_args
    print(f"LLM called with model: {call_args.kwargs['model']}")
    assert call_args.kwargs['model'] == "claude-3-opus-20240229"
    print("✅ Model selection verified!")

if __name__ == "__main__":
    test_antigravity_agent()
