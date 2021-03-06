# coding: utf-8
import os
import sys
import time

import tihldelib.userlib as lib

__author__ = 'Harald Floor Wilhelmsen'


def get_useramount():
    formatstring = 'Format: python lan_users.py useramount'

    # Checking if there are sufficient arguments, if not exit
    if len(sys.argv) != 2:
        sys.exit('Invaild number of arguments. ' + formatstring)

    user_amount = sys.argv[1].strip()

    if not user_amount.isdigit():
        sys.exit('Wrong number-format. ' + formatstring)

    return user_amount, int(input('Start id of user id'))


def create_lan_users():
    user_amount, start_id = get_useramount()

    response = str(input(str(user_amount) + ' users to add. Continue? [y/N]'))
    if response.replace('\n', '').strip() != 'y':
        return 'User called exit before adding users'

    api = lib.get_ipa_api()
    username_format = 'lan-{}'

    credentials_file_path = '/root/lan_users{}.txt'.format(time.time())
    with open(credentials_file_path, 'a') as credentials_file:
        for i in range(start_id, start_id + user_amount):
            username = username_format.format(i)
            user_info = lib.add_user_ipa(username=username, firstname='Lan', lastname='Lanesen', groupid=1002,
                                         homedir_base='/home/lan/', api=api)
            credentials_file.write('Brukernavn: {0}\nPassord: {1}\n\n'.format(username, user_info[1]))


def main():
    euid = os.geteuid()
    if euid != 0:
        print('Needs to be run as root. Re-run with sudo')
        return
    msg = create_lan_users()
    if msg:
        print(msg)
        return


main()
