import argparse
import os

import utils
import cat
import ls
import mv
import rm
import touch
import tree

if __name__ == '__main__':

    parser = argparse.ArgumentParser('gh')
    parser.add_argument('command', choices=['cat', 'ls', 'mv', 'rm', 'touch', 'tree'])
    parser.add_argument('-u', '--username', default='keggsmurph21')
    parser.add_argument('repo')
    parser.add_argument('-b', '--branch', default='master')
    parser.add_argument('paths', nargs='*')
    parser.add_argument('--password', default=None)
    parser.add_argument('--token', default=os.environ.get('GITHUB_TOKEN'))
    parser.add_argument('--is-private', action='store_true')
    args = parser.parse_args()

    utils.register_state(
            username=args.username,
            password=args.password,
            token=args.token,
            repo=args.repo,
            branch=args.branch
    )

    commands = dict(
            cat=cat,
            ls=ls,
            mv=mv,
            rm=rm,
            touch=touch,
            tree=tree
    )

    commands.get(args.command).main(args)

