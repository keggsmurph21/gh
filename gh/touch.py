import utils

def main(args):

    if utils.repo_exists():
        # maybe echo something?
        return

    data = {
        'name': args.repo,
        'private': args.is_private
    }

    err, _ = utils.call(f'/user/repos', data=data)
    if err:
        raise utils.GHError('repo-create', err)

    # maybe echo something on success?

