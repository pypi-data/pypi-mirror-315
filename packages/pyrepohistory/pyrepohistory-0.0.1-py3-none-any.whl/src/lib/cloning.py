import os
import shutil

import git

def temp_clone(vcs_link, temp_location):
    """
    ARGS
    vcs_link : url link to upstream repo vcs
    temp_location : filepath to where the repo should be cloned to 

    RETURNS
    repo : the GitRepository object of the cloned repo 
    repo_path : the filepath to the cloned repository
    """
    os.makedirs(temp_location)
    repo_path = temp_location
    repo = git.Repo.clone_from(vcs_link, repo_path)
    print(f"Successfully Cloned {vcs_link}")
    return repo, repo_path


def delete_clone(temp_location):
    """
    ARGS
    temp_location : filepath to the cloned repository 

    RETURNS
    whether or not the deletion was a success
    """
    if os.path.exists(temp_location):
        shutil.rmtree(temp_location)
        print(f"{temp_location} has been deleted.")
        return 0
    else:
        print("No clone at location")
        return 1
