import utils

def main(args):

    if not utils.repo_exists():
        raise utils.GHError('repo-exists', f'cannot stat "{args.repo}"')
  
    data = {
        'method': 'patch',
        'name': args.paths[0]
    }

    err, _ = utils.call(f'/repos/{args.username}/{args.repo}', data=data)
    if err:
        raise utils.GHError('repo-move', err)
