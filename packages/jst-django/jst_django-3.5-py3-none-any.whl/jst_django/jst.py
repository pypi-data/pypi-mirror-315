import questionary.question
import os
from rich import print
import typer
from cookiecutter.main import cookiecutter
import questionary
from typing import Annotated
from .generate import Generate
from .utils import Jst
from .api import Github
from .translate import Translate
from .module import Module
from jst_aicommit.main import JstAiCommit

app = typer.Typer()

BASE_DIR = os.getcwd()


@app.command(name="install", help="Modul o'rnatish")
def install_module(
    module_name: Annotated[str, typer.Argument()] = None, version: str = typer.Option(None, "--version", "-v")
):
    Module().run(module_name, version)


@app.command(name="create", help="Yangi loyiha yaratish")
def create_project(version: str = typer.Option(None, "--version", "-v")):
    if version is None:
        version = Github().latest_release()
        print("version: ", version)
    else:
        Github().releases(version)
    template = questionary.text("Template: ", default="django").ask()
    if template.startswith("http") is not True:
        template = "https://github.com/JscorpTech/{}".format(template)
    choices = [
        "silk",
        "storage",
    ]
    packages = questionary.checkbox("O'rtailadigan kutubxonalarni tanlang", choices=choices).ask()
    cookiecutter(
        template,
        checkout=version,
        extra_context={choice: choice in packages for choice in choices},
    )


@app.command(name="generate", help="Compoment generatsiya qilish")
def generate():
    Generate().run()


@app.command(name="aic", help="O'zgarishlarga qarab atomatik git commit yaratadi")
def aic():
    JstAiCommit().run()


@app.command(name="init", help="jst.json config faylini yaratish")
def init():
    Jst().make_config()


@app.command(name="requirements", help="Kerakli kutubxonalar")
def requirements():
    Jst().requirements()


@app.command(name="translate", help="Avtomatik tarjima")
def translate():
    Translate().run()


if __name__ == "__main__":
    app()
