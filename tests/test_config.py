import os.path

import pytest
from click.testing import CliRunner

from src.gols import Config, cli


@pytest.fixture()
def t_config():
    t = Config()

    return t


def test_config_created(t_config):
    runner = CliRunner()
    result = runner.invoke(cli(t_config), )
