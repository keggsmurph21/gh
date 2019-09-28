import utils

def main(args):

    if not utils.repo_exists():
        raise utils.GHError('repo-exists', f'cannot stat "{args.repo}"')

    if len(args.paths) == 0:
        raise utils.GHError('repo-cat', 'too few arguments')
   
    for path in args.paths:

        err, listing = utils.call(f'/repos/{args.username}/{args.repo}/contents/{path}')
        if err:
            raise utils.GHError('repo-cat', err)
    
        if type(listing) == list or listing['type'] == 'dir':
            raise utils.GHError('repo-cat', f'{path} is a directory')
        if listing['type'] == 'file':
            err, contents = utils.download(path)
            if err:
                raise utils.GHError('repo-cat', err)
            print(contents)
        elif listing['type'] == 'symlink':
            raise NotImplementedError('cat symlink')
        else:
            raise NotImplementedError(f'{path} (unrecognized type "{listing["type"]}"')
