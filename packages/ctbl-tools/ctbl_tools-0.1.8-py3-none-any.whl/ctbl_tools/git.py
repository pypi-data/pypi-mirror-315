"""It provides a simple programmatical interface to git.

First, you create a git object by providing a local path to a repo:

```python
from cbl_tools.git import git

x = git("~/Dev/my_repo")
```
The previous will fail if provided path is not a git repo.

Then you may either get the remote urls with `x.get_remote()`, or a get the status of the working tree by invoking `x.get_status()`.

You may also do a commit with a list of files with `x.commit(list-of-files)`, or do a push (`x.git_push('my-commit-message')`) or a pull (`x.git_pull()`).

This package also includes two auxiliary functions:

* `git_clone(url:str, path:str)`: It clones `url` into `path`.
* `is_git_url(url:str)`: It checks whether `url` is a valid git url.
* `is_git_folder(path:str, return_folder:bool = False)`: It checks whether `path` is a cylon folder or one of its subfolders. It `return_folder` is False,
  it returns a boolean with the result. Otherwise, it returns the path of the root of the cylon folder.
"""
import re
import errno
import os.path
from ctbl_tools import process
from ctbl_tools import norm_path
from ctbl_tools.exceptions import EmptyValueError


def git_clone(url:str, path:str) -> bool:
    """It clones url to the local path."""

    path = norm_path(path)
    if os.path.exists(path):
        raise FileExistsError(f"{path} already exists")

    if not is_git_url(url):
        raise ValueError(f"{url} is not a valid git url")

    p = process.process()
    p.run(f"git clone {url} {path}")
    return p.is_ok()

def is_git_url(url:str)-> bool:
    """It tests url to be one of the five valid url-like git strings."""
    if not url:
        raise EmptyValueError("empty url")

    allw = "[\w\-\d\.]"
    user = f"({allw}+@)"
    host = f"{allw}+(\.{allw}+)+"
    port = f"(:\d+)?"
    path = f"({allw}+/?)*"

    # Type of URL #1: via SSH
    if re.fullmatch(f"ssh://{user}?{host}{port}{path}", url):
        return True

    # Type of URL #2: via HTTP(S), FTP(S), or via a pseudo-url with GIT as protocol
    if re.fullmatch(f"((ht|f)tp(s)?|git)://{host}{port}{path}", url):
        return True

    # Type of URL #3: via user and host, which is for a private server
    if re.fullmatch(f"{user}?{host}:~?{path}", url):
        return True

    return False

def is_git_folder(path:str, return_folder:bool = False):

    # We run a rev-parse
    path = norm_path(path)
    p = process.process()
    p.run(f"git -C {path} rev-parse --absolute-git-dir")

    # If there was something wrong, it's not a git folder
    if not p.is_ok() or p.is_there_stderr() or not p.is_there_stdout():
        return False

    # We split the returned line and check if there is a dir there
    is_git = os.path.isdir(os.path.dirname(p.stdout[0])) and os.path.basename(p.stdout[0]) == '.git'

    if return_folder and is_git:
        return os.path.dirname(p.stdout[0])
        
    if return_folder:
        return None

    return is_git


class git:

    local_path = None
    remote_path = None

    def __init__(self, path:str) -> None:
        """This method takes a local path and treats it as if it were a cylon repo;
        that is, it expects to find a git repo, with a files/ folder and a cylon.
        """
        # If normed path is not a folder, we reject it
        path = norm_path(path)
        if not os.path.isdir(path):
            raise NotADirectoryError(errno.ENOTDIR, f"{path} is not a folder", path)

        # We ask if it's a git folder
        if not is_git_folder(path):
            raise ValueError("Argument is not a git folder")

        p = process.process()
        p.run(f"git -C {path} rev-parse --absolute-git-dir")

        if not p.is_ok() or not p.is_there_stdout() or p.is_there_stderr():
            raise ValueError("Internal inconsistency in the arguments")

        self.local_path = os.path.dirname(p.stdout[0])

    def get_remote(self) -> dict:
        """It retrieves the list of remote repositories (usually just one), with their 'fetch' and 'push'
        URLs (usually the same). It returns (and stores within self.remote_path) a dictionary with the
        following structure:

        name-of-repo -> {
            'fetch' -> ['username', 'server', 'path'],
            'push' -> ['username', 'server', 'path']
        }
        """

        p = process.process()
        p.run(f"git -C {self.local_path} remote -v")

        if not p.is_ok() or p.is_there_stderr() or not p.is_there_stdout():
            return None

        res = {}
        for line in p.stdout:
            x = re.fullmatch(r"(\w+)\t(\S+)\s\((fetch|push)\)", line)
            if x:
                if not x.group(1) in res:
                    res[x.group(1)] = {}
                res[x.group(1)][x.group(3)] = self._url_split(x.group(2))
        self.remote_path = res
        return res

    def _url_split(self, arg:str) -> list:
        tst = re.search(r"([^@]+?)@([^:]+?):(.+)", arg)

        if tst:
            url_user = tst.group(1)
            url_domain = tst.group(2)
            url_path = tst.group(3)

            if url_path.startswith("~" + url_user):
                url_path = '~' + url_path[len(url_user)+1:]
            return [url_user, url_domain, url_path]
        else:
            return None

    def get_url(self, arg:str = '') -> str:
        """If self.remote_path has been populated, it returns the remote url for the only repo;
        otherwise, it returns None. If there is more than one repo, you should provide its name
        as argument; otherwise, it returns None."""
        if not self.remote_path:
            return None

        if len(self.remote_path)>1:
            if arg == '':
                return None
            ln = self.remote_path[arg]
        else:
            ln = self.remote_path[list(self.remote_path.keys())[0]]

        return ln[0] + '@' + ln[1] + ':' + ln[2]

    def get_status(self) -> dict:
        """It gets the status of the working tree in the porcelain v1 format (described
        in the git manual for status). It returns either a dictionary or None. The keys
        of the dict are the XY codes described for the porcelain v1 format, while the
        elements are simple lists with paths of the corresponding files."""
        p = process.process()
        p.run(f"git -C {self.local_path} status --porcelain")
        if not p.is_ok() or not p.is_there_stdout():
            return None

        res = {}
        for line in p.stdout:
            x = re.fullmatch(r"(.{2})\s(.+)", line)
            if x:
                if not x.group(1) in res:
                    res[x.group(1)] = []
                res[x.group(1)].append(x.group(2))
        return res

    def git_add(self, include_new:bool = False) -> bool:
        if include_new:
            opt = '-A'
        else:
            opt = '-u'

        p = process.process()
        p.run(f"git -C {self.local_path} add {opt}")
        return p.is_ok()

    def git_commit(self, msg:str = '') -> process.process:
        if not msg:
            msg = 'Automatic commit by cbl_tools.git.commit()'
        p = process.process()
        p.run(f"git -C {self.local_path} commit -m '{msg}'")
        return p

    def git_push(self) -> bool:
        p = process.process()
        p.run(f"git -C {self.local_path} push --all")
        return p

    def git_pull(self) -> process.process:
        p = process.process()
        p.run(f"git -C {self.local_path} pull")
        return p
