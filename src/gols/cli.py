"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mgols` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``gols.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``gols.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import click

import os
import sys
import logging
import click
import requests
import shutil
import yaml

try:
    import gi
    from gi.repository import GLib
except ImportError as e:
    print('Dependency missing: python-gobject')
    print(e)
    sys.exit(1)
try:
    gi.require_version('Notify', '0.7')
    from gi.repository import Notify
except (ImportError, ValueError) as e:
    print('Dependency missing: libnotify')
    print(e)
    sys.exit(1)

logger = logging.getLogger(__name__)
logging.basicConfig()


class Config(dict):
    def __init__(self):
        self.template = {'username': 'username', 'password': 'password'}
        self.path = self._create_or_load(click.get_app_dir('gols'),
                                         'config.yaml')
        self.conf_dir_fit = self._conf_dir_fit(click.get_app_dir('my_app'),
                                               'fit')
        super(Config, self).__init__()

    @staticmethod
    def _conf_dir_fit(app_directory, directory):
        conf_dir_fit = os.path.join(app_directory, directory)
        if not os.path.exists(conf_dir_fit):
            os.makedirs(conf_dir_fit)
        return conf_dir_fit

    @staticmethod
    def _create_or_load(directory, fn):
        if os.path.exists(os.path.join(directory, fn)):
            return os.path.join(directory, fn)
        else:
            if not os.path.exists(directory):
                os.makedirs(directory)
                with open(os.path.join(directory, fn), 'w') as ymlfile:
                    yaml.dump({'username': 'username', 'password': 'password'},
                              ymlfile, default_flow_style=False)
                return os.path.join(directory, fn)

    def load(self):
        with open(self.path, 'r') as ymlfile:
            self.configdict = yaml.load(ymlfile)
            if self.configdict == self.template:
                if click.confirm(
                        'the config file {} has been created, edit it please'.format(
                                self.path), abort=True):
                    with open(self.path, 'w') as ymlfile:
                        username = click.prompt(
                            'enter you Garmin Connect username')
                        password = click.prompt(
                            'enter you Garmin Connect password',
                            hide_input=True)
                        yaml.dump({'username': username, 'password': password},
                                  ymlfile, default_flow_style=False)
                    self.load()


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@pass_config
@click.option('--debug/--no_debug', default=False,
              help='Set to true to see debug logs on top of info')
def cli(config, debug):
    config.load()
    if debug:
        from http.client import HTTPConnection
        HTTPConnection.debuglevel = 1
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
        logging.root.setLevel(level=logging.DEBUG)
    else:
        logger.setLevel(level=logging.INFO)


@click.command(short_help='uploads .fit files to your garmin connect account')
@pass_config
@click.option('--directory_fit', '-d', required=True,
              type=click.Path(exists=True, file_okay=False),
              help='Path of your .fit files on your watch mount path')
@click.option('--notification/--no_notification', '-n', default=False,
              help='Get notified')
@click.option('--move/--no_move', '-m', default=False,
              help='Move files upon upload')
def upload(config, directory_fit, notification, move):
    username = config.configdict['username']
    password = config.configdict['password']
    conf_dir_fit = config.conf_dir_fit

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
    }
    params_login = {
        'service': 'https://connect.garmin.com/modern/',
        'webhost': 'olaxpw-conctmodern011',
        'source': 'https://connect.garmin.com/en-US/signin',
        'redirectAfterAccountLoginUrl': 'https://connect.garmin.com/modern/',
        'redirectAfterAccountCreationUrl': 'https://connect.garmin.com/modern/',
        'gauthHost': 'https://sso.garmin.com/sso',
        'locale': 'en_US',
        'id': 'gauth-widget',
        'cssUrl': 'https://static.garmincdn.com/com.garmin.connect/ui/css/gauth-custom-v1.2-min.css',
        'clientId': 'GarminConnect',
        'rememberMeShown': 'true',
        'rememberMeChecked': 'false',
        'createAccountShown': 'true',
        'openCreateAccount': 'false',
        'usernameShown': 'false',
        'displayNameShown': 'true',
        'consumeServiceTicket': 'false',
        'initialFocus': 'true',
        'embedWidget': 'false',
        'generateExtraServiceTicket': 'false',
        'globalOptInShown': 'false',
        'globalOptInChecked': 'false',
        'connectLegalTerms': 'true',
    }
    data_login = {
        'username': username,
        'password': password,
        'embed': 'true',
        'lt': 'e1s1',
        '_eventId': 'submit',
        'displayNameRequired': 'false',
        'rememberme': 'on',
    }

    # begin session with headers because, requests client isn't an option, dunno if Icewasel is still banned...
    logger.info('Login into Garmin connect')
    s = requests.session()
    s.headers.update(headers)
    # we need the cookies from the login page before we can post the user/pass
    url_login = 'https://sso.garmin.com/sso/login'
    req_login = s.get(url_login, params=params_login)
    if req_login.status_code != 200:
        logger.info('issue with {}, you can turn on debug for more info'.format(
            req_login))
    req_login2 = s.post(url_login, data=data_login)
    if req_login2.status_code != 200:
        logger.info('issue with {}, you can turn on debug for more info'.format(
            req_login2))
    # we need that to authenticate further, kind like a weird way to login but...
    t = req_login2.cookies.get('CASTGC')
    t = 'ST-0' + t[4:]
    # now the auth with the cookies we got
    # url_post_auth = 'https://connect.garmin.com/modern' this one I still don't know how to get it
    url_post_auth = 'https://connect.garmin.com/post-auth/login'
    params_post_auth = {'ticket': t}
    req_post_auth = s.get(url_post_auth, params=params_post_auth)
    if req_post_auth.status_code != 200:
        logger.info('issue with {}, you can turn on debug for more info'.format(
            req_post_auth))
    logger.info('Let\'s upload stuff now')
    # login should be done we upload now

    #url_upload = 'https://connect.garmin.com/proxy/upload-service-1.1/json/upload/.fit'
    url_upload = 'https://connect.garmin.com/modern/proxy/upload-service/upload/.fit'
    if len(os.listdir(directory_fit)):
        for filename in os.listdir(directory_fit):
            logger.info('uploading:  {}'.format(filename))
            files = {'data': (filename,
                              open(os.path.join(directory_fit, filename), 'rb'),
                              'application/octet-stream')
                     }
            s.headers.update({'Referer':'https://connect.garmin.com/modern/import-data', 'NK':'NT'})
            req5 = s.post(url_upload, files=files)
            if req5.status_code != 200:
                logger.info(
                    'issue with {}, you can turn on debug for more info'.format(
                        req5))

            fn = req5.json()['detailedImportResult']['fileName']
            if 'failures' in req5.json()['detailedImportResult']:
                for failure in req5.json()['detailedImportResult']['failures']:
                    m_failures = failure['messages'][0]['content']
                    logger.info(m_failures)
                    if notification:
                        Notify.init('gols')
                        message = u'{} upload failed\n{}\n'.format(fn,
                                                                   m_failures)
                        notif = Notify.Notification.new('gols',
                                                        '--FAILURE--\n' + message)
                        # notif.set_urgency(Notify.Urgency.CRITICAL)
                        notif.show()
            if 'successes' in req5.json()['detailedImportResult']:
                for successes in req5.json()['detailedImportResult']['successes']:
                    m_success = 'https://connect.garmin.com/modern/activity/' + str(
                        successes['internalId'])
                    logger.info(m_success)
                    if notification:
                        Notify.init('gols')
                        message = '--SUCCESS--\n{} upload succeeded\n{}\n'.format(
                            fn, m_success)
                        notif = Notify.Notification.new('gols', message)
                        # notif.set_urgency(Notify.Urgency.CRITICAL)
                        notif.show()
            if move:
                shutil.move(os.path.join(directory_fit, filename),
                            os.path.join(conf_dir_fit, filename))
        Notify.uninit()
        logger.info('Done uploading')
    else:
        logger.info('No file found in {}'.format(directory_fit))
    logger.info('Finished')
