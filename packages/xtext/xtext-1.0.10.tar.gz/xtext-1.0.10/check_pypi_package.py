import requests
import typer
from typing import Optional
from rich import print


app = typer.Typer()


@app.command()
def check_pypi_package(
    package_name: str = typer.Argument(..., help="The name of the package to check")
) -> None:
    
    request = requests.get(f"https://pypi.org/simple/{package_name}")

    if request.status_code == 404:
        print(f"The Package [bold plum3]{package_name}[/bold plum3] [bold red]does not exist on PyPI[/bold red]")
    else:
        print(f"The Package [bold plum3]{package_name}[/bold plum3] [bold green]exists on PyPI[/bold green]")


if __name__ == "__main__":

    libs = [
        "xtext"
    ]

    for lib in libs:
        check_pypi_package(lib)
