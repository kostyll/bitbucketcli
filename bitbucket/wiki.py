import logging
import requests
import os
import sys
import getpass
import json
import imp
import argparse
import prettytable
from os.path import expanduser
from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne


home = expanduser("~")
filename = os.path.join(home, '.bitbucket.py')
creds = imp.load_source('.bitbucket', filename)
user = creds.username
passwd = creds.passwd


class Wikiget(Command):
	log = logging.getLogger(__name__ + '.Wikiget')
			
	def get_parser(self, prog_name):
		parser = super(Wikiget, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		parser.add_argument('--page', '-p', metavar='<page name>', required=True, help='The page title')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		url = "https://bitbucket.org/api/1.0/repositories/%s/%s/wiki/%s/" % (parsed_args.account,parsed_args.reponame,parsed_args.page)
		r = requests.get(url, auth=(user, passwd))
		if r.status_code == 200:
			data = json.loads(r.text)
			print "\nMarkup: %s\n" % (data['markup'])
			print "Revision: %s\n" %  (data['rev'])
			print "Page Content: %s\n" % (data['data'])
		else:
			print "\n Error: '404' No Wiki Pages Found 'or' Invalid argument supplied.\n"
			sys.exit(1)


class Wikipost(Command):
	log = logging.getLogger(__name__ + '.Wikipost')
			
	def get_parser(self, prog_name):
		parser = super(Wikipost, self).get_parser(prog_name)
		parser.add_argument('--account', '-a', metavar='<account name>', required=True, help='Your account name')
		parser.add_argument('--reponame', '-r', metavar='<repo name>', required=True, help='The repository name')
		parser.add_argument('--page', '-p', metavar='<page name>', required=True, help='The page title')
		parser.add_argument('--content', '-c', metavar='<page content>', required=True, help='The page content')
		return parser

	def take_action(self,parsed_args):
		self.log.debug('take_action(%s)' % parsed_args)

		args = {}
		args['content'] = parsed_args.content

		url = "https://bitbucket.org/api/1.0/repositories/%s/%s/wiki/%s/" % (parsed_args.account,parsed_args.reponame,parsed_args.page)
		r = requests.post(url, data=args, auth=(user, passwd))
		if r.status_code == 200:
			data = json.loads(r.text)
			print "\n Wiki Page Created Successfully.\n"
		else:
			print "\n Error: '%s' Something Went Wrong -- Bitbucket.\n" % (r.status_code)
			sys.exit(1)