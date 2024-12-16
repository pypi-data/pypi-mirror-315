<p align="center">

<h1 align="center">Agentic Security</h1>

<p align="center">
    The open-source Agentic LLM Vulnerability Scanner
    <br />
    <br />

<p>
<img alt="GitHub Contributors" src="https://img.shields.io/github/contributors/msoedov/agentic_security" />
<img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/msoedov/agentic_security" />
<img alt="" src="https://img.shields.io/github/repo-size/msoedov/agentic_security" />
<img alt="Downloads" src="https://static.pepy.tech/badge/agentic_security" />
<img alt="GitHub Issues" src="https://img.shields.io/github/issues/msoedov/agentic_security" />
<img alt="GitHub Pull Requests" src="https://img.shields.io/github/issues-pr/msoedov/agentic_security" />
<img alt="Github License" src="https://img.shields.io/github/license/msoedov/agentic_security" />
</p>
  </p>
</p>

## Features

- Customizable Rule Sets or Agent based attacks🛠️
- Comprehensive fuzzing for any LLMs 🧪
- LLM API integration and stress testing 🛠️
- Wide range of fuzzing and attack techniques 🌀

Note: Please be aware that Agentic Security is designed as a safety scanner tool and not a foolproof solution. It cannot guarantee complete protection against all possible threats.

## 📦 Installation

To get started with Agentic Security, simply install the package using pip:

```shell
pip install agentic_security
```

## ⛓️ Quick Start

```shell
agentic_security

2024-04-13 13:21:31.157 | INFO     | agentic_security.probe_data.data:load_local_csv:273 - Found 1 CSV files
2024-04-13 13:21:31.157 | INFO     | agentic_security.probe_data.data:load_local_csv:274 - CSV files: ['prompts.csv']
INFO:     Started server process [18524]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8718 (Press CTRL+C to quit)
```

```shell
python -m agentic_security
# or
agentic_security --help


agentic_security --port=PORT --host=HOST

```

## UI 🧙

<img width="100%" alt="booking-screen" src="https://res.cloudinary.com/do9qa2bqr/image/upload/v1713002396/1-ezgif.com-video-to-gif-converter_s2hsro.gif">

## LLM kwargs

Agentic Security uses plain text HTTP spec like:

```http
POST https://api.openai.com/v1/chat/completions
Authorization: Bearer sk-xxxxxxxxx
Content-Type: application/json

{
     "model": "gpt-3.5-turbo",
     "messages": [{"role": "user", "content": "<<PROMPT>>"}],
     "temperature": 0.7
}

```

Where `<<PROMPT>>` will be replaced with the actual attack vector during the scan, insert the `Bearer XXXXX` header value with your app credentials.

### Adding LLM integration templates

TBD

```
....
```

## Adding own dataset

To add your own dataset you can place one or multiples csv files with `prompt` column, this data will be loaded on `agentic_security` startup

```
2024-04-13 13:21:31.157 | INFO     | agentic_security.probe_data.data:load_local_csv:273 - Found 1 CSV files
2024-04-13 13:21:31.157 | INFO     | agentic_security.probe_data.data:load_local_csv:274 - CSV files: ['prompts.csv']
```

## Run as CI check

ci.py

```python
from agentic_security import AgenticSecurity

spec = """
POST http://0.0.0.0:8718/v1/self-probe
Authorization: Bearer XXXXX
Content-Type: application/json

{
    "prompt": "<<PROMPT>>"
}
"""
result = AgenticSecurity.scan(llmSpec=spec)

# module: failure rate
# {"Local CSV": 79.65116279069767, "llm-adaptive-attacks": 20.0}
exit(max(r.values()) > 20)
```

```
python ci.py
2024-04-27 17:15:13.545 | INFO     | agentic_security.probe_data.data:load_local_csv:279 - Found 1 CSV files
2024-04-27 17:15:13.545 | INFO     | agentic_security.probe_data.data:load_local_csv:280 - CSV files: ['prompts.csv']
0it [00:00, ?it/s][INFO] 2024-04-27 17:15:13.74 | data:prepare_prompts:195 | Loading Custom CSV
[INFO] 2024-04-27 17:15:13.74 | fuzzer:perform_scan:53 | Scanning Local CSV 15
18it [00:00, 176.88it/s]
+-----------+--------------+--------+
|  Module   | Failure Rate | Status |
+-----------+--------------+--------+
| Local CSV |    80.0%     |   ✘    |
+-----------+--------------+--------+
```

## Extending dataset collections

1. Add new metadata to agentic_security.probe_data.REGISTRY

```python
    {
        "dataset_name": "markush1/LLM-Jailbreak-Classifier",
        "num_prompts": 1119,
        "tokens": 19758,
        "approx_cost": 0.0,
        "source": "Hugging Face Datasets",
        "selected": True,
        "dynamic": False,
        "url": "https://huggingface.co/markush1/LLM-Jailbreak-Classifier",
    },
```

and implement loader into

```python
@dataclass
class ProbeDataset:
    dataset_name: str
    metadata: dict
    prompts: list[str]
    tokens: int
    approx_cost: float

    def metadata_summary(self):
        return {
            "dataset_name": self.dataset_name,
            "num_prompts": len(self.prompts),
            "tokens": self.tokens,
            "approx_cost": self.approx_cost,
        }

```

## Dynamic datasets with mutations

One of the current examples uses sampling for the existing preloaded prompt data and applying mutations yielding a new dataset

```python
class Stenography:
    fn_library = {
        "rot5": stenography_fn.rot5,
        "rot13": stenography_fn.rot13,
        "base64": stenography_fn.base64_encode,
        "mirror": stenography_fn.mirror_words,
        "random_case": stenography_fn.randomize_letter_case,
        "scramble_words": stenography_fn.scramble_words,
        "noise_characters": stenography_fn.insert_noise_characters,
        "substitute_with_ascii": stenography_fn.substitute_with_ascii,
        "remove_vowels": stenography_fn.remove_vowels,
        "zigzag_obfuscation": stenography_fn.zigzag_obfuscation,
    }

    def __init__(self, prompt_groups: [ProbeDataset]):
        self.prompt_groups = prompt_groups

    def apply(self):
        for prompt_group in self.prompt_groups:

            size = len(prompt_group.prompts)
            for name, fn in self.fn_library.items():
                logger.info(f"Applying {name} to {prompt_group.dataset_name}")
                selected_prompts = random.sample(prompt_group.prompts, int(size * 0.25))
                prompts = [
                    f"Follow the instructions in {name}: {fn(p)}"
                    for p in selected_prompts
                ]
                yield ProbeDataset(
                    dataset_name=f"stenography.{name}({prompt_group.dataset_name})",
                    metadata={},
                    prompts=prompts,
                    tokens=count_words_in_list(prompts),
                    approx_cost=0.0,
                )
```

## Probe endpoint

In the example of custom integration, we use `/v1/self-probe` for the sake of integration testing.

```python
POST https://agentic_security-preview.vercel.app/v1/self-probe
Authorization: Bearer XXXXX
Content-Type: application/json

{
    "prompt": "<<PROMPT>>"
}

```

This endpoint randomly mimics the refusal of a fake LLM.

```python
@app.post("/v1/self-probe")
def self_probe(probe: Probe):
    refuse = random.random() < 0.2
    message = random.choice(REFUSAL_MARKS) if refuse else "This is a test!"
    message = probe.prompt + " " + message
    return {
        "id": "chatcmpl-abc123",
        "object": "chat.completion",
        "created": 1677858242,
        "model": "gpt-3.5-turbo-0613",
        "usage": {"prompt_tokens": 13, "completion_tokens": 7, "total_tokens": 20},
        "choices": [
            {
                "message": {"role": "assistant", "content": message},
                "logprobs": None,
                "finish_reason": "stop",
                "index": 0,
            }
        ],
    }

```

## CI/CD integration

TBD

## Documentation

For more detailed information on how to use Agentic Security, including advanced features and customization options, please refer to the official documentation.

## Roadmap and Future Goals

- \[ \] Expand dataset variety
- \[ \] Introduce two new attack vectors
- \[ \] Develop initial attacker LLM
- \[ \] Complete integration of OWASP Top 10 classification

| Tool                    | Source                                                                        | Integrated |
|-------------------------|-------------------------------------------------------------------------------|------------|
| Garak                   | [leondz/garak](https://github.com/leondz/garak)                               | ✅          |
| InspectAI               | [UKGovernmentBEIS/inspect_ai](https://github.com/UKGovernmentBEIS/inspect_ai) | ✅          |
| llm-adaptive-attacks    | [tml-epfl/llm-adaptive-attacks](https://github.com/tml-epfl/llm-adaptive-attacks) | ✅       |
| Custom Huggingface Datasets | markush1/LLM-Jailbreak-Classifier                                                                         | ✅          |
| Local CSV Datasets      | -                                                                             | ✅          |

Note: All dates are tentative and subject to change based on project progress and priorities.

## 👋 Contributing

Contributions to Agentic Security are welcome! If you'd like to contribute, please follow these steps:

- Fork the repository on GitHub
- Create a new branch for your changes
- Commit your changes to the new branch
- Push your changes to the forked repository
- Open a pull request to the main Agentic Security repository

Before contributing, please read the contributing guidelines.

## License

Agentic Security is released under the Apache License v2.

## Contact us

## Repo Activity

<img width="100%" src="https://repobeats.axiom.co/api/embed/2b4b4e080d21ef9174ca69bcd801145a71f67aaf.svg" />
