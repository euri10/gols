import os

import pytest
from click.testing import CliRunner
from testfixtures import LogCapture

from gols.cli import cli
from gols.cli import upload


@pytest.fixture(scope='function')
def runnerfs(request):
    runner = CliRunner()
    with runner.isolated_filesystem() as fs:
        yield runner, fs


@pytest.fixture(scope='function')
def cdf():
    fit = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fit')
    return fit


def test_debug_turned_on(runnerfs):
    runner, fs = runnerfs
    with LogCapture() as l:
        result = runner.invoke(cli, ['--debug', 'upload'])
        assert result.exit_code == 2
        assert 'Debug level set on' in str(l)


def test_upload_help(runnerfs):
    runner, fs = runnerfs
    result = runner.invoke(upload, ['--help'])
    assert result.exit_code == 0
    assert 'Usage' in result.output


def test_required_fit_directory(runnerfs):
    runner, fs = runnerfs
    result = runner.invoke(upload, ['upload', fs])
    assert result.exit_code == 2
    assert 'Error: Missing option' in result.output


def test_no_file_found(runnerfs, cdf, monkeypatch):
    monkeypatch.setenv('GARMINCONNECT_USERNAME', 'gols@mailinator.com')
    monkeypatch.setenv('GARMINCONNECT_PASSWORD', 'G0lsG0ls')
    runner, fs = runnerfs
    with LogCapture() as l:
        # logger = logging.getLogger()
        result = runner.invoke(cli, ['--debug', 'upload', '-d', fs, '-c', cdf])
        print(l)
        assert result.exit_code == 0
        assert 'No file found in {}'.format(fs) in str(l)


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
