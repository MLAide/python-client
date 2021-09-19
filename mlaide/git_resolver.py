from git import Repo, InvalidGitRepositoryError, NoSuchPathError
from typing import Optional
from .model.git import Git


def get_git_metadata(remote_name: str = 'origin') -> Optional[Git]:
    try:
        repo = Repo(search_parent_directories=True)
    except (InvalidGitRepositoryError, NoSuchPathError):
        return None

    git_metadata = Git(
        commit_time=repo.head.object.committed_datetime,
        commit_hash=repo.head.object.hexsha,
        is_dirty=repo.is_dirty(),
        repository_uri=next(repo.remote(remote_name).urls)
    )

    return git_metadata
