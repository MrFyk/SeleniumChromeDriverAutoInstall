import platform
import re
import requests
import requests_cache
import shutil
import os
from ast import literal_eval



def get_chrome_info():
    # 查看操作系统名称
    system_name = platform.system()
    chrome_version_file_path = ''
    if system_name == 'Darwin':
        chrome_version_file_path = '/Applications/Google Chrome.app/Contents/Info.plist'
    elif system_name == 'Windows':
        chrome_version_file_path_one = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.VisualElementsManifest.xml'
        chrome_version_file_path_two = r'C:\Program Files\Google\Chrome\Application\chrome.VisualElementsManifest.xml'
        if os.path.exists(chrome_version_file_path_one):
            chrome_version_file_path = chrome_version_file_path_one
        else:
            chrome_version_file_path = chrome_version_file_path_two
    else:
        # 手头无Linux，无法测试
        pass

    # 匹配版本号
    with open(chrome_version_file_path, 'r') as f:
        version_number = re.search(r'\d*\.\d*\.\d*\.\d*', f.read()).group(0)

    # 查看机器类型
    machine_type = platform.machine()

    return [system_name, machine_type, version_number]


def get_driver_download_link(system_name, machine_type, version_number):
    URL = 'https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json'
    requests_cache.install_cache('./chrome_driver_info')
    response = requests.get(url=URL)
    matching_str = '{"version":"' + version_number[:version_number.rfind('.')] + r'.\d*".*?}]}}'
    matching_result = re.findall(matching_str, response.text)
    version_list = set(re.findall(r'\d*\.\d*\.\d*\.\d*', str(matching_result)))

    def version_compare(version):
        if int(version[version.rfind('.') + 1:]) <= int(version_number[version_number.rfind('.') + 1:]):
            return version

    best_matching_version = max(version_list, key=version_compare)

    for item in matching_result:
        if literal_eval(item)['version'] == best_matching_version:
            best_matching_info = literal_eval(item)
            break

    system_machine = ''
    if system_name == 'Darwin' and machine_type == 'arm64':
        system_machine = 'mac-arm64'
    elif system_name == 'Darwin' and machine_type != 'arm64':
        system_machine = 'mac-x64'
    elif system_name == 'Windows':
        system_machine = 'win64'

    for driver_item in best_matching_info['downloads']['chromedriver']:
        if driver_item['platform'] == system_machine:
            return driver_item['url']


def driver_download_unzip(system_name, link):
    driver_bytes = requests.get(url=link).content
    driver_path = link.split('/')[-1]
    with open(driver_path, 'wb') as f:
        f.write(driver_bytes)

    zip_file = driver_path
    target_folder = './'
    shutil.unpack_archive(zip_file, target_folder, 'zip')

    os.remove(zip_file)

    if system_name == 'Darwin':
        current_path = os.getcwd() + f'/{driver_path[:-4]}/chromedriver'
        order = f'chmod -R 777 {current_path}'
        os.system(order)
        return current_path
    elif system_name == 'Windows':
        current_path = os.getcwd() + rf'\{driver_path[:-4]}\chromedriver.exe'
        return current_path
    else:
        # 手头无Linux，无法测试
        pass


def main():
    sys_name, machine, version_num = get_chrome_info()
    # print(sys_name, machine, version_num)
    download_link = get_driver_download_link(sys_name, machine, version_num)
    # print(download_link)

    file_path_one = os.getcwd() + f"/{download_link.split('/')[-1][:-4]}/chromedriver"
    file_path_two = os.getcwd() + fr"\{download_link.split('/')[-1][:-4]}\chromedriver.exe"
    if os.path.exists(file_path_one) and sys_name == 'Darwin':
        return file_path_one
    elif os.path.exists(file_path_two) and sys_name == 'Windows':
        return file_path_two
    else:
        driver_path = driver_download_unzip(sys_name, download_link)
        return driver_path


if __name__ == '__main__':
    result = main()
    print(result)
