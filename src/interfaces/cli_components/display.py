from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.rule import Rule
from rich import box

from src.interfaces.cli_components.theme import APP_NAME, APP_VERSION, APP_SUBTITLE
from src.core.entities import ScriptFile


def print_banner(console: Console) -> None:
    console.clear()
    title_text = Text()
    title_text.append("  ╔═╗  ", style="bold cyan")
    title_text.append(APP_NAME, style="bold white")
    title_text.append(f"  {APP_VERSION}  ", style="dim cyan")
    title_text.append("╗═╗  \n", style="bold cyan")
    title_text.append(f"       {APP_SUBTITLE}       ", style="dim white")

    console.print(
        Panel(
            title_text,
            border_style="cyan",
            padding=(1, 4),
        )
    )
    console.print()


def print_file_selection_menu(console: Console, files: list[Path]) -> None:
    console.print(Rule("[bold cyan]📂 Pilih File JSON Input[/bold cyan]", style="cyan"))
    console.print()

    if not files:
        console.print(
            Panel(
                "[yellow]⚠  Tidak ada file JSON ditemukan di folder [bold]data/input/[/bold]\n"
                "   Pastikan Anda telah menempatkan file JSON yang valid di sana.[/yellow]",
                border_style="yellow",
                padding=(1, 2),
            )
        )
        console.print()
        console.print("  [bold red][ Q ][/bold red] [white]Keluar[/white]")
        console.print()
        return

    table = Table(
        show_header=True,
        header_style="bold cyan",
        box=box.ROUNDED,
        border_style="blue",
        padding=(0, 1),
        expand=False,
    )
    table.add_column("#", style="bold yellow", width=4, justify="center")
    table.add_column("Nama File", style="white", min_width=30)
    table.add_column("Scripts", style="cyan", width=10, justify="center")
    table.add_column("Tanggal", style="dim white", width=14)

    for idx, filepath in enumerate(files, 1):
        try:
            import json
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            script_count = str(len(data.get("scripts", [])))
            date = data.get("date", "-")
        except Exception:
            script_count = "?"
            date = "-"

        table.add_row(str(idx), filepath.name, script_count, date)

    console.print(table)
    console.print()
    console.print("  [bold red][ Q ][/bold red] [white]Keluar[/white]")
    console.print()


def print_script_submenu(
    console: Console,
    script_file: ScriptFile,
    filename: str,
    selected_voice: "str | None",
) -> None:
    console.print(Rule(f"[bold cyan]📄 {filename}[/bold cyan]", style="cyan"))
    console.print()

    for i, doc in enumerate(script_file.scripts, 1):
        console.print(
            f"  [bold yellow]{i}.[/bold yellow] [white]{doc.topic}[/white] "
            f"[dim]({len(doc.scenes)} scenes)[/dim]"
        )
    console.print()

    console.print(Rule("[bold blue]Opsi[/bold blue]", style="blue"))
    console.print()
    console.print("  [bold magenta][ P ][/bold magenta] [white]Pengaturan Suara (Voice Settings)[/white]")

    if selected_voice is None:
        console.print("       [bold red]⚠  Belum ada suara dipilih — wajib diisi sebelum render![/bold red]")
    else:
        console.print(f"       [dim]Suara aktif: [cyan]{selected_voice}[/cyan][/dim]")

    console.print()

    if selected_voice is None:
        console.print("  [dim][ R ][/dim] [dim]Render Video (pilih suara dulu)[/dim]")
    else:
        console.print("  [bold green][ R ][/bold green] [white]Render Video[/white]")
        console.print("       [dim]Generate gambar + audio + rakit video[/dim]")

    console.print()
    console.print("  [bold red][ B ][/bold red] [white]Kembali ke menu utama[/white]")
    console.print()


def print_voice_list(console: Console, voices: list[str], current_voice: "str | None") -> None:
    console.print(Rule("[bold cyan]🎙️ Daftar Suara[/bold cyan]", style="cyan"))
    console.print()

    table = Table(
        show_header=True,
        header_style="bold cyan",
        box=box.SIMPLE_HEAVY,
        border_style="blue",
        padding=(0, 2),
    )
    table.add_column("#", style="bold yellow", width=4, justify="center")
    table.add_column("Nama Suara", style="white", min_width=35)
    table.add_column("Status", style="green", width=12, justify="center")

    for idx, voice in enumerate(voices, 1):
        status = "✅ Aktif" if (current_voice and voice == current_voice) else ""
        table.add_row(str(idx), voice, status)

    console.print(table)
    console.print()


def print_render_document_menu(console: Console, script_file: ScriptFile) -> None:
    console.print(Rule("[bold cyan]🎬 Pilih Script untuk Di-render[/bold cyan]", style="cyan"))
    console.print()

    table = Table(
        show_header=True,
        header_style="bold cyan",
        box=box.ROUNDED,
        border_style="blue",
        padding=(0, 1),
    )
    table.add_column("#", style="bold yellow", width=4, justify="center")
    table.add_column("Document ID", style="cyan", min_width=30)
    table.add_column("Topik", style="white", min_width=20)
    table.add_column("Platform", style="dim white", min_width=20)
    table.add_column("Scenes", style="magenta", width=8, justify="center")

    for idx, doc in enumerate(script_file.scripts, 1):
        table.add_row(
            str(idx),
            doc.document_id,
            doc.topic,
            doc.production_metadata.platform,
            str(len(doc.scenes)),
        )

    console.print(table)
    console.print()
    console.print("  [bold red][ 0 ][/bold red] [white]Kembali[/white]")
    console.print()


def print_error_panel(console: Console, message: str) -> None:
    console.print(
        Panel(
            f"[bold red]❌ ERROR[/bold red]\n\n{message}",
            border_style="red",
            padding=(1, 2),
        )
    )


def print_success_panel(console: Console, message: str) -> None:
    console.print(
        Panel(
            f"[bold green]✅ SUKSES[/bold green]\n\n{message}",
            border_style="green",
            padding=(1, 2),
        )
    )