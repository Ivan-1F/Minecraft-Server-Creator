import requests
import json
from progress.bar import Bar
import pkg_resources

from mcservercreator import constant

def get_all_versions_info():
    return json.loads(requests.get(constant.VERSION_API).text)

# ['20w46a', '20w45a', '1.16.4', '1.16.4-rc1', '1.16.4-pre2', ...]
def get_all_versions_id():
    ret = []
    versions_info = get_all_versions_info()
    for version in versions_info['versions']:
        ret.append(version['id'])
    return ret

# {'id': '1.16.5', 'type': 'release', 'url': 'https://launchermeta.mojang.com/v1/packages/436877ffaef948954053e1a78a366b8b7c204a91/1.16.5.json', 'time': '2021-01-14T16:09:14+00:00', 'releaseTime': '2021-01-14T16:05:32+00:00'}
def get_version_info(version: str):
    versions_info = get_all_versions_info()
    for version_info in versions_info['versions']:
        if version_info['id'] == version:
            return version_info

# 'https://launchermeta.mojang.com/v1/packages/436877ffaef948954053e1a78a366b8b7c204a91/1.16.5.json'
def get_version_url(version: str):
    version_info = get_version_info(version)
    return version_info['url']


def get_version_detail(version: str):
    url = get_version_url(version)
    return json.loads(requests.get(url).text)

# 'https://launcher.mojang.com/v1/objects/1b557e7b033b583cd9f66746b7a9ab1ec1673ced/server.jar'
def get_server_jar_url(version: str):
    detail = get_version_detail(version)
    return detail['downloads']['server']['url']

def download_server_jar(path: str, mc_version: str):
    with open(path, "wb") as f:
        response = requests.get(get_server_jar_url(mc_version), stream=True)
        total_length = response.headers.get('content-length')
        total_length = int(total_length)
        with Bar('Downloading Minecraft server core', max=total_length) as bar:
            dl = 0
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                bar.next(len(data))

def download_fabric_installer(path: str):
    with open(path, "wb") as f:
        response = requests.get(constant.FABRIC_URL, stream=True)
        total_length = response.headers.get('content-length')
        total_length = int(total_length)
        with Bar('Downloading fabric installer', max=total_length) as bar:
            dl = 0
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                bar.next(len(data))

def get_all_installed_packages():
    installed_packages = pkg_resources.working_set
    packages_list = sorted([i.key for i in installed_packages])
    return packages_list

def replace_in_file(path: str, old: str, new: str):
    ret = ''
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if old in line:
                line = line.replace(old, new)
            ret += line
    with open(path, 'w', encoding='utf-8') as f:
        f.write(ret)
        f.close()