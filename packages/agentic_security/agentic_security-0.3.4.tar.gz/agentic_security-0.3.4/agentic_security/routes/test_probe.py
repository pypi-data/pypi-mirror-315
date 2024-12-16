import pytest
from fastapi.testclient import TestClient

from ..app import app
from ..models.schemas import Probe
from ..probe_actor.refusal import REFUSAL_MARKS
from ..probe_data import REGISTRY

client = TestClient(app)


def test_probe_schema_validation():
    """Test Probe model validation"""
    # Valid probe
    probe = Probe(prompt="test prompt")
    assert probe.prompt == "test prompt"

    # Invalid probe (missing required field)
    with pytest.raises(ValueError):
        Probe()


def test_self_probe_endpoint():
    """Test /v1/self-probe endpoint"""
    response = client.post("/v1/self-probe", json={"prompt": "test prompt"})
    assert response.status_code == 200

    data = response.json()
    # Verify OpenAI response structure
    assert "id" in data
    assert "object" in data
    assert "created" in data
    assert "model" in data
    assert "usage" in data
    assert "choices" in data

    # Verify choices structure
    choices = data["choices"]
    assert len(choices) == 1
    assert "message" in choices[0]
    assert "role" in choices[0]["message"]
    assert "content" in choices[0]["message"]

    # Verify message content contains the prompt
    content = choices[0]["message"]["content"]
    assert "test prompt" in content

    # Verify message is either a refusal or "This is a test!"
    remaining_text = content.replace("test prompt", "").strip()
    is_refusal = any(mark in remaining_text for mark in REFUSAL_MARKS)
    is_test = "This is a test!" in remaining_text
    assert is_refusal or is_test


def test_self_probe_invalid_input():
    """Test /v1/self-probe endpoint with invalid input"""
    # Missing prompt field
    response = client.post("/v1/self-probe", json={})
    assert response.status_code == 422

    # Empty prompt
    response = client.post("/v1/self-probe", json={"prompt": ""})
    assert response.status_code == 200  # Empty prompts are allowed by schema


def test_data_config_endpoint():
    """Test /v1/data-config endpoint"""
    response = client.get("/v1/data-config")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(REGISTRY)

    # Verify each item in response matches REGISTRY format
    for item in data:
        assert isinstance(item, dict)
        # Add assertions for expected fields based on REGISTRY structure
        # This will depend on what fields are defined in the REGISTRY items


def test_refusal_rate():
    """Test that refusal rate is approximately 20%"""
    refusal_count = 0
    total_trials = 1000

    for _ in range(total_trials):
        response = client.post("/v1/self-probe", json={"prompt": "test"})
        content = response.json()["choices"][0]["message"]["content"]
        if any(mark in content for mark in REFUSAL_MARKS):
            refusal_count += 1

    refusal_rate = refusal_count / total_trials
    # Allow for some statistical variation (±5%)
    assert (
        0.15 <= refusal_rate <= 0.25
    ), f"Refusal rate {refusal_rate} is outside expected range"
