# coding=utf-8
import json
import re
import sys
import pycurl
from urllib import urlencode, unquote

import datetime
import requests

links = {}
locations = {}
cookies = {
    'Set-Cookie': [],
}
flags = {
    'is_post': True,
}
headers = [
    'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language: en-US;q=0.8',
    'Connection: keep-alive',
    'User-Agent: Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 ' +\
    '(KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
]
url = 'https://auth.aiesec.org/users/sign_in'


def get_curl(url, header_function, *extra_headers):
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.HTTPHEADER, headers + list(extra_headers))
    curl.setopt(pycurl.SSL_VERIFYPEER, 0)
    curl.setopt(pycurl.SSL_VERIFYHOST, 0)
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.MAXREDIRS, 5)
    curl.setopt(pycurl.HEADERFUNCTION, header_function)
    curl.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/' +\
                    '537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36')
    return curl


def call_needed_redirect():
    if locations.get('location'):
        location = locations['location']
        curl = get_curl(location, header_function, cookies['Set-Cookie'][0])
        curl.setopt(pycurl.FOLLOWLOCATION, 0)
        curl.perform()
        curl.close()
        curl = get_curl(links['token'], header_function)
        curl.setopt(pycurl.FOLLOWLOCATION, 0)
        curl.perform()
        curl.close()
        parts = links['found'].split('=')
        if len(parts) > 1:
            token = parts[1]
        else:
            token = parts[0]
        links['found'] = token
        pass


def header_function(line):
    # print line
    if "Location" in line and "redirect" in line and 'response_type' in line:
        location = line.split(' ')[1]
        unquoted = unquote(location)
        unquoted = unquoted[:len(unquoted) - 2]
        print unquoted
        locations['location'] = unquoted
    ######################################################
    if 'Set-Cookie' in line and flags['is_post'] and 'gis' in line:
        parts = line.split('; ')
        id_session = parts[0].replace('Set-Cookie', 'Cookie')
        cookies['Set-Cookie'] = [id_session + '; request-method=POST',]
        flags['is_post'] = False
    ######################################################
    if 'sign_in?code' in line and not links.get('token'):
        link = line.split(' ')[1]
        link = link[:len(link) - 2]
        links['token'] = link
    ######################################################
    if 'token' in line:
        token = line.split(' ')[1]
        token = token[:len(token) - 1]
        links['found'] = token
    pass


def login(email, password):
    data = (
        ('user[email]', email),
        ('user[password]', password),
    )
    formdata = urlencode(data)

    c = get_curl(url, header_function)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.POSTFIELDS, formdata)
    c.perform()
    c.close()

    call_needed_redirect()

    if links.get('found'):
        return links['found']
    else:
        return None


def logout():
    pass