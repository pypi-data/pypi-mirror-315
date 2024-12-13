import asyncio
import math
import os
import warnings
from uuid import uuid4

import pytest
import requests
from paperqa.agents.task import GradablePaperQAEnvironment, LitQAv2TaskDataset
from paperqa.litqa import LitQAEvaluation

from pqapi import (
    AnswerResponse,
    QueryRequest,
    UploadMetadata,
    agent_query,
    async_agent_query,
    async_send_feedback,
    check_dois,
    get_bibliography,
    get_query_request,
    upload_file,
    upload_paper,
)
from pqapi.models import AgentSettings, QuerySettings


def test_bad_bibliography():
    with pytest.raises(requests.exceptions.HTTPError):
        get_bibliography("bad-bibliography")


@pytest.mark.parametrize(
    "query",
    [
        "How are bispecific antibodies engineered?",
        QueryRequest(query="How are bispecific antibodies engineered?"),
    ],
)
def test_agent_query(query: QueryRequest | str) -> None:
    response = agent_query(query, "default")
    assert isinstance(response, AnswerResponse)


def test_query_request_deprecation_warning(recwarn: pytest.WarningsRecorder) -> None:
    warnings.simplefilter("always", DeprecationWarning)
    query = {
        "query": "How are bispecific antibodies engineered?",
        "id": uuid4(),
        "group": "default",
    }

    response = agent_query(query, "default")

    deprecation_warnings = [
        w for w in recwarn if isinstance(w.message, DeprecationWarning)
    ]
    # there are two -- one for the QueryRequest and one for AnswerResponse
    assert len(deprecation_warnings) == 2
    assert "Using legacy query format" in str(deprecation_warnings[0].message)
    # just to vibe check we're still getting a healthly response with old queryrequest
    assert response.status == "success"


def test_query_named_template():
    response = agent_query(
        "How are bispecific antibodies engineered?", named_template="hasanybodydone"
    )
    assert isinstance(response, AnswerResponse)


@pytest.mark.asyncio
async def test_get_query_request() -> None:
    assert isinstance(
        await get_query_request(name="better table parsing"), QueryRequest
    )


def test_upload_file() -> None:
    script_dir = os.path.dirname(__file__)
    # pylint: disable-next=consider-using-with
    file = open(os.path.join(script_dir, "paper.pdf"), "rb")  # noqa: SIM115
    response = upload_file(
        "default",
        file,
        UploadMetadata(filename="paper.pdf", citation="Test Citation"),
    )
    assert response["success"], f"Expected success in response {response}."


@pytest.mark.parametrize(
    "query",
    [
        "How are bispecific antibodies engineered?",
        QueryRequest(query="How are bispecific antibodies engineered?"),
    ],
)
@pytest.mark.asyncio
async def test_async_agent_query(query: QueryRequest | str) -> None:
    response = await async_agent_query(query, "default")
    assert isinstance(response, AnswerResponse)


@pytest.mark.asyncio
async def test_feedback_model() -> None:
    response = await async_agent_query(
        QueryRequest(query="How are bispecific antibodies engineered?"), "default"
    )
    assert isinstance(response, AnswerResponse)
    feedback = {"test_feedback": "great!"}
    assert (
        len(await async_send_feedback([response.answer.id], [feedback], "default")) == 1
    )


@pytest.mark.asyncio
async def test_async_tmp():
    response = await async_agent_query(
        QueryRequest(query="How are bispecific antibodies engineered?"),
    )
    assert isinstance(response, AnswerResponse)


def test_upload_paper() -> None:
    script_dir = os.path.dirname(__file__)
    # pylint: disable-next=consider-using-with
    file = open(os.path.join(script_dir, "paper.pdf"), "rb")  # noqa: SIM115
    upload_paper("10.1021/acs.jctc.2c01235", file)


def test_check_dois() -> None:
    response = check_dois(
        dois=[
            "10.1126/science.1240517",
            "10.1126/science.1240517",  # NOTE: duplicate input DOI
            "10.1016/j.febslet.2014.11.036",
        ]
    )
    assert response == {
        "10.1016/j.febslet.2014.11.036": ["c1433904691e17c2", "cached"],
        "10.1126/science.1240517": ["", "DOI not found"],
    }


@pytest.mark.integration
@pytest.mark.asyncio
async def test_litqa_v2_evaluation() -> None:
    """
    Evaluate on LitQA v2 using the default settings on the PaperQA server.

    To evaluate an unreleased paper-qa + server pairing:
    1. Deploy the pre-release of paperqa-server to the dev server.
    2. Run pytest with pqapi set point at the dev server. This can be done via:
       `PQA_URL=<dev url> PQA_API_KEY=<dev key> pytest --capture=no --integration`.
        - Don't use `-n auto` for pytest because it suppresses stdout:
          https://github.com/pytest-dev/pytest-xdist/issues/402
    """

    async def query_then_eval(env: GradablePaperQAEnvironment) -> LitQAEvaluation:
        response = await async_agent_query(
            query=QueryRequest(
                query=env._query.query,
                settings=QuerySettings(agent=AgentSettings(max_timesteps=18)),
            ),
        )
        assert env._evaluation_from_answer is not None
        return await env._evaluation_from_answer(response.answer)

    dataset = LitQAv2TaskDataset()
    evaluations = []
    batch_size = math.ceil(50 / 3)  # Fits eval or test split in <=3 batches
    for batch in dataset.iter_batches(batch_size):
        evaluations += await asyncio.gather(*(query_then_eval(e) for e in batch))
    accuracy, precision = LitQAEvaluation.calculate_accuracy_precision(evaluations)
    print(f"Accuracy: {accuracy * 100:.2f}, Precision: {precision * 100:.2f}.")
