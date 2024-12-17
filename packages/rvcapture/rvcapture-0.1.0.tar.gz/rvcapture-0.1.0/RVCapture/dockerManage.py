import subprocess


class DockerManage:

    @staticmethod
    def get_docker_status():
        """
        Get the status of the docker container.
        """
        try:
            subprocess.run(
                ["docker", "info"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            return {
                "status" : 1,
                "message" : "Docker is running."
            }
        except subprocess.CalledProcessError:
            return {
                "status" : 0,
                "message" : "Docker is not running."
            }
        except FileNotFoundError:
            return {
                "status" : -1,
                "message" : "Docker is not installed."
            }
        except Exception as e:
            return {
                "status" : -1,                
                "message" : e
            }

    @staticmethod
    def get_docker_containers():
        """
        Get a list of running docker containers.
        """
        dockerStatus = DockerManage.get_docker_status()
        if dockerStatus["status"] != 1:
            return dockerStatus

        try:
            result = subprocess.run(
                ["docker", "ps", "-a", "--no-trunc"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
            containers = result.stdout.split("\n")
            return {
                "status" : 1,
                "message" : containers
            }
        except subprocess.CalledProcessError:
            return {
                "status" : 0,
                "message" : "Unable to retrieve containers."
            }
        except Exception as e:
            return {
                "status" : -1,                
                "message" : e
            }
