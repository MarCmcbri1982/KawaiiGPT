# KawaiiGPT
KawaiiGPT — Open-source LLM gateway accessing DeepSeek, Gemini, and Kimi-K2 through reverse-engineered Pollinations API with no API keys required, built-in prompt injection capabilities for security research, Termux/Linux native support, and Rich console interface
<div align="center">

```
 /$$   /$$                                   /$$ /$$        /$$$$$$  /$$$$$$$  /$$$$$$$$
| $$  /$$/                                  |__/|__/       /$$__  $$| $$__  $$|__  $$__/
| $$ /$$/   /$$$$$$  /$$  /$$  /$$  /$$$$$$  /$$ /$$      | $$  \__/| $$  \ $$   | $$   
| $$$$$/   |____  $$| $$ | $$ | $$ |____  $$| $$| $$      | $$ /$$$$| $$$$$$$/   | $$   
| $$  $$    /$$$$$$$| $$ | $$ | $$  /$$$$$$$| $$| $$      | $$|_  $$| $$____/    | $$   
| $$\  $$  /$$__  $$| $$ | $$ | $$ /$$__  $$| $$| $$      | $$  \ $$| $$         | $$   
| $$ \  $$|  $$$$$$$|  $$$$$/$$$$/|  $$$$$$$| $$| $$      |  $$$$$$/| $$         | $$   
|__/  \__/ \_______/ \_____/\___/  \_______/|__/|__/       \______/ |__/         |__/   
```

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

**Open-source LLM gateway — access DeepSeek, Gemini, Kimi-K2 and more through reverse-engineered Pollinations API**

[Installation](#installation) · [Features](#features) · [Configuration](#configuration) · [Usage](#usage) · [FAQ](#faq) · [Disclaimer](#disclaimer)

</div>

---

## About

**KawaiiGPT** is an open-source command-line AI tool that provides unified access to multiple large language models through the [Pollinations](https://github.com/pollinations/pollinations) reverse-engineered API wrapper. No official API keys or registration required — models are accessed freely via the Pollinations gateway at `gen.pollinations.ai`.

The tool supports backend LLMs including **DeepSeek**, **Gemini**, and **Kimi-K2**, with built-in prompt injection (jailbreak) capabilities for security research and red-team evaluation.

> **Note:** KawaiiGPT is not a proprietary model — it is a jailbreak wrapper that proxies requests to existing LLMs through reverse-engineered API endpoints.

## Features

<table>
<tr><td colspan="2"><strong>LLM Access</strong></td></tr>
<tr><td>✅</td><td>Unified gateway to multiple backend LLMs (DeepSeek, Gemini, Kimi-K2)</td></tr>
<tr><td>✅</td><td>Reverse-engineered Pollinations API — no API keys required</td></tr>
<tr><td>✅</td><td>Configurable LLM provider and model selection</td></tr>
<tr><td>✅</td><td>Custom API base URL override</td></tr>
<tr><td colspan="2"><strong>Security Research</strong></td></tr>
<tr><td>✅</td><td>Built-in prompt injection / jailbreak capabilities</td></tr>
<tr><td>✅</td><td>Jailbreak evaluation for red-team testing (see help menu)</td></tr>
<tr><td>✅</td><td>Uncensored model access for penetration testing research</td></tr>
<tr><td colspan="2"><strong>Interface & Platform</strong></td></tr>
<tr><td>✅</td><td>Rich-styled console menu with ASCII art banner</td></tr>
<tr><td>✅</td><td>Native Linux and Termux (Android) support</td></tr>
<tr><td>✅</td><td>One-command install via <code>install.py</code></td></tr>
<tr><td>✅</td><td>Persistent JSON configuration (<code>config.json</code>)</td></tr>
</table>

---

## Installation

### Prerequisites

| Dependency | Version | Purpose |
|------------|---------|---------|
| Python | 3.8+ | Runtime |
| pip | Latest | Package manager |
| git | Latest | Clone repository |
| requests | ≥ 2.28.0 | HTTP client for API calls |
| rich | ≥ 13.0.0 | Terminal UI rendering |

### Linux

```bash
apt-get update && apt-get upgrade -y
apt install python3 python3-pip git -y
git clone https://github.com/MrSanZz/KawaiiGPT
cd KawaiiGPT
python3 install.py
python3 kawai.py
```

### Termux (Android)

```bash
pkg update && pkg upgrade -y
pkg install python3 git -y
git clone https://github.com/MrSanZz/KawaiiGPT
cd KawaiiGPT
python3 install.py
python3 kawai.py
```

### Manual Install

```bash
git clone https://github.com/MrSanZz/KawaiiGPT
cd KawaiiGPT
pip install -r requirements.txt
python3 main.py
```

---

## Configuration

Settings are stored in `config.json` and can be edited from the interactive menu (option `[3]`) or manually:

```json
{
  "llm_provider": "pollinations",
  "api_base_url": "",
  "default_model": "deepseek"
}
```

| Key | Description | Default |
|-----|-------------|---------|
| `llm_provider` | Backend provider: `pollinations`, `deepseek`, `gemini`, `kimi-k2` | `pollinations` |
| `api_base_url` | Custom API endpoint (leave empty for default) | `""` |
| `default_model` | Preferred model name | `""` |

---

## Usage

Launch the application and navigate the Rich-styled console menu:

```
┌─────────────────────────────────────────────────────┐
│              KawaiiGPT — Main Menu                  │
├─────────────────────────────────────────────────────┤
│  [1]  Install dependencies                          │
│  [2]  Start                                         │
│  [3]  Settings                                      │
│  [4]  Description                                   │
│  [0]  Exit                                          │
└─────────────────────────────────────────────────────┘
```

| Option | Action |
|:------:|--------|
| `1` | Install Python dependencies from `requirements.txt` |
| `2` | Launch the LLM chat interface |
| `3` | Configure LLM provider, API URL, default model |
| `4` | Display project README / description |
| `0` | Exit application |

---

## Project Structure

```
KawaiiGPT/
├── main.py                # Entry point — Rich console menu
├── kawai.py               # Alternative entry point (install.py bootstrap)
├── install.py             # Dependency installer
├── config.json            # User configuration (auto-created)
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── core/
│   ├── __init__.py
│   ├── inpainting.py      # LLM response processing
│   ├── processor.py       # Request pipeline
│   └── validator.py       # Input validation
├── detection/
│   ├── __init__.py
│   ├── detector.py        # Model detection logic
│   ├── signature.py       # Prompt signature handling
│   └── temporal.py        # Rate limiting / timing
├── gui/
│   ├── __init__.py
│   └── main_window.py     # GUI interface module
└── utils/
    ├── __init__.py
    ├── file_handler.py    # File I/O utilities
    ├── gpu_manager.py     # Resource management
    └── logger.py          # Logging configuration
```

---

## FAQ

<details>
<summary><strong>What LLM models are supported?</strong></summary>

KawaiiGPT accesses models through the Pollinations API gateway. Currently supported backends include **DeepSeek**, **Gemini**, and **Kimi-K2**. The Pollinations platform also provides access to additional models like GPT-5 and Qwen — availability depends on the upstream API.
</details>

<details>
<summary><strong>Do I need an API key?</strong></summary>

No. KawaiiGPT uses the reverse-engineered Pollinations API which provides free access without registration or API keys. Basic features are available without any credentials.
</details>

<details>
<summary><strong>Why was the original code obfuscated?</strong></summary>

The original releases used obfuscation solely to prevent rebranding and resale of KawaiiGPT under another name. The current version is fully open source. There is no RAT, spyware, malware, or ransomware in the codebase.
</details>

<details>
<summary><strong>Is this the same as WormGPT?</strong></summary>

No. KawaiiGPT is a separate project created for educational and research purposes. The "WormGPT" label is sometimes referenced in jailbroken model contexts, but KawaiiGPT is its own tool — it proxies to legitimate LLMs through reverse-engineered API endpoints.
</details>

<details>
<summary><strong>Does it work on Windows?</strong></summary>

The primary platforms are Linux and Termux (Android). Windows is not officially supported but may work with a standard Python 3.8+ installation. Use WSL for the best experience on Windows.
</details>

<details>
<summary><strong>Is the Pollinations API reliable?</strong></summary>

Pollinations.ai is a free, open-source platform with 500+ community projects. While it provides stable access, availability of specific models may change as the upstream service evolves. Rate limits apply to unauthenticated requests.
</details>

---

## Disclaimer

> **This project is provided for educational and research purposes only.**
>
> - All risks and consequences of usage are the sole responsibility of the user.
> - Modifying or selling this tool is prohibited.
> - KawaiiGPT uses pre-existing models accessed through reverse-engineered APIs — no fine-tuned or custom models are included.
> - Prompt injection (jailbreak) features are intended for authorized security research and red-team evaluation only.
> - The developers are not responsible for any misuse of this tool.

---

<div align="center">

**If you find this project useful, please consider giving it a star** ⭐

Made by [MrSanZz](https://github.com/MrSanZz) · Contributors: Shoukaku07, FlamabyX5

</div>
