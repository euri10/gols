import os

import pytest
from click.testing import CliRunner
from testfixtures import LogCapture

from gols.cli import cli
from gols.cli import upload


@pytest.fixture(scope='function')
def runner():
    yield CliRunner()


@pytest.fixture(scope='function')
def fs():
    yield os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', 'directory_fit')


@pytest.fixture(scope='function')
def cdf():
    yield os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', 'conf_dir_fit')


def test_debug_turned_on(runner):
    with LogCapture() as l:
        result = runner.invoke(cli, ['--debug', 'upload'])
        assert result.exit_code == 2
        assert 'Debug level set on' in str(l)


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
        result = runner.invoke(cli, ['--debug', 'upload', '-d', fs, '-c', cdf,
                                     '-u', username, '-p', password])
        print(result.output)
        print(l)
        assert result.exit_code == 0
        assert 'Done uploading'.format(fs) in str(l)


# @pytest.mark.parametrize('args, expected_output, expected_exit_code',
#                          [('', 'Error: Missing option', 2),
#                           (['-d /tmp'], 'Error: Invalid value for', 2),
#                           (['-d'],'',0)
#                           ])
# def test_upload_args(runnerfs, args, expected_output, expected_exit_code):
#     runner, fs = runnerfs
#     print(fs)
#     result = runner.invoke(upload, args=args)
#     assert result.exit_code == expected_exit_code
#     print(result.output)
#     assert expected_output in result.output
