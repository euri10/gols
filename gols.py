import os
import sys
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

import click
import logging
import requests
from utils.hidden_password import HiddenPassword

logger = logging.getLogger(__name__)
logging.basicConfig()


@click.command(short_help='uploads .fit files to your garmin connect account')
# @click.option('--username', '-u',  # prompt=True,
#               default=lambda: os.environ.get('GARMIN_CONNECT_USER', ''),
#               help='Defaults to GARMIN_CONNECT_USER environment variable')
# @click.option('--password', '-p',  # prompt=True,
#               default=lambda: HiddenPassword(
#                   os.environ.get('GARMIN_CONNECT_PASSWORD', '')),
#               help='Defaults to GARMIN_CONNECT_USER environment variable',
#               hide_input=True)
@click.option('--directory_fit', '-d', required=True, type=click.Path(exists=True, file_okay=False), help='Path of your .fit files on your watch mount path')
@click.option('--notification/--no_notification', '-n', default=False, help='Get notified')
@click.option('--move/--no_move', '-m', default=False, help='Move files upon upload')
@click.option('--debug/--no_debug', default=False, help='Set to true to see debug logs on top of info')
def upload(debug, directory_fit, notification, move):
    # do we need output ?
    if debug:
        from http.client import HTTPConnection
        HTTPConnection.debuglevel = 1
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
        logging.root.setLevel(level=logging.DEBUG)
    else:
        logger.setLevel(level=logging.INFO)

    # config loading
    conf_file_path, conf_dir_fit = init()
    config = parse_config_or_create_new(conf_file_path)
    username = config['username']
    password = config['password']

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

    #begin session with headers because, requests client isn't an option, dunno if Icewasel is still banned...
    logger.info('Login into Garmin connect')
    s = requests.session()
    s.headers.update(headers)
    # we need the cookies from the login page before we can post the user/pass
    url_login = 'https://sso.garmin.com/sso/login'
    req_login = s.get(url_login, params=params_login)
    if req_login.status_code != 200:
        logger.info('issue with {}, you can turn on debug for more info'.format(req_login))
    req_login2 = s.post(url_login, data=data_login)
    if req_login2.status_code != 200:
        logger.info('issue with {}, you can turn on debug for more info'.format(req_login2))
    # we need that to authenticate further, kind like a weird way to login but...
    t = req_login2.cookies.get('CASTGC')
    t = 'ST-0' + t[4:]
    # now the auth with the cookies we got
    # url_post_auth = 'https://connect.garmin.com/modern' this one I still don't know how to get it
    url_post_auth = 'https://connect.garmin.com/post-auth/login'
    params_post_auth = {'ticket': t}
    req_post_auth = s.get(url_post_auth, params=params_post_auth)
    if req_post_auth.status_code != 200:
        logger.info('issue with {}, you can turn on debug for more info'.format(req_post_auth))
    logger.info('Let\'s upload stuff now')
    # login should be done we upload now
    url_upload = 'https://connect.garmin.com/proxy/upload-service-1.1/json/upload/.fit'
    for filename in os.listdir(directory_fit):
        logger.info('uploading:  {}'.format(filename))
        files = {'data': (filename,
                          open(os.path.join(directory_fit, filename), 'rb'),
                          'application/octet-stream')
                 }
        req5 = s.post(url_upload, files=files)
        if req5.status_code != 200:
            logger.info('issue with {}, you can turn on debug for more info'.format(req5))

        fn = req5.json()['detailedImportResult']['fileName']
        if 'failures' in req5.json()['detailedImportResult']:
            for failure in req5.json()['detailedImportResult']['failures']:
                m_failures = failure['messages'][0]['content']
                logger.info(m_failures)
                if notification:
                    Notify.init('gols')
                    message = u'{} upload failed\n{}\n'.format(fn, m_failures)
                    notif = Notify.Notification.new('gols', '--FAILURE--\n'+message)
                    # notif.set_urgency(Notify.Urgency.CRITICAL)
                    notif.show()
        if 'successes' in req5.json()['detailedImportResult']:
            for successes in req5.json()['detailedImportResult']['successes']:
                m_success = 'https://connect.garmin.com/modern/activity/'+str(successes['internalId'])
                logger.info(m_success)
                if notification:
                    Notify.init('gols')
                    message = '--SUCCESS--\n{} upload succeeded\n{}\n'.format(fn, m_success)
                    notif = Notify.Notification.new('gols', message)
                    # notif.set_urgency(Notify.Urgency.CRITICAL)
                    notif.show()
        if move:
            shutil.move(os.path.join(directory_fit, filename), os.path.join(conf_dir_fit, filename))
    Notify.uninit()

def parse_config_or_create_new(conf_file_path):
    if not os.path.isfile(conf_file_path):
        logger.info('no config file found, if you press Y/y next it will prompt for you to change it')
        if click.confirm('Fill the required info or edit the {} file yourself and restart, No will stop'.format(conf_file_path)):
            with open(conf_file_path, 'w') as ymlfile:
                username = click.prompt('enter you Garmin Connect username')
                password = click.prompt('enter you Garmin Connect username', hide_input=True)
                yaml.dump({'username': username, 'password': password}, ymlfile, default_flow_style=False)
        else:
            with open(conf_file_path, 'w') as ymlfile:
                yaml.dump({'username': 'username', 'password': 'password'}, ymlfile, default_flow_style=False)
            logger.info('{} created, you need to fill them now')
    else:
        with open(conf_file_path, 'r') as ymlfile:
            config = yaml.load(ymlfile)
        return config


def init():
    logger.info('getting configuration parameters or creating them')
    if os.environ.get('XDG_CONFIG_HOME') is None or os.environ.get('XDG_CONFIG_HOME') == '':
        XDG_CONFIG_HOME = os.path.join(os.path.expanduser('~'), '.config')
    else:
        XDG_CONFIG_HOME = os.environ.get('XDG_CONFIG_HOME')
    CONF_DIR_PATH = os.path.join(XDG_CONFIG_HOME, 'gols')
    CONF_DIR_FIT = os.path.join(CONF_DIR_PATH, 'fit')
    CONF_FILE_PATH = os.path.join(CONF_DIR_PATH, 'config.yaml')

    if not os.path.exists(CONF_DIR_PATH):
        os.makedirs(CONF_DIR_PATH)
    if not os.path.exists(CONF_DIR_FIT):
        os.makedirs(CONF_DIR_FIT)
    return CONF_FILE_PATH, CONF_DIR_FIT

if __name__ == '__main__':
    upload()