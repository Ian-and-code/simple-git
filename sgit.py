from re import sub, Match, findall
import sys
import subprocess as subs
import re
# -------------------------
#   RESOLUCIÓN DE REPOS
# -------------------------

def repo_b(s: str):
    """
    user/repo/branch → flags de branch y URL completa
    """
    def repl(m: Match):
        r"""([^\s]+)/([^\s]+)/([^\s]+)"""
        us, repo, branch = m.groups()
        return f"--branch {branch} --single-branch https://github.com/{us}/{repo}.git"
    return sub(repl.__doc__, repl, s)

def repo(s: str):
    """
    user/repo → URL https
    """
    def repl(m: Match):
        r"""([^\s]+)/([^\s]+)"""
        us, repo = m.groups()
        return f"https://github.com/{us}/{repo}.git"
    return sub(repl.__doc__, repl, s)

# -------------------------
#   PROCESAR ARGUMENTOS
# -------------------------

def process_args(argv):
    """
    Reemplaza user/repo y user/repo/branch expandiendo argumentos.
    """
    args = argv[:]
    i = 0
    while i < len(args):
        a = args[i]
        if findall(r"([^\s]+)/([^\s]+)/([^\s]+)", a):
            repl = repo_b(a).split()
            args[i:i+1] = repl
            i += len(repl)
        elif findall(r"([^\s]+)/([^\s]+)", a):
            repl = repo(a).split()
            args[i:i+1] = repl
            i += len(repl)
        else:
            i += 1
    return args

# -------------------------
#   EJECUTAR GIT REAL
# -------------------------

def run_git(args):
    cmd = ["git"] + args
    proc = subs.run(cmd, capture_output=True, text=True)

    # Capturamos ambas salidas
    raw = proc.stdout + proc.stderr
    gits = "git Git gIt giT GIt gIT GIT".split()
    sgits = "sgit Sgit sGIt sgiT SGit sgIT SGIT".split()
    patched = raw
    # git → sgit (palabra completa)
    for g, sg in zip(gits, sgits):
        patched = re.sub(r"(?<![A-Za-z0-9_])(%s)(?![A-Za-z0-9_])" % g, sg, patched)
    return patched

# -------------------------
#   MOSTRAR VERSION
# -------------------------

def show_version():
    print("sgit 1.0.0 — Simple Git Wrapper")

# -------------------------
#   MAIN
# -------------------------

def main():
    raw = sys.argv[1:]

    # Interceptar --version
    if "--version" in raw:
        show_version()
        return

    args = process_args(raw)
    salida = run_git(args)

    # Mostrar salida modificada
    print(salida, end="")

if __name__ == "__main__":
    main()
