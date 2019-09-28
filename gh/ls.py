import utils

def main(args):

    if not utils.repo_exists():
        raise utils.GHError('repo-exists', f'cannot stat "{args.repo}"')

    paths = args.paths if len(args.paths) else ['/']
    for i, path in enumerate(paths):

        if len(paths) > 1:
            if i:
                print()
            print(path + ':')

        err, listings = utils.call(f'/repos/{args.username}/{args.repo}/contents/{path}')
        if err:
            raise utils.GHError('repo-list', err)

        if type(listings) == dict:
            listings = [listings]

        for listing in listings:
            name = listing['path']
            if listing['type'] == 'file':
                print(name)
            elif listing['type'] == 'dir':
                print(name + '/')
            elif listing['type'] == 'symlink':
                print(name + '@')
            else:
                print(f'{name} (unrecognized type "{listing["type"]}"')
            #print(listing['type'], listing['path'], listing['download_url'])
