import utils

def main(args):

    if not utils.repo_exists():
        raise utils.GHError('repo-exists', f'cannot stat "{args.repo}"')
 
    if len(args.paths) != 1:
        raise utils.GHError('repo-move', 'too many arguments')

    data = {
        'method': 'patch',
        'name': args.paths[0]
    }

    err, _ = utils.call(f'/repos/{args.username}/{args.repo}', data=data)
    if err:
        raise utils.GHError('repo-move', err)
