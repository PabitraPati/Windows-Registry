'''
Given a registry constant and one of it's key,
find out the subkeys and values for the same.

This code works for both Python 2.7 as well as Python 3.5

author :- Pabitra Kumar Pati
'''

import logging

logging.basicConfig(filename="Registry_Read.log",filemode='w', level=logging.INFO)
log = logging.getLogger("Registry_Read.py")

from sys import version_info
if version_info[0] < 3:
    from _winreg import *
else:
    from winreg import *
log.info("Python version :- {}".format(version_info))


class Registry_Read():

    def __init__(self, const):
        self.const = const

    def get_subkeys(self, keypath):
        '''
        This method traverses the Sub-Keys present for the given key.

        Arguments :-
        keypath :-
             keypath for the key you want to access.
             E.g. :- If you want to get the keys and subkeys for
             'HKEY_LOCAL_MACHINE\SOFTWARE\Intel',
             then your keypath will be '\SOFTWARE\Intel',
             'HKEY_LOCAL_MACHINE' being the Registry Constant.
        '''
        # UAC does not provide KEY_ALL_ACCESS on Constants HKEY_CLASSES_ROOT and HKEY_LOCAL_MACHINE
        try:
            ob = OpenKey(self.const, keypath, 0, KEY_READ)
            keys = self.get_subattribs('key', ob)
        except Exception as e:
            log.error("Exception occured :- {}, key path :- {}".format(e, keypath))
        return keys

    def get_values(self, keypath):
        '''
        For a given keypath, this method reads each values and
        returns a list of values for the same key
        to the calling method

        Arguments :-
        keypath :-
             keypath for the key you want to access.
             E.g. :- If you want to get the keys and subkeys for
             'HKEY_LOCAL_MACHINE\SOFTWARE\Intel',
             then your keypath will be '\SOFTWARE\Intel',
             'HKEY_LOCAL_MACHINE' being the Registry Constant.
        '''
        try:
            with OpenKey(self.const, keypath, 0, KEY_READ) as subkey:
                v = self.get_subattribs('values',subkey)
        except Exception as e:
            log.error("Exception occured :- {}, key path :- {}".format(e, keypath))
        return v

    def get_subattribs(self, attrib_name, ob):
        '''
        Iterates over the given registry attribute (key or value)
        And returns the respective subkeys or values.

        Arguments :-
        attrib_name :-
              whether you want to get key or value
              Can either be 'key' or 'value'
        ob :- handle of the key opened for accessing.
        '''
        count = 0
        attrib = []
        while True:
            try:
                subattribs = EnumKey(ob, count) if attrib_name is 'key' else EnumValue(ob, count)
                attrib.append(subattribs)
                count+=1
            except WindowsError as e:
                break
        return attrib



obj = Registry_Read(HKEY_CURRENT_USER)

keypath1 = r'SOFTWARE\Skype'
log.info(
    "Subkeys for given key {} are {} ".format(
    keypath1, obj.get_subkeys(keypath1)))

keypath2=r'SOFTWARE\Skype\Phone\UI'
log.info(
    "Values for given key {} are {} ".format(
    keypath2, obj.get_values(keypath2)))