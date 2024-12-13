import click
import functools
import json
from pathlib import Path
import shutil
import tempfile
from .const import WORKSPACE_DIR
from .hash import get_sha256


@click.group()
@click.option(
    "--verbose",
    "-v",
    count=True,
    help="Increase verbosity level (use multiple times for more verbosity)",
)
@click.pass_context
def main(ctx, verbose):
    """ComfyUI Pack CLI"""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


@main.command(
    name="restore",
    help="Restore the ComfyUI workspace to specified directory",
)
@click.argument("cpack", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--dir",
    "-d",
    default="ComfyUI",
    help="target directory to restore the ComfyUI project",
    type=click.Path(file_okay=False),
)
@click.pass_context
def restore_cmd(ctx, cpack: str, dir: str):
    from .package import install
    from rich.console import Console

    console = Console()

    install(cpack, dir, ctx.obj["verbose"])
    console.print("\n[green]✓ ComfyUI Workspace is restored![/green]")
    console.print(f"{dir}")

    console.print(
        "\n[green] Next steps: [/green]\n"
        "1. Change directory to the restored workspace\n"
        "2. Source the virtual environment by running `source .venv/bin/activate`\n"
        "3. Run the ComfyUI project by running `python main.py`"
    )


def _print_schema(schema, verbose: int = 0):
    from rich.table import Table
    from rich.console import Console

    table = Table(title="")

    # Add columns
    table.add_column("Input", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Required", style="yellow")
    table.add_column("Default", style="blue")
    table.add_column("Range", style="magenta")

    # Get required fields
    required = schema.get("required", [])

    # Add rows
    for field, info in schema["properties"].items():
        range_str = ""
        if "minimum" in info or "maximum" in info:
            min_val = info.get("minimum", "")
            max_val = info.get("maximum", "")
            range_str = f"{min_val} to {max_val}"

        table.add_row(
            field,
            info.get("format", "") or info.get("type", ""),
            "✓" if field in required else "",
            str(info.get("default", "")),
            range_str,
        )

    Console().print(table)


@main.command(name="info")
@click.argument("cpack", type=click.Path(exists=True, dir_okay=False))
@click.pass_context
def info_cmd(ctx, cpack: str):
    """
    Display information about the ComfyUI package.

    Example:
        $ comfy_pack info workspace.cpack.zip
    """
    from .utils import generate_input_model

    with tempfile.TemporaryDirectory() as temp_dir:
        pack_dir = Path(temp_dir) / ".cpack"
        shutil.unpack_archive(cpack, pack_dir)
        workflow = json.loads((pack_dir / "workflow_api.json").read_text())

    inputs = generate_input_model(workflow)
    _print_schema(inputs.model_json_schema(), ctx.obj["verbose"])


@functools.lru_cache
def _get_cache_workspace(cpack: str):
    sha = get_sha256(cpack)
    return WORKSPACE_DIR / sha[0:8]


@main.command(
    context_settings={
        "ignore_unknown_options": True,
        "allow_extra_args": True,
    },
    help="Run a ComfyUI package with the given inputs",
)
@click.argument("cpack", type=click.Path(exists=True, dir_okay=False))
@click.option("--output-dir", "-o", type=click.Path(), default=".")
@click.pass_context
def run(ctx, cpack: str, output_dir: str):
    from .utils import generate_input_model
    from pydantic import ValidationError
    from rich.console import Console

    inputs = dict(
        zip([k.lstrip("-").replace("-", "_") for k in ctx.args[::2]], ctx.args[1::2])
    )

    console = Console()

    with tempfile.TemporaryDirectory() as temp_dir:
        pack_dir = Path(temp_dir) / ".cpack"
        shutil.unpack_archive(cpack, pack_dir)
        workflow = json.loads((pack_dir / "workflow_api.json").read_text())

    input_model = generate_input_model(workflow)

    try:
        validated_data = input_model(**inputs)
        console.print("[green]✓ Input is valid![/green]")
        for field, value in validated_data.model_dump().items():
            console.print(f"{field}: {value}")
    except ValidationError as e:
        console.print("[red]✗ Validation failed![/red]")
        for error in e.errors():
            console.print(f"- {error['loc'][0]}: {error['msg']}")
        return 1

    from .package import install

    workspace = _get_cache_workspace(cpack)
    if not (workspace / "DONE").exists():
        console.print("\n[green]✓ Restoring ComfyUI Workspace...[/green]")
        if workspace.exists():
            shutil.rmtree(workspace)
        install(cpack, workspace)
        with open(workspace / "DONE", "w") as f:
            f.write("DONE")
    console.print("\n[green]✓ ComfyUI Workspace is restored![/green]")
    console.print(f"{workspace}")

    from .run import ComfyUIServer, run_workflow

    with ComfyUIServer(str(workspace.absolute()), verbose=ctx.obj["verbose"]) as server:
        console.print("\n[green]✓ ComfyUI is launched in the background![/green]")
        results = run_workflow(
            server.host,
            server.port,
            workflow,
            Path(output_dir).absolute(),
            verbose=ctx.obj["verbose"],
            **validated_data.model_dump(),
        )
        console.print("\n[green]✓ Workflow is executed successfully![/green]")
        if results:
            console.print("\n[green]✓ Retrieved outputs:[/green]")
        if isinstance(results, dict):
            for field, value in results.items():
                console.print(f"{field}: {value}")
        elif isinstance(results, list):
            for i, value in enumerate(results):
                console.print(f"{i}: {value}")
        else:
            console.print(results)
