import urllib.request
import requests
from github import Github, InputGitAuthor
from bs4 import BeautifulSoup
import os

# 항상 루트에서 python ./script/update_original.py 로 실행해야 루트에 있는 Original.md 파일로 대체됩니다.
def download_from_google_style_guide_original():
    url = "https://raw.githubusercontent.com/google/styleguide/gh-pages/pyguide.md"
    savename = "Original.md"
    urllib.request.urlretrieve(url, savename)
    print("저장완료")

# commit 이름과 링크를 가져옵니다.
def get_commit_from_google_style_guide_original():
    data = requests.get("https://github.com/google/styleguide/blob/gh-pages/pyguide.md")
    html = data.text
    soup = BeautifulSoup(html, 'html.parser')
    commit_label = soup.select(".text-small.text-mono.link-gray")[0].text
    commit_url = 'https://github.com' + soup.select(".text-small.text-mono.link-gray")[0].attrs['href']
    print(commit_label, commit_url)
    return { "label":commit_label,'url': commit_url }

# access_token값을 통해 PR보냅니다.
def github_pull_request(access_token, rep_name, data):
    repo = Github(access_token).get_repo(repo_name)
    branch = repo.get_branch(branch='master')

    try:
      repo.create_git_ref(ref='refs/heads/original/'+data['label'], sha=branch.commit.sha)
    except:
      print('원본이 업데이트 되지 않았습니다.')
      return False

    text = open('Original.md', "r").read()
    contents = repo.get_contents('Original.md', ref="refs/heads/master")
    repo.update_file(contents.path, 'merge ' + data['label'] + ' 🛰', text, contents.sha, branch='original/'+data['label'])
    body = '''
새로운 번역이 왔습니다. 번역해주세요! 💤
'''
    pr = repo.create_pull(title='['+data['label']+'] 변역 요청 💬', body=body, head='original/'+data['label'], base="master")
    return True


if __name__ == "__main__":
    access_token = os.environ['ACCESS_TOKEN']
    repo_name = 'Sotaneum/Google-Python-Style-Guide-kor'
    download_from_google_style_guide_original()
    data = get_commit_from_google_style_guide_original()
    if github_pull_request(access_token, repo_name, data) is False:
        print("PR 실패")
    else:
      print("PR 성공!")













