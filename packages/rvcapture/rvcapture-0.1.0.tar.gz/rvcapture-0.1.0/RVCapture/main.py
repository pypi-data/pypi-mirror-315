import typer
from RVCapture.keysManage import AuthKeys
from RVCapture.deviceManage import DeviceManager
import pyfiglet
from termcolor import colored
import os
from tabulate import tabulate

app = typer.Typer(help="Roojh Capture CLI Tool")
key_app = typer.Typer(help="Manage authentication keys")
device_app = typer.Typer(help="Manage devices")
app.add_typer(key_app, name="key")
app.add_typer(device_app, name="device")

# Helper to clear screen and display title
def display_title():
    os.system('cls' if os.name == 'nt' else 'clear')
    title = pyfiglet.figlet_format("Roojh Capture CLI", font="small")
    print(colored(title, 'yellow'))


@key_app.command("add-key")
def add_key(
    alias: str = typer.Option(None, help="Alias for the key (will prompt if not provided)"),
    access_key: str = typer.Option(None, help="Access key for the alias (will prompt if not provided)"),
    access_id: str = typer.Option(None, help="Access ID for the alias (will prompt if not provided)")
):
    """
    Add a new authentication key.
    """
    if not alias:
        alias = typer.prompt("Enter the alias for the key")
    if not access_key:
        access_key = typer.prompt("Enter the access key for the alias")
    if not access_id:
        access_id = typer.prompt("Enter the access ID for the alias")
    
    auth_keys = AuthKeys()
    auth_keys.addKey(alias, access_key, access_id)
    typer.echo(f"Key added for alias: {alias}")


@key_app.command("get-key")
def get_key(
    alias: str = typer.Option(None, help="Alias of the key to fetch (will prompt if not provided)")
):
    """
    Get details of an authentication key by alias.
    """
    if not alias:
        alias = typer.prompt("Enter the alias of the key to fetch")
    
    auth_keys = AuthKeys()
    key = auth_keys.getKey(alias)
    if key:
        typer.echo(f"Alias: {alias}, AccessKey: {key['accessKey']}, AccessID: {key['accessID']}")
    else:
        typer.echo(f"No key found for alias: {alias}")


@key_app.command("delete-key")
def delete_key(
    alias: str = typer.Option(None, help="Alias of the key to delete (will prompt if not provided)")
):
    """
    Delete an authentication key by alias.
    """
    if not alias:
        alias = typer.prompt("Enter the alias of the key to delete")
    
    auth_keys = AuthKeys()
    if auth_keys.deleteKey(alias):
        typer.echo(f"Key deleted for alias: {alias}")
    else:
        typer.echo(f"No key found for alias: {alias}")


@key_app.command("list-keys")
def list_keys():
    """
    List all authentication keys in a tabular format.
    """
    auth_keys = AuthKeys()
    keys = auth_keys.getAllAuthKeys()
    
    if keys:
        table_data = [
            [alias, key['accessKey'], key['accessID']] 
            for alias, key in keys.items()
        ]
        headers = ["Alias", "Access Key", "Access ID"]
        typer.echo(tabulate(table_data, headers, tablefmt="grid"))
    else:
        typer.echo("No keys found.")


@key_app.command("select-key")
def select_key(
    alias: str = typer.Option(None, help="Alias of the key to select as default (will prompt if not provided)")
):
    """
    Select a key as the default for operations.
    """
    if not alias:
        alias = typer.prompt("Enter the alias of the key to select as default")
    
    auth_keys = AuthKeys()
    if alias in auth_keys.getAllAuthKeys():
        auth_keys.setSelectedKey(alias)
        typer.echo(f"Selected alias: {alias}")
    else:
        typer.echo(f"No key found for alias: {alias}")


@key_app.command("selected-key")
def selected_key():
    """
    Show the currently selected authentication key.
    """
    auth_keys = AuthKeys()
    selected = auth_keys.getSelectedKey()
    if selected:
        typer.echo(f"Selected Key - Alias: {auth_keys.selectedKeyAlias}, "
                   f"AccessKey: {selected['accessKey']}, AccessID: {selected['accessID']}")
    else:
        typer.echo("No key is currently selected.")


@device_app.command("list")
def list_devices(
    detailed: bool = typer.Option(False, "-d", "--detailed", help="Show detailed information"),
    limit: int = typer.Option(None, "-l", "--limit", help="Limit the number of devices displayed"),
    only: str = typer.Option(None, "-o", "--only", help="Filter by status (active/inactive)"),
    all : bool = typer.Option(False, "-a", "--all", help="Get globally "),
):
    """
    List devices either from local envoirnment or all devices with options for detailed info, limits, and status filters.
    """

    if all:
        list_global_devices(detailed=detailed, limit=limit, only=only)
    else:
        list_local_devices(detailed=detailed, limit=limit, only=only)

def list_local_devices(
    detailed: bool = typer.Option(False, "-d", "--detailed", help="Show detailed information"),
    limit: int = typer.Option(None, "-l", "--limit", help="Limit the number of devices displayed"),
    only: str = typer.Option(None, "-o", "--only", help="Filter by status (active/inactive)"),
):
    """
    List devices running specifically in this machine.
    """
    manager = DeviceManager()
    manager.list_docker_devices(detailed=detailed, limit=limit, only=only)


def list_global_devices(
    detailed: bool = typer.Option(False, "-d", "--detailed", help="Show detailed information"),
    limit: int = typer.Option(None, "-l", "--limit", help="Limit the number of devices displayed"),
    only: str = typer.Option(None, "-o", "--only", help="Filter by status (active/inactive)"),
):
    """
    List devices running globally.
    """
    manager = DeviceManager()
    
    if only and only not in ['active', 'inactive']:
        typer.echo("Invalid status filter. Use 'active' or 'inactive'.")
        return

    manager.list_devices(detailed=detailed, limit=limit, only=only)


@device_app.command("get-device")
def get_device(
    device_id: str = typer.Option(None, "-d", "--device-id", help="Device ID to fetch"),
):
    """
    Get detailed information about a specific device.
    """
    if not device_id:
        device_id = typer.prompt("Enter the device ID to fetch")

    manager = DeviceManager()
    manager.get_device(device_id)

@device_app.command("reconfigure-device")
def reconfigure_device(
    device_id: str = typer.Option(None, "--device-id", "-d", help="Device ID"),
    port_path: str = typer.Option(None, "--port-path", "-p", help="Port path"),
    recipe_name: str = typer.Option(None, "--recipe-name", "-r", help="Recipe name"),
    mode : str = typer.Option(None, "--mode", "-m", help="USB Serial (1), LAN (2)"),
):
    """
    Update a component on a device.
    """
    if not device_id:
        device_id = typer.prompt("Enter the device ID to update")

    if not mode:
        mode = typer.prompt("Enter the mode to update (USB Serial (1), LAN (2))")

    if not port_path:
        port_path = typer.prompt(f"Enter the {"Lan IP" if mode == "2" else "Com path"} to update")

    if not recipe_name:
        recipe_name = typer.prompt("Enter the recipe name to update")

    manager = DeviceManager()
    manager.update_component(device_id, port_path, recipe_name, mode)

@device_app.command("assign-device")
def assign_device(
    device_id: str = typer.Option(None, "--device-id", "-d", help="Device ID"),
    bed_id: str = typer.Option(None, "--bed-id", "-b", help="Bed ID"),
    hospital_id: str = typer.Option(None, "--hospital-id", "-h", help="Hospital ID"),
):
    """
    Assign a device to a bed.
    """
    if not device_id:
        device_id = typer.prompt("Enter the device ID to assign")

    if not bed_id:
        bed_id = typer.prompt("Enter the bed ID to assign")

    if not hospital_id:
        hospital_id = typer.prompt("Enter the hospital ID to assign")

    manager = DeviceManager()
    manager.assignDeviceToBed(device_id, bed_id, hospital_id)



@device_app.command("provision-device")
def provision_device():
    """
    Provision a new device.
    """
    manager = DeviceManager()
    manager.provision_device()


@device_app.callback(invoke_without_command=True)
def device_menu(ctx: typer.Context):
    """
    Manage devices. 
    Displays a menu if no subcommand is provided.
    """
    if ctx.invoked_subcommand is None:
        display_title()
        typer.echo("Device Management Menu")
        typer.echo("\nAvailable commands:")
        typer.echo("\tlist\t\t\tList devices from the API")
        typer.echo("\tprovision-device\tProvision a new device")
        typer.echo("\tget-device\t\tGet detailed information about a specific device")
        typer.echo("\trecofigure-device\tReconfigure a component on a device")
        typer.echo("\tassign-device\t\tAssign a device to a bed")
        typer.echo("\thelp\t\t\tShow this message and exit.")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Welcome to the Roojh Capture CLI Tool!
    """
    if ctx.invoked_subcommand is None:
        display_title()
        typer.echo("Welcome to the Roojh Capture CLI Tool!")
        typer.echo("\nAvailable commands:")
        typer.echo("  key           Manage authentication keys")
        typer.echo("  device        Manage devices")
        typer.echo("  help          Show this message and exit.")


@key_app.callback(invoke_without_command=True)
def key_menu(ctx: typer.Context):
    """
    Manage authentication keys. 
    Displays a menu if no subcommand is provided.
    """
    if ctx.invoked_subcommand is None:
        display_title()
        typer.echo("Key Management Menu")
        typer.echo("\nAvailable commands:")
        typer.echo("  add-key       Add a new authentication key")
        typer.echo("  get-key       Get details of a specific authentication key")
        typer.echo("  delete-key    Delete an authentication key")
        typer.echo("  list-keys     List all authentication keys")
        typer.echo("  select-key    Select a key as the default")
        typer.echo("  selected-key  Show the currently selected key")
        typer.echo("\nUse 'main.py key <command> --help' for details on a specific command.")



if __name__ == "__main__":
    app()