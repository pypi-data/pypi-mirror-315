import json
import os
import subprocess
import shutil
import platform


def loadAppConfig():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the absolute path to appConfigs.json
    config_path = os.path.join(current_dir, "appConfigs.json")
    
    # Load the configuration
    with open(config_path, "r") as f:
        appConfig = json.load(f)
    
    return appConfig

def getAppName():
    appConfig = loadAppConfig()["appConfig"]
    return appConfig["shortName"]


def detect_os():
    system = platform.system()
    if system == "Linux":
        return {"status": 1, "message": "Linux"}
    else:
        return {"status": -1, "message": f"Unsupported operating system: {system}"}


def check_command_availability(command: str):
    if not shutil.which(command):
        return False
    else:
        return True


def fetch_env_vars_for_add_device():
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")

    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        return {
            "status": -1,
            "message": "AWS Access Key ID and Secret Access Key must be set as environment variables.",
        }

    return {
        "status": 1,
        "message": {
            "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
            "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
            "AWS_SESSION_TOKEN": "" if not AWS_SESSION_TOKEN else AWS_SESSION_TOKEN,
        },
    }


def install_aws_cli():
    arch = subprocess.check_output(["uname", "-m"]).decode("utf-8").strip()
    if arch == "x86_64":
        aws_cli_url = "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"
    elif arch == "aarch64":
        aws_cli_url = "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip"
    else:
        return {"status": -1, "message": f"Unsupported architecture: {arch}"}

    try:
        subprocess.run(["curl", aws_cli_url, "-o", "awscliv2.zip"], check=True)
        subprocess.run(["unzip", "awscliv2.zip"], check=True)
        subprocess.run(
            [
                "sudo",
                "./aws/install",
                "--bin-dir",
                "/usr/local/bin",
                "--install-dir",
                "/usr/local/aws-cli",
            ],
            check=True,
        )
        subprocess.run(["rm", "-rf", "awscliv2.zip", "aws"], check=True)
    except Exception as e:
        return {"status": -1, "message": f"Error installing AWS CLI: {e.output}"}
    return {"status": 1, "message": "AWS CLI installed successfully."}


def authenticate_ecr(region: str, account_id: str):
    login_command = ["aws", "ecr", "get-login-password", "--region", region]
    docker_login_command = [
        "docker",
        "login",
        "--username",
        "AWS",
        "--password-stdin",
        f"{account_id}.dkr.ecr.{region}.amazonaws.com",
    ]

    try:
        login_process = subprocess.Popen(login_command, stdout=subprocess.PIPE)
        subprocess.run(docker_login_command, stdin=login_process.stdout, check=True)
        login_process.stdout.close()
    except Exception as e:
        return {"status": -1, "message": f"Error authenticating ECR: {e.output}"}
    return {"status": 1, "message": "ECR authenticated successfully."}


def pull_docker_image(image_uri: str):
    try:
        subprocess.run(["docker", "pull", image_uri], check=True)
    except Exception as e:
        return {"status": -1, "message": f"Error pulling image {image_uri}: {e.output}"}
    return {"status": 1, "message": f"Image {image_uri} pulled successfully."}


def check_docker_image(image_url: str):
    result = subprocess.run(
        ["docker", "images", "-q", image_url], stdout=subprocess.PIPE
    )

    if not result.stdout:
        return {
            "status": -1,
            "message": f"Image {image_url} not found locally. Pulling from ECR...",
        }
    else:
        return {
            "status": 1,
            "message": f"Image {image_url} is already available locally.",
        }


def run_docker_container(
    image_uri: str,
    client_id: str,
    thing_name: str,
    aws_region: str,
    AWS_ACCESS_KEY_ID: str,
    AWS_SECRET_ACCESS_KEY: str,
    AWS_SESSION_TOKEN: str,
):
    output_dir = f"/outputFiles/{thing_name}"
    os.makedirs(output_dir, exist_ok=True)

    docker_run_command = [
        "docker",
        "run",
        "-e",
        f"AWS_ACCESS_KEY_ID={AWS_ACCESS_KEY_ID}",
        "-e",
        f"AWS_SECRET_ACCESS_KEY={AWS_SECRET_ACCESS_KEY}",
        "-e",
        f"AWS_SESSION_TOKEN={AWS_SESSION_TOKEN}",
        "--privileged",
        "-e",
        f"CLIENT_ID={client_id}",
        "-e",
        f"THING_NAME={thing_name}",
        "-e",
        "PROVISION=true",
        "-e",
        f"AWS_REGION={aws_region}",
        "--volume",
        "/dev:/dev",
        "--device",
        "/dev/ttyUSB0:/dev/ttyUSB0",
        "--volume",
        f"{output_dir}:/outputFiles",
        "--name",
        thing_name,
        "-it",
        "-d",
        image_uri,
    ]

    try:
        subprocess.run(docker_run_command, check=True)
    except Exception as e:
        return {"status": -1, "message": f"Error running docker container: {e.output}"}

    return {
        "status": 1,
        "message": f"Docker container {thing_name} started successfully.",
    }
