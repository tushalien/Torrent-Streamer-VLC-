import argparse
import sys

parser = argparse.ArgumentParser(description='Stream torrents directly ')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-s', action='store', nargs='+', dest='music',  help='Stream the movie.')
group.add_argument('-m', action='store',  nargs='+', dest='movie', help='Play the song .')
group.add_argument('-t', action='store',  nargs='+', dest='tv',  help='Steam the tv show specified.')

# Parse and check arguments
search_term = parser.parse_args()


if results.music:

    print results.music
    #print("music" + str(query))
if results.movie:
    print results.movie
if results.tv:
	str1 = ' '.join(results.tv)
	print results.tv
	print str1
