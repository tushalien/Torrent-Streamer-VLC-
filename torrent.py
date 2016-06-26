#!/usr/bin/env python
from __future__ import print_function
import os
import requests
from bs4 import BeautifulSoup
import argparse

# Version Independent
import sys

if (sys.version_info > (3, 0)):
    from urllib.parse import quote_plus as qp
    raw_input = input
else:
    from urllib import quote_plus as qp


def open_url(url, hdr={}):
	"""For use in a proxy network"""

    http_proxy  = os.environ.get("HTTP_PROXY")
    https_proxy = os.environ.get("HTTPS_PROXY")
    ftp_proxy   = os.environ.get("FTP_PROXY")

    proxyDict = { 
        "http"  : http_proxy,
        "https" : https_proxy,
        "ftp"   : ftp_proxy
        }

    html = requests.get(url, headers=hdr, proxies=proxyDict)
    return html


def list_torrents(torrents):
	""" List all the find torrents in a more teadable format"""

    for title, (torrent_link, _) in enumerate(torrents):
        yield '[{}] {}'.format(title, torrent_link)



def get_torrent_list(search_url):
    """Fetches a list of top torrents ."""

    torrent_search = open_url(search_url)
    soup = BeautifulSoup(torrent_search.text, 'html.parser')
    torrent_results = soup.find_all("a", class_="cellMainLink")
    return [(x.text.encode('utf-8'), x.get('href')) for x in torrent_results]


def get_search_term():
	"""Takes the user input """

	parser = argparse.ArgumentParser(description='Stream torrents directly ')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-s', action='store', nargs='+', dest='music',  help='Stream the movie.')
	group.add_argument('-m', action='store',  nargs='+', dest='movie', help='Play the song .')
	group.add_argument('-t', action='store',  nargs='+', dest='tv',  help='Steam the tv show specified.')

	search_term = parser.parse_args()

	if search_term.music:
		search = ' '.join(search_term.music)
		return (search + ' category:music')

	if search_term.movie:
		search = ' '.join(search_term.movie)
		return (search + ' category:movie')

	if search_term.tv:
		search = ' '.join(search_term.tv)
		return (search + ' category:tv')
	else:
		print ("Check your input !!")
		exit()


def main():
    """ Run the Program """

    query =qp(get_search_term())

    url = 'https://kat.cr/usearch/' + query

    try:
        print ('Searching....')
        torrent_list = get_torrent_list(url)
        print (torrent_list)

    except Exception as e:
        print (e)
        exit()

    print('Found:', '\n'.join(list_torrents(torrent_list)))

    try:
        choice = raw_input('Choose the torrent: ')

        while not(choice.isdigit()) or not(0 <= int(choice) < len(torrent_list)):
            print("Invalid Choice.  Try again!")
            choice = raw_input('Choose the torrent: ')

        title, torrent_link = torrent_list[int(choice)]

        user_choice = raw_input('Stream "%s"? (y/n) ' % title)

        if user_choice.upper() != "Y" :
            sys.exit()

    except:
        title, torrent_link = torrent_list[0]

    print ('Streaming Torrent: ' + title)

    final_url = 'https://kat.cr' + torrent_link
    torrent_page = open_url(final_url)
    soup = BeautifulSoup(torrent_page.text, 'html.parser')
    final = 'https:' + soup.find_all('a', class_='siteButton')[0].get('href')
    
    os.system('peerflix ' + final + ' -a --vlc')


if __name__ == '__main__':
    main()