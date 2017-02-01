import logging
import pytest
from click.testing import CliRunner
from ..gols.gols import upload, cli
from testfixtures import LogCapture


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
    result = runner.invoke(cli, ['upload', fs])
    assert result.exit_code == 2
    assert 'Error: Missing option' in result.output


def test_ok(runnerfs):
    runner, fs = runnerfs
    with LogCapture() as l:
        logger = logging.getLogger()
        result = runner.invoke(cli, ['upload', '-d', fs])
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



