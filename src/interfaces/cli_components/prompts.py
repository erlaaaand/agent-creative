import asyncio
import tempfile
import os
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt

from src.application.render_use_case import RenderUseCase
from src.infrastructure.audio.edge_tts_adapter import EdgeTTSAdapter
from src.core.entities import ScriptFile
from src.interfaces.cli_components import display


def prompt_file_selection(console: Console, files: list[Path]) -> Path | None:
    if not files:
        choice = Prompt.ask(
            "[bold]Pilihan[/bold]",
            choices=["q", "Q"],
            default="Q",
            console=console,
            show_choices=False,
        )
        return None

    valid_choices = [str(i) for i in range(1, len(files) + 1)] + ["q", "Q"]
    choice = Prompt.ask(
        "[bold]Masukkan nomor file atau Q untuk keluar[/bold]",
        console=console,
        show_choices=False,
    )

    if choice.upper() == "Q":
        return None

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(files):
            return files[idx]
        else:
            console.print("[red]Nomor tidak valid.[/red]")
            return None
    except ValueError:
        console.print("[red]Input tidak valid.[/red]")
        return None


def run_voice_settings(console: Console, current_voice: "str | None") -> "str | None":
    tts = EdgeTTSAdapter()

    if current_voice:
        console.print(f"\n[dim]Suara aktif saat ini: [cyan]{current_voice}[/cyan][/dim]")

    console.print()
    console.print("  [bold cyan][1][/bold cyan] Tampilkan suara Bahasa Indonesia saja [dim](id-ID)[/dim]")
    console.print("  [bold cyan][2][/bold cyan] Tampilkan semua suara [dim](semua bahasa)[/dim]")
    console.print()

    filter_choice = Prompt.ask(
        "[bold]Pilih filter[/bold]",
        choices=["1", "2"],
        default="1",
        console=console,
        show_choices=False,
    )

    console.print("[dim cyan]⏳ Mengambil daftar suara...[/dim cyan]")
    try:
        if filter_choice == "1":
            voices = asyncio.run(tts.get_available_id_voices())
        else:
            voices = asyncio.run(tts.get_all_voices())
    except Exception as e:
        display.print_error_panel(console, f"Gagal mengambil daftar suara: {e}")
        return current_voice

    display.print_voice_list(console, voices, current_voice)

    choice = Prompt.ask(
        "[bold]Pilih nomor suara (0 untuk batal)[/bold]",
        console=console,
        show_choices=False,
    )

    if choice == "0":
        return current_voice

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(voices):
            selected_voice = voices[idx]
            console.print(f"\n[dim cyan]▶ Memutar preview suara [bold]{selected_voice}[/bold]...[/dim cyan]")

            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                tmp_path = tmp.name

            try:
                asyncio.run(tts.preview_voice(selected_voice, tmp_path))
                console.print("[green]✅ Preview sedang diputar...[/green]")
            except Exception as e:
                console.print(f"[yellow]⚠ Preview gagal: {e}[/yellow]")

            console.input("\n[dim]Tekan Enter untuk melanjutkan...[/dim]")
            return selected_voice
        else:
            console.print("[red]Nomor tidak valid.[/red]")
            return current_voice
    except ValueError:
        console.print("[red]Input tidak valid.[/red]")
        return current_voice


def run_render(
    console: Console,
    use_case: RenderUseCase,
    filepath: Path,
    script_file: ScriptFile,
    voice: str,
) -> None:
    display.print_render_document_menu(console, script_file)

    valid_choices = [str(i) for i in range(len(script_file.scripts) + 1)]
    choice = Prompt.ask(
        "[bold]Pilih nomor script untuk di-render (0 untuk kembali)[/bold]",
        console=console,
        show_choices=False,
    )

    if choice == "0":
        return

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(script_file.scripts):
            doc = script_file.scripts[idx]
            console.print(
                f"\n[cyan]🚀 Memulai render: [bold]{doc.topic}[/bold] "
                f"dengan suara [bold]{voice}[/bold][/cyan]\n"
            )

            job = use_case.execute(filepath, doc.document_id, voice)
            display.print_success_panel(
                console,
                f"[bold]{doc.topic}[/bold] berhasil di-render!\n\n"
                f"📁 Output: [cyan]{job.output_path}[/cyan]",
            )
        else:
            console.print("[red]Nomor tidak valid.[/red]")
    except Exception as e:
        display.print_error_panel(console, str(e))


def prompt_submenu_choice(console: Console) -> str:
    return Prompt.ask(
        "[bold]Masukkan pilihan[/bold]",
        console=console,
        show_choices=False,
    ).upper()