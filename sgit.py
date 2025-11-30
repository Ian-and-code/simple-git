from re import sub, Match, findall
import sys
import subprocess as subs
def repo_b(repo_sgit: str):
    def repo_b_repl(m: Match):
        r"""([^\s]+)/([^\s]+)/([^\s]+)"""
        us, repo, branch = m.groups()
        return f"--branch {branch} --single-branch https://github.com/{us}/{repo}.git"
    repo = sub(repo_b_repl.__doc__, repo_b_repl, repo_sgit)
    return repo

def repo(repo_sgit: str):
    def repo_repl(m: Match):
        r"""([^\s]+)/([^\s]+)"""
        us, repo = m.groups()
        return f"https://github.com/{us}/{repo}.git"
    repo = sub(repo_repl.__doc__, repo_repl, repo_sgit)
    return repo

def main():
    for narg, varg in enumerate(sys.argv[1:], start=1):
        if findall("([^\s]+)/([^\s]+)/([^\s]+)", varg):
            sys.argv[narg] = repo_b(varg)
        elif findall("([^\s]+)/([^\s]+)", varg):
            sys.argv[narg] = repo(varg)
    subs.run(sys.argv)
if __name__ == "__main__":
    main()
