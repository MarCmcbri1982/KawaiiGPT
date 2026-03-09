"""
KawaiiGPT — Application entry point.
Rich-style console menu: install dependencies, description, settings, start.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.rule import Rule
from rich.theme import Theme

from utils import ensure_env

custom_theme = Theme(
    {
        "logo": "bold magenta",
        "menu": "cyan",
        "menu_key": "bold yellow",
        "success": "bold green",
        "error": "bold red",
        "muted": "dim",
    }
)
console = Console(theme=custom_theme)

BASE_DIR = Path(__file__).parent
README_PATH = BASE_DIR / "README.md"
CONFIG_PATH = BASE_DIR / "config.json"

DEFAULT_CONFIG = {
    "llm_provider": "pollinations",
    "api_base_url": "",
    "default_model": "",
}

def clear_screen() -> None:
    """Clear screen via Rich."""
    console.clear()


def load_config() -> dict:
    """Load config from config.json or return defaults."""
    if not CONFIG_PATH.exists():
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {**DEFAULT_CONFIG, **data}
    except (json.JSONDecodeError, OSError):
        return DEFAULT_CONFIG.copy()


def save_config(config: dict) -> bool:
    """Save config to config.json."""
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except OSError:
        return False


def install_dependencies() -> bool:
    """Install dependencies from requirements.txt."""
    req_file = BASE_DIR / "requirements.txt"
    if not req_file.exists():
        console.print("[error]requirements.txt not found.[/error]")
        return False
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(req_file)],
            check=True,
        )
        console.print("\n[success]Dependencies installed successfully.[/success]\n")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"\n[error]Install failed: {e}[/error]\n")
        return False


def run_app() -> None:
    """Run the main application."""
    from gui.main_window import MainWindow
    app = MainWindow()
    app.run()


def show_description() -> None:
    """Show project description from README.md."""
    if not README_PATH.exists():
        console.print("[error]README.md not found.[/error]")
        return
    try:
        text = README_PATH.read_text(encoding="utf-8")
        md = Markdown(text)
        console.print(Panel(md, title="[logo] Description [/logo]", border_style="magenta"))
    except OSError as e:
        console.print(f"[error]Could not read README: {e}[/error]")


def show_settings() -> None:
    """Show and edit settings (LLM provider, API URL) from README spec."""
    config = load_config()
    while True:
        clear_screen()
        console.print(Panel(
            f"[menu]LLM provider:[/menu] [menu_key]{config['llm_provider']}[/menu_key]\n"
            f"[menu]API base URL:[/menu] [menu_key]{config['api_base_url'] or '(default)'}[/menu_key]\n"
            f"[menu]Default model:[/menu] [menu_key]{config['default_model'] or '(none)'}[/menu_key]",
            title="[logo] Settings [/logo]",
            border_style="magenta",
        ))
        console.print()
        console.print("[menu_key][1][/menu_key] [menu]Set LLM provider[/menu] (pollinations, deepseek, gemini, kimi-k2)")
        console.print("[menu_key][2][/menu_key] [menu]Set API base URL[/menu]")
        console.print("[menu_key][3][/menu_key] [menu]Set default model[/menu]")
        console.print("[menu_key][0][/menu_key] [menu]Back to menu[/menu]")
        console.print()
        choice = Prompt.ask("[bold]Option[/bold]", choices=["0", "1", "2", "3"], default="0")

        if choice == "0":
            break
        if choice == "1":
            provider = Prompt.ask(
                "[bold]LLM provider[/bold] (e.g. pollinations, deepseek, gemini, kimi-k2)",
                default=config["llm_provider"],
            ).strip().lower()
            if provider:
                config["llm_provider"] = provider
                if save_config(config):
                    console.print("[success]Saved.[/success]")
        if choice == "2":
            url = Prompt.ask("[bold]API base URL[/bold]", default=config["api_base_url"] or "")
            config["api_base_url"] = url.strip()
            if save_config(config):
                console.print("[success]Saved.[/success]")
        if choice == "3":
            model = Prompt.ask("[bold]Default model[/bold]", default=config["default_model"] or "")
            config["default_model"] = model.strip()
            if save_config(config):
                console.print("[success]Saved.[/success]")
        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")


LOGO = r"""
 /$$   /$$                                   /$$ /$$        /$$$$$$  /$$$$$$$  /$$$$$$$$
| $$  /$$/                                  |__/|__/       /$$__  $$| $$__  $$|__  $$__/
| $$ /$$/   /$$$$$$  /$$  /$$  /$$  /$$$$$$  /$$ /$$      | $$  \__/| $$  \ $$   | $$   
| $$$$$/   |____  $$| $$ | $$ | $$ |____  $$| $$| $$      | $$ /$$$$| $$$$$$$/   | $$   
| $$  $$    /$$$$$$$| $$ | $$ | $$  /$$$$$$$| $$| $$      | $$|_  $$| $$____/    | $$   
| $$\  $$  /$$__  $$| $$ | $$ | $$ /$$__  $$| $$| $$      | $$  \ $$| $$         | $$   
| $$ \  $$|  $$$$$$$|  $$$$$/$$$$/|  $$$$$$$| $$| $$      |  $$$$$$/| $$         | $$   
|__/  \__/ \_______/ \_____/\___/  \_______/|__/|__/       \______/ |__/         |__/   
"""


def show_menu() -> None:
    """Main menu (Rich style)."""
    clear_screen()
    console.print()
    console.print(
        Panel(
            LOGO.strip(),
            title="[logo] KawaiiGPT [/logo]",
            border_style="magenta",
            padding=(0, 2),
        )
    )
    console.print()
    console.print(Rule(style="dim"))
    console.print()
    console.print("[menu_key][1][/menu_key] [menu]Install dependencies[/menu]")
    console.print("[menu_key][2][/menu_key] [menu]Start[/menu]")
    console.print("[menu_key][3][/menu_key] [menu]Settings[/menu]")
    console.print("[menu_key][4][/menu_key] [menu]Description[/menu]")
    console.print("[menu_key][0][/menu_key] [menu]Exit[/menu]")
    console.print()
    console.print(Rule(style="dim"))


@ensure_env
def main() -> None:
    while True:
        show_menu()
        choice = Prompt.ask(
            "[bold]Choose option[/bold]",
            choices=["0", "1", "2", "3", "4"],
            default="1",
        )

        if choice == "0":
            console.print("\n[muted]Goodbye![/muted]\n")
            break

        if choice == "1":
            confirm = Prompt.ask(
                "\n[bold]Install dependencies from requirements.txt?[/bold]",
                choices=["y", "n"],
                default="n",
            )
            if confirm.lower() == "y":
                console.print("\n[muted]Installing...[/muted]\n")
                install_dependencies()
            else:
                console.print("[muted]Cancelled.[/muted]")
            Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
            continue

        if choice == "2":
            console.print("\n[muted]Starting application...[/muted]\n")
            try:
                run_app()
            except Exception as e:
                console.print(f"[error]Start failed: {e}[/error]")
            Prompt.ask("\n[dim]Press Enter to return to menu[/dim]", default="")
            continue

        if choice == "3":
            show_settings()
            continue

        if choice == "4":
            console.print()
            show_description()
            Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
            continue


if __name__ == "__main__":
    main()
