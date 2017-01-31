
import pytest
from click.testing import CliRunner
from ..gols.gols import upload, cli


@pytest.fixture(scope='function')
def runnerfs(request):
    runner = CliRunner()
    with runner.isolated_filesystem() as fs:
        yield runner, fs


def test_upload_help(runnerfs):
    runner, fs = runnerfs
    result = runner.invoke(upload, ['--help'])
    assert result.exit_code == 0
    assert 'Usage' in result.output


def test_required_fit_directory(runnerfs):
    runner, fs = runnerfs
    result = runner.invoke(upload)
    assert result.exit_code == 2
    assert 'Error: Missing option' in result.output


@pytest.mark.parametrize('args, expected_output, expected_exit_code',
                         [('', 'Usage: upload [OPTIONS]\n\nError: Missing option "--directory_fit" / "-d".\n', 2),
                          (['-d /tmp'], 'Error: Invalid value for', 2),
                          (['-d '],'',2)
                          ])
def test_upload_args(runnerfs, args, expected_output, expected_exit_code):
    runner, fs = runnerfs
    result = runner.invoke(upload, args=args)
    assert result.exit_code == expected_exit_code
    assert expected_output in result.output



