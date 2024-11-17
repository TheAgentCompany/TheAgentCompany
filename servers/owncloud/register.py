import requests
import json
from bs4 import BeautifulSoup
import re


class OwnCloudAPIClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
    def install_instance(self, admin_login, admin_password, data_directory="/var/www/html/data"):
        """
        初始化安装OwnCloud实例
        """
        install_url = f"{self.base_url}/index.php/index.php"
        
        install_data = {
            "install": "true",
            "adminlogin": admin_login,
            "adminpass": admin_password,
            "adminpass-clone": admin_password,
            "directory": data_directory,
            "dbtype": "sqlite",
            "dbhost": "localhost"
        }
        
        try:
            response = self.session.post(install_url, data=install_data)
            print()
            if response.status_code == 200 or response.json()['message']=="Current user is not logged in":
                return True
            else:
                print(f"安装失败: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
            return False
            
    def login(self, username, password):
        """
        登录到OwnCloud
        """
        login_url = f"{self.base_url}/index.php/login"
        
        login_data = {
            "user": username,
            "password": password,
            "requesttoken": self._get_request_token()
        }
        
        try:
            response = self.session.post(login_url, data=login_data)
            if response.status_code == 200:
                return True
            else:
                print(f"登录失败: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
            return False
    
    def _get_request_token(self):
        """
        获取请求token
        """
        try:
            # 获取登录页面
            response = self.session.get(f"{self.base_url}")
            response.raise_for_status()  # 检查响应状态
            
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 方法1：从head中的meta标签获取
            token_meta = soup.find('meta', {'name': 'requesttoken'})
            if token_meta and 'content' in token_meta.attrs:
                return token_meta['content']
            
            # 方法2：从data-requesttoken属性获取
            token_elem = soup.find(attrs={'data-requesttoken': True})
            if token_elem:
                return token_elem['data-requesttoken']
            
            # 方法3：从页面脚本中获取
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and 'requesttoken' in script.string:
                    match = re.search(r"requesttoken\s*:\s*['\"]([^'\"]+)['\"]", script.string)
                    if match:
                        return match.group(1)
            
            # 方法4：从隐藏的input字段获取
            token_input = soup.find('input', {'name': 'requesttoken'})
            if token_input and 'value' in token_input.attrs:
                return token_input['value']
                
            print("HTML内容：", response.text[:500])  # 打印前500个字符用于调试
            raise ValueError("无法在页面中找到requesttoken")
            
        except requests.exceptions.RequestException as e:
            print(f"获取token失败 - 网络错误: {e}")
            return None
        except Exception as e:
            print(f"获取token失败 - 解析错误: {e}")
            return None


def main():
    # 使用示例
    client = OwnCloudAPIClient("http://localhost:8091")
    
    # 首次安装
    if client.install_instance("theagentcompany", "theagentcompany"):
        print("OwnCloud安装成功")
    else:
        print("OwnCloud安装失败")
    
    # 登录
    if client.login("theagentcompany", "theagentcompany"):
        print("登录成功")
    else:
        print("登录失败")

if __name__ == "__main__":
    main()