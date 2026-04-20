from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel

from config import settings
from src.interfaces.cli_components.theme import APP_THEME
from src.interfaces.cli_components import display, prompts
from src.application.render_use_case import RenderUseCase
from src.infrastructure.audio.edge_tts_adapter import EdgeTTSAdapter
from src.infrastructure.visual.huggingface_adapter import HuggingFaceAdapter
from src.infrastructure.video.moviepy_adapter import MoviePyAdapter
from src.infrastructure.local_storage import LocalStorageAdapter

console = Console(theme=APP_THEME)


def _build_use_case() -> RenderUseCase:
    storage = LocalStorageAdapter()
    tts = EdgeTTSAdapter()
    visual = HuggingFaceAdapter()
    video = MoviePyAdapter()
    return RenderUseCase(storage, tts, visual, video, console=console)


def run_submenu(use_case: RenderUseCase, filepath: Path) -> None:
    selected_voice: Optional[str] = None

    while True:
        try:
            script_file = use_case.load_script_file(filepath)
        except Exception as e:
            display.print_error_panel(console, f"Gagal membaca file: {e}")
            return

        display.print_banner(console)
        display.print_script_submenu(console, script_file, filepath.name, selected_voice)

        choice = prompts.prompt_submenu_choice(console)

        if choice == "P":
            console.print()
            selected_voice = prompts.run_voice_settings(console, selected_voice)

        elif choice == "R":
            if selected_voice is None:
                console.print()
                console.print(
                    Panel(
                        "[yellow]⚠  Belum ada suara yang dipilih.\n\n"
                        "[white]Silakan pilih suara terlebih dahulu melalui menu "
                        "[bold magenta][ P ] Pengaturan Suara[/bold magenta][/white][/yellow]",
                        border_style="yellow",
                        padding=(1, 2),
                    )
                )
                console.input("\n[dim]Tekan Enter untuk melanjutkan...[/dim]")
            else:
                console.print()
                prompts.run_render(console, use_case, filepath, script_file, selected_voice)
                console.input("\n[dim]Tekan Enter untuk melanjutkan...[/dim]")

        elif choice == "B":
            break

        else:
            console.print("[red]Pilihan tidak valid. Masukkan P, R, atau B.[/red]")
            console.input("[dim]Tekan Enter untuk melanjutkan...[/dim]")


def main() -> None:
    use_case = _build_use_case()

    while True:
        try:
            display.print_banner(console)
            files = use_case._storage.list_input_files()
            display.print_file_selection_menu(console, files)

            selected_file = prompts.prompt_file_selection(console, files)

            if selected_file is None:
                console.print(
                    Panel(
                        "[bold white]Sampai jumpa! 👋[/bold white]",
                        border_style="cyan",
                        padding=(0, 2),
                    )
                )
                break

            run_submenu(use_case, selected_file)

        except KeyboardInterrupt:
            console.print()
            console.print(
                Panel(
                    "[bold white]Program dihentikan. Sampai jumpa! 👋[/bold white]",
                    border_style="yellow",
                    padding=(0, 2),
                )
            )
            break

        except Exception as e:
            display.print_error_panel(console, f"Terjadi error tidak terduga:\n{e}")
            console.input("[dim]Tekan Enter untuk kembali ke menu utama...[/dim]")