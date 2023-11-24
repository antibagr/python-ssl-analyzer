import io
import json
import pathlib
import tarfile
import typing as t

import docker
import requests
from docker.models.containers import Container
from loguru import logger

from app.dto.annotations import TestSSLRecord


class TestSSLContainer:
    def __init__(
        self,
        *,
        client: docker.DockerClient,
        container_name: str,
        output_path: pathlib.Path,
    ) -> None:
        self._client = client
        self._container_name = container_name
        self._output_path = output_path

    @property
    def container(self) -> Container:
        return self._client.containers.get(self._container_name)

    def stop(self) -> None:
        self.container.stop()

    def wait_for_complete(self) -> None:
        try:
            logger.info("Waiting for container to complete")
            self.container.wait()
        except requests.exceptions.ReadTimeout:
            logger.error("Container timeout")
            self.container.kill()

    def get_json(self) -> list[TestSSLRecord]:
        tar_gz, _ = self.container.get_archive(self._output_path, encode_stream=True)

        with tarfile.open(
            fileobj=io.BytesIO(b"".join(tar_gz)),
            mode="r",
        ) as tar:
            try:
                if _file := tar.extractfile(self._output_path.name):
                    json_bytes = _file.read()
                else:
                    raise KeyError
            except KeyError:
                logger.error("No file in tar archive")
                return []
        return t.cast(list[TestSSLRecord], json.loads(json_bytes))
