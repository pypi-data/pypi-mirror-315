import typer
import os
import sys
import ansible_runner

from typing_extensions import Annotated

app = typer.Typer(no_args_is_help=True)

@app.command(no_args_is_help=True)
def ssh_setup(ssh_host: Annotated[str, typer.Argument(help="For Specific Host(s) or All")]):
    print("Setting Up SSH Key to Remote Host...")
    os.chdir('/opt/cstation/ansible_playbook/server/')
    print(f'Setting Up SSH Connection for Host(s): {ssh_host}')
    if ssh_host == "All":
        os.system('ansible-playbook server_ssh.yaml')
    else:
        os.system(f'ansible-playbook -l {ssh_host} server_ssh.yaml')


if __name__ == "__main__":
    app()


