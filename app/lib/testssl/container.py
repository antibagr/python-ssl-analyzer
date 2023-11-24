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
        workdir: pathlib.Path,
        output_file_name: pathlib.Path,
        commands_file_name: pathlib.Path,
    ) -> None:
        self._client = client
        self._container_name = container_name
        self._workdir = workdir
        self._output_file_name = output_file_name
        self._commands_file_name = commands_file_name

    @property
    def container(self) -> Container:
        return self._client.containers.get(self._container_name)

    def stop(self) -> None:
        self.container.stop()

    def wait_for_complete(self) -> None:
        try:
            logger.info("Waiting for container to complete")
            _, output = self.container.exec_run(
                f"parallel --jobs 16 --bar -a {self._commands_file_name.as_posix()}",
                tty=True,
                stream=True,
                user="testssl_user",
                workdir=self._workdir.as_posix(),
            )
            for line in output:
                logger.info(line.decode("utf-8").strip())
            logger.info("Finished executing commands")
        except requests.exceptions.ReadTimeout:
            logger.error("Container timeout")
            self.container.kill()

    def get_json(self) -> list[TestSSLRecord]:
        logger.info(self._workdir / self._output_file_name.name)
        tar_gz, _ = self.container.get_archive(
            self._workdir / self._output_file_name.name, encode_stream=True
        )

        with tarfile.open(
            fileobj=io.BytesIO(b"".join(tar_gz)),
            mode="r",
        ) as tar:
            try:
                if _file := tar.extractfile(self._output_file_name.name):
                    json_bytes = _file.read()
                else:
                    raise KeyError
            except KeyError:
                logger.error("No file in tar archive")
                return []
        return t.cast(list[TestSSLRecord], json.loads(json_bytes))
