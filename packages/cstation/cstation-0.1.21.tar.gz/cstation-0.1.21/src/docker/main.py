import typer

app = typer.Typer(no_args_is_help=True)

@app.command()
def deploy():
    print("DEPLOY")


if __name__ == "__main__":
    app()
