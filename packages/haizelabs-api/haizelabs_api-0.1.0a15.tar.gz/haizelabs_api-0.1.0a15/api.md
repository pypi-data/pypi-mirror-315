# Judges

Types:

```python
from haizelabs_api.types import JudgeCallResponse
```

Methods:

- <code title="post /judges/call">client.judges.<a href="./src/haizelabs_api/resources/judges.py">call</a>(\*\*<a href="src/haizelabs_api/types/judge_call_params.py">params</a>) -> <a href="./src/haizelabs_api/types/judge_call_response.py">JudgeCallResponse</a></code>

# Testing

Types:

```python
from haizelabs_api.types import (
    TestingUpdateResponse,
    TestingCreateEvaluationResponse,
    TestingStartResponse,
    TestingUpdateEvaluationResponse,
    TestingWriteScoreResponse,
)
```

Methods:

- <code title="post /testing/update">client.testing.<a href="./src/haizelabs_api/resources/testing.py">update</a>(\*\*<a href="src/haizelabs_api/types/testing_update_params.py">params</a>) -> <a href="./src/haizelabs_api/types/testing_update_response.py">TestingUpdateResponse</a></code>
- <code title="post /testing/create_evaluation">client.testing.<a href="./src/haizelabs_api/resources/testing.py">create_evaluation</a>(\*\*<a href="src/haizelabs_api/types/testing_create_evaluation_params.py">params</a>) -> <a href="./src/haizelabs_api/types/testing_create_evaluation_response.py">TestingCreateEvaluationResponse</a></code>
- <code title="post /testing/start">client.testing.<a href="./src/haizelabs_api/resources/testing.py">start</a>(\*\*<a href="src/haizelabs_api/types/testing_start_params.py">params</a>) -> <a href="./src/haizelabs_api/types/testing_start_response.py">TestingStartResponse</a></code>
- <code title="post /testing/update_evaluation">client.testing.<a href="./src/haizelabs_api/resources/testing.py">update_evaluation</a>(\*\*<a href="src/haizelabs_api/types/testing_update_evaluation_params.py">params</a>) -> <a href="./src/haizelabs_api/types/testing_update_evaluation_response.py">object</a></code>
- <code title="post /testing/write_score">client.testing.<a href="./src/haizelabs_api/resources/testing.py">write_score</a>(\*\*<a href="src/haizelabs_api/types/testing_write_score_params.py">params</a>) -> <a href="./src/haizelabs_api/types/testing_write_score_response.py">object</a></code>

# Monitoring

Types:

```python
from haizelabs_api.types import MonitoringLogResponse
```

Methods:

- <code title="post /monitoring/log">client.monitoring.<a href="./src/haizelabs_api/resources/monitoring.py">log</a>(\*\*<a href="src/haizelabs_api/types/monitoring_log_params.py">params</a>) -> <a href="./src/haizelabs_api/types/monitoring_log_response.py">object</a></code>
