import pytest
import httpx


@pytest.fixture
def client():
    alb_dns = "http://applicationLoadBalancer-162032022.us-east-1.elb.amazonaws.com"

    with httpx.Client(base_url=alb_dns) as client:
        yield client


def test_predict_input_validation_invalid_output(client):
    response = client.post("/predict", json={"text": ""})
    data = response.json()

    assert response.status_code == 422
    assert "detail" in data
    assert isinstance(data["detail"], list)
    assert any("min_length" in str(item) for item in data["detail"])

    response = client.post("/predict", json={"text": None})
    data = response.json()

    assert response.status_code == 422
    assert "detail" in data

    response = client.post("/predict", json={"text": 123})
    data = response.json()

    assert response.status_code == 422
    assert "detail" in data


def test_predict_input_validation_valid_output(client):
    response = client.post("/predict", json={"text": "I love this movie"})
    data = response.json()

    assert response.status_code == 200
    assert "prediction" in data
    assert data["prediction"] in ("positive", "negative", "neutral")


def test_output_is_valid(client):
    response = client.post("/predict", json={"text": "I love this movie"})
    data = response.json()

    assert "prediction" in data
    assert len(data) == 1
    assert isinstance(data["prediction"], str)