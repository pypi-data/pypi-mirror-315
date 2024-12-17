import uuid
from RVCapture.apiManage import DeviceAPI
from RVCapture.configManage import ConfigStore
from tabulate import tabulate
from termcolor import colored
from halo import Halo
from RVCapture.dockerManage import DockerManage
import re
from RVCapture.utils import (
    fetch_env_vars_for_add_device,
    detect_os,
    install_aws_cli,
    authenticate_ecr,
    loadAppConfig,
    pull_docker_image,
    check_docker_image,
    run_docker_container,
    check_command_availability,
)


class DeviceManager:
    def __init__(self):
        self.device_api = DeviceAPI()
        self.configManage = ConfigStore()

    def list_devices(self, detailed: bool = False, limit: int = None, only: str = None):
        """
        List devices with optional filters for detailed info, limit, and status.
        """
        spinner = Halo(text="Searching global devices...", spinner="dots")
        spinner.start()

        data = self.device_api.get_devices()
        spinner.stop()

        if not data or not data["status"]:
            print("Failed to retrieve devices.")
            return

        devices = data["data"]

        if only:
            devices = self.device_api.filter_devices(devices, only)

        if limit:
            devices = devices[:limit]

        table_data = []
        for device in devices:
            device = dict(device)
            if detailed:
                row = [
                    device["deviceId"],
                    device["bedId"],
                    device["deviceType"],
                    device["driverId"],
                    device["hospitalId"],
                    f"Hospital - {device.get('hospitalId', 'N/A')}\nWard - {device.get('wardId', 'N/A')}\nBed - {device.get('bedId', 'N/A')}",
                    device["status"],
                ]
            else:
                row = [
                    device["deviceId"],
                    f"Hospital - {device.get('hospitalId', 'N/A')}\nWard - {device.get('wardId', 'N/A')}\nBed - {device.get('bedId', 'N/A')}",
                    device["status"],
                ]
            table_data.append(row)

        headers = ["Device ID", "Location", "Status"]
        if detailed:
            headers = [
                "Device ID",
                "Bed ID",
                "Device Type",
                "Driver ID",
                "Hospital ID",
                "Location",
                "Status",
            ]

        # Color the status column based on active or inactive
        for row in table_data:
            status = row[-1]
            if status == "active":
                row[-1] = colored(status, "green")
            elif status == "inactive":
                row[-1] = colored(status, "red")

        # Print the table
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def list_docker_devices(
        self, detailed: bool = False, limit: int = None, only: str = None
    ):
        """
        List devices running specifically in this machine.
        """

        # Check docker status
        spinner = Halo(text="Checking docker status...", spinner="dots")
        spinner.start()
        docker_status = DockerManage.get_docker_status()
        if docker_status["status"] != 1:
            spinner.fail(f'An error occurred - {docker_status["message"]}')
            return docker_status
        spinner.succeed(f'Docker status: {docker_status["message"]}')
        spinner.stop()

        # Search for local devices
        spinner = Halo(text="Searching local devices...", spinner="dots")
        spinner.start()
        containers = DockerManage.get_docker_containers()
        if containers["status"] != 1:
            spinner.fail(f'An error occurred - {containers["message"]}')
            return containers
        spinner.succeed(f"Found local devices")
        spinner.stop()

        # Filter out non-roojh containers
        containers = containers["message"]
        headers = re.split(r"\s{2,}", containers[0])
        containers = containers[1:-1]
        container_data = []
        for container in containers:
            data = re.split(r"\s{2,}", container)
            if "147997154696" in data[1]:
                container_data.append(data)

        if len(container_data) == 0:
            spinner.fail(f"No Roojh Capture devices found.")
            return

        # Print the table
        print(tabulate(container_data, headers=headers, tablefmt="grid"))

    def get_device(self, device_id: str):
        """
        Get detailed information about a specific device.
        """
        spinner = Halo(text=f"Loading device {device_id}...", spinner="dots")
        spinner.start()

        data = self.device_api.get_device(device_id)
        spinner.stop()

        if not data or not data["status"]:
            print(f"No device found with id : {device_id}.")
            return

        device = data["data"]
        print(f"Device {device_id}:")
        print(f"  Bed ID: {device['bedId']}")
        print(f"  Device Type: {device['deviceType']}")
        print(f"  Driver ID: {device['driverId']}")
        print(f"  Hospital ID: {device['hospitalId']}")
        print(f"  Location: {device['location']}")
        print(f"  Status: {device['status']}")

    def update_component(self, device_id: str, port_path: str, recipe_name: str, mode: int):
        """
        Update a component on a device.
        """
        spinner = Halo(
            text=f"Updating component on device {device_id}...", spinner="dots"
        )
        spinner.start()

        data = self.device_api.updateComponentOnDevice(
            device_id, port_path, recipe_name, mode
        )
        spinner.stop()

        if not data:
            print(f"Failed to update component on device {device_id}.")
            return

        print(f"Component updated successfully on device {device_id}.")

    def assignDeviceToBed(self, device_id: str, bed_id: str, hospital_id: str):
        """
        Assign a device to a bed.
        """
        spinner = Halo(
            text=f"Assigning device {device_id} to bed {bed_id}...", spinner="dots"
        )
        spinner.start()

        data = self.device_api.assignDeviceToBed(device_id, bed_id, hospital_id)
        spinner.stop()

        if not data:
            print(f"Failed to assign device {device_id} to bed {bed_id}.")
            return

        print(f"Device {device_id} assigned to bed {bed_id}.")

    def provision_device(self):
        spinner = Halo(text="Starting provisioning of a new device...", spinner="dots")
        spinner.start()

        configs = loadAppConfig()["dockerConfig"]
        AWS_ACCOUNT_ID = configs["aws_account_id"]
        REPOSITORY_NAME = configs["repository_name"]
        IMAGE_TAG = configs["image_tag"]
        AWS_REGION = configs["aws_region"]

        # check for os
        spinner.text = "Checking operating system..."
        os = detect_os()
        if os["status"] != 1:
            spinner.fail(f"Error: {os['message']}")
            spinner.stop()
            return
        else:
            spinner.succeed(f"Operating system: {os['message']}")

        # Check for env variables
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN = "", "", ""
        env_vars = fetch_env_vars_for_add_device()
        if env_vars["status"] != 1:
            spinner.fail(f"Error: {env_vars['message']}")
            spinner.stop()
            return
        else:
            spinner.succeed(f"Environment variables found.")
            AWS_ACCESS_KEY_ID = env_vars["message"]["AWS_ACCESS_KEY_ID"]
            AWS_SECRET_ACCESS_KEY = env_vars["message"]["AWS_SECRET_ACCESS_KEY"]
            AWS_SESSION_TOKEN = env_vars["message"]["AWS_SESSION_TOKEN"]

        # Check for command availability
        spinner.text = "Checking for required commands..."
        unavailable_commands = []
        if not check_command_availability("docker"):
            unavailable_commands.append("docker")
        if not check_command_availability("unzip"):
            unavailable_commands.append("unzip")
        if len(unavailable_commands) > 0:
            spinner.fail(
                f"Error: The following commands are not available: {', '.join(unavailable_commands)}"
            )
            spinner.stop()
            return
        else:
            spinner.succeed(f"All required commands are available.")
        if not check_command_availability("aws"):
            spinner.text = "Installing AWS CLI..."
            res = install_aws_cli()
            if res["status"] != 1:
                spinner.fail(f"Error: {res['message']}")
                spinner.stop()
                return
            else:
                spinner.succeed(f"Success : {res['message']}")

        IMAGE_URI = f"{AWS_ACCOUNT_ID}.dkr.ecr.{AWS_REGION}.amazonaws.com/{REPOSITORY_NAME}:{IMAGE_TAG}"

        # authenticate ecr
        spinner.text = "Authenticating ECR..."
        res = authenticate_ecr(AWS_REGION, AWS_ACCOUNT_ID)
        if res["status"] != 1:
            spinner.fail(f"Error: {res['message']}")
            spinner.stop()
            return
        else:
            spinner.succeed(f"Success : {res['message']}")

        # check if docker image exists
        spinner.text = "Checking if Docker image exists..."
        res = check_docker_image(IMAGE_URI)
        if res["status"] != 1:
            spinner.text = "Pulling Docker image..."
            res = pull_docker_image(IMAGE_URI)
            if res["status"] != 1:
                spinner.fail(f"Error: {res['message']}")
                spinner.stop()
                return
            else:
                spinner.succeed(f"Success : {res['message']}")
        else:
            spinner.succeed(f"Success : {res['message']}")


        if(AWS_SECRET_ACCESS_KEY == "" or AWS_ACCESS_KEY_ID == ""):
            spinner.fail(f"Error: AWS Access Key ID or Secret Access Key is not set.")
            spinner.stop()
            return
        # docker run
        thing_name = f"{uuid.uuid4()}"
        spinner.text = "Running Docker container..."
        res = run_docker_container(
            IMAGE_URI,
            self.device_api.client_id,
            thing_name,
            AWS_REGION,
            AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY=AWS_SECRET_ACCESS_KEY,
            AWS_SESSION_TOKEN=AWS_SESSION_TOKEN,
        )
        if res["status"] != 1:
            spinner.fail(f"Error: {res['message']}")
            spinner.stop()
            return {
                "status": -1,
                "message": res["message"],
            }
        else:
            spinner.succeed(f"Success : {res['message']}")
            spinner.stop()
            return {
                "status": 1,
                "message": f"Docker container {thing_name} started successfully.",
                "thing_name": thing_name,
                "client_id": self.device_api.client_id,
                "aws_region": AWS_REGION,
            }
