import logging

import docker
from docker.errors import ContainerError, DockerException, NotFound

logger = logging.getLogger(__name__)


class DockerService:
    IMAGE_NAME = "ticketforge-sandbox"
    MEMORY_LIMIT = "2g"
    CPU_LIMIT = 1.0
    TIMEOUT_SECONDS = 300

    def __init__(self):
        self.client = docker.from_env()
        self._image_pulled = False

    def ensure_image(self) -> None:
        if getattr(self, "_image_pulled", False):
            return
        try:
            self.client.images.get(self.IMAGE_NAME)
            self._image_pulled = True
        except docker.errors.ImageNotFound:
            logger.info("Pulling sandbox image %s", self.IMAGE_NAME)
            self.client.images.pull(self.IMAGE_NAME)
            self._image_pulled = True

    async def create_sandbox(self, repo_url: str, branch: str = "main") -> str:
        self.ensure_image()
        container = self.client.containers.run(
            self.IMAGE_NAME,
            detach=True,
            network_mode="none",
            mem_limit=self.MEMORY_LIMIT,
            nano_cpus=int(self.CPU_LIMIT * 1e9),
            environment={
                "REPO_URL": repo_url,
                "BRANCH": branch,
            },
            remove=False,
        )
        logger.info("Created sandbox container %s for %s@%s", container.id[:12], repo_url, branch)
        return container.id

    async def exec_in_sandbox(self, container_id: str, command: str) -> str:
        try:
            container = self.client.containers.get(container_id)
            exit_code, output = container.exec_run(
                ["bash", "-c", command],
                demux=True,
            )
            stdout = output[0].decode("utf-8") if output[0] else ""
            stderr = output[1].decode("utf-8") if output[1] else ""
            if exit_code != 0:
                logger.warning(
                    "Command failed in %s (exit %d): %s", container_id[:12], exit_code, stderr
                )
            return stdout + stderr
        except (NotFound, ContainerError, DockerException) as e:
            logger.error("Exec failed in %s: %s", container_id[:12], e)
            raise

    async def get_diff(self, container_id: str) -> str:
        return await self.exec_in_sandbox(container_id, "cd /workspace && git diff")

    async def destroy_sandbox(self, container_id: str) -> None:
        try:
            container = self.client.containers.get(container_id)
            container.stop(timeout=10)
            container.remove(force=True)
            logger.info("Destroyed sandbox container %s", container_id[:12])
        except NotFound:
            logger.warning("Container %s already removed", container_id[:12])
        except DockerException as e:
            logger.error("Failed to destroy %s: %s", container_id[:12], e)
