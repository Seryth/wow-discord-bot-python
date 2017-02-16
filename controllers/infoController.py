import requests,json,random
import os
from git import Repo
from const import PATHS

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

jokeUrl = "http://api.icndb.com/jokes/random"

def joke():
    response = requests.get(jokeUrl, headers=headers).json()
    return response["value"]["joke"]

def giphy(search):
    giphyUrl = "http://api.giphy.com/v1/gifs/search?q="+"+".join(search)+"&api_key=dc6zaTOxFJmzC"
    response = requests.get(giphyUrl, headers=headers).json()
    responseCount = len(response["data"])
    return response["data"][random.randint(0, responseCount)]['url']

def latestCommit():
    cwd = os.getcwd()
    repo = Repo(cwd)
    branch = repo.active_branch
    gitUrl = PATHS.GITHUB_REPO_API_URL + "commits/" + str(branch)
    resp = requests.get(url=gitUrl)
    data = json.loads(resp.content)

    return "active local branch: **" + str(branch) + "** at remote: " + PATHS.GITHUB_REPO_URL + "tree/" + str(branch) + "\nlatest commit: ```" + data['sha'] + " at " + data['commit']['committer']['date'] + "\n>" + data['commit']['message'] + "```"