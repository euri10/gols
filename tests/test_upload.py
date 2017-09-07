import os

import pytest
from click.testing import CliRunner
from testfixtures import LogCapture

from gols.cli import main
from gols.cli import upload


@pytest.fixture(scope='function')
def runner():
    yield CliRunner()


@pytest.fixture(scope='function')
def fs():
    if not os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', 'directory_fit')):
        os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', 'directory_fit'))
    yield os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', 'directory_fit')


@pytest.fixture(scope='function')
def cdf():
    if not os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', 'conf_dir_fit')):
        os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', 'conf_dir_fit'))
    yield os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', 'conf_dir_fit')


def test_debug_turned_on(runner):
    with LogCapture() as l:
        result = runner.invoke(main, ['--debug', 'upload'])
        assert result.exit_code == 2
        assert 'Debug level set on' in str(l)


def test_debug_turned_off(runner):
    with LogCapture() as l:
        result = runner.invoke(main, ['upload'])
        assert result.exit_code == 2
        assert 'Info level set on' in str(l)


def test_upload_help(runner):
    result = runner.invoke(upload, ['--help'])
    assert result.exit_code == 0
    assert 'Usage' in result.output


def test_required_fit_directory(runner, fs):
    result = runner.invoke(upload, ['upload', fs])
    assert result.exit_code == 2
    assert 'Error: Missing option' in result.output


def test_upload_fit(runner, fs, cdf):
    username = 'gols@mailinator.com'
    password = 'G0lsG0ls'
    with LogCapture() as l:
        # logger = logging.getLogger()
        result = runner.invoke(main, ['--debug', 'upload', '-d', fs, '-c', cdf, '-u', username, '-p', password])  # noqa
        print(result.output)
        print(l)
        assert result.exit_code == 0
        assert 'Done uploading' in str(l)
