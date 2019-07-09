# built-in
from argparse import ArgumentParser, REMAINDER
from pathlib import Path

# app
from ..config import builders
from ..controllers import DockerContainer
from .base import BaseCommand


class DockerPrepareCommand(BaseCommand):
    """Make docker container nice.
    """
    @classmethod
    def get_parser(cls) -> ArgumentParser:
        parser = cls._get_default_parser('command')
        builders.build_config(parser)
        builders.build_from(parser)
        builders.build_venv(parser)
        builders.build_output(parser)
        builders.build_other(parser)
        parser.add_argument('name', nargs=REMAINDER, help='command to run')
        return parser

    def __call__(self) -> bool:
        script_path = Path(__file__).parent.parent / 'templates' / 'docker_prepare.sh'

        container = DockerContainer(
            path=Path(self.config['project']),
            env=self.config.env,
            repository=self.config['docker']['repo'],
            tag=self.config['docker']['tag'],
        )
        if not container.exists():
            self.logger.warning('creating container...', extra=dict(
                container=container.container_name,
            ))
            container.create()

        self.logger.info('running...', extra=dict(
            container=container.container_name,
        ))
        container.run(['sh', '-c', script_path.read_text()])
        self.logger.info('ready')
        return True
