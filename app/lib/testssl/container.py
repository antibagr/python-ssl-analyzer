import io
import json
import pathlib
import tarfile
import typing as t

import docker
import requests
from docker.models.containers import Container
from loguru import logger

from app.dto.annotations import TestSSLRecords


class TestSSLContainer:
    def __init__(
        self,
        *,
        client: docker.DockerClient,
        container_name: str,
        workdir: pathlib.Path,
        output_directory: pathlib.Path,
        commands_file_name: pathlib.Path,
    ) -> None:
        self._client = client
        self._container_name = container_name
        self._workdir = workdir
        self._output_directory = output_directory
        self._commands_file_name = commands_file_name

    @property
    def container(self) -> Container:
        return self._client.containers.get(self._container_name)

    def stop(self) -> None:
        self.container.stop()

    def wait_for_complete(self) -> None:
        try:
            logger.info("Waiting for container to complete")
            # TODO: (a.bagrianov): Run ThreadPoolExecutor
            # and parse simultaneously as data is being streamed
            # Hint: We know for sure that the script is done when
            # we got a record with id == "scanTime"
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

    def stream_data(self) -> t.Generator[TestSSLRecords, None, None]:
        # TODO: (a.bagrianov): Just use shared volume instead...
        logger.info(
            f"Streaming data from {self._container_name}:{self._workdir / self._output_directory}"
        )
        tar_gz, _ = self.container.get_archive(
            self._workdir / self._output_directory, encode_stream=True
        )

        full_tar_gz = io.BytesIO(b"".join(tar_gz))

        with tarfile.open(fileobj=full_tar_gz, mode="r") as tar:
            for member in tar.getmembers():
                if member.isfile():
                    data = tar.extractfile(member)
                    if data:
                        yield t.cast(TestSSLRecords, json.loads(data.read()))
