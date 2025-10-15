import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import requests # 导入 requests 库用于发送 HTTP 请求
from kivy.clock import mainthread # 确保 UI 更新在主线程

# 使用 KV 语言字符串定义 App 的界面布局
# 这种方式可以将界面逻辑和业务逻辑分开，非常清晰
KV_STRING = """
BoxLayout:
    orientation: 'vertical'
    padding: 20
    spacing: 20

    Label:
        id: status_label
        text: '状态: 未连接'
        font_size: '20sp'
        size_hint_y: 0.2

    TextInput:
        id: ip_input
        text: '192.168.1.100' # 在这里预设一个默认IP地址
        hint_text: '请输入服务器IP地址'
        font_size: '18sp'
        size_hint_y: 0.2

    Button:
        id: start_button
        text: '开始录制'
        font_size: '20sp'
        on_press: app.send_request('/start')

    Button:
        id: stop_button
        text: '停止录制'
        font_size: '20sp'
        on_press: app.send_request('/stop')
"""

class RemoteControllerApp(App):

    def build(self):
        # 加载上面定义的界面布局
        self.root = Builder.load_string(KV_STRING)
        return self.root

    def send_request(self, endpoint):
        """发送 HTTP GET 请求到后台服务器"""
        ip_address = self.root.ids.ip_input.text
        if not ip_address:
            self.update_status("错误: 请输入IP地址")
            return

        # 构建完整的 URL
        url = f"http://{ip_address}:5000{endpoint}"
        self.update_status(f"正在发送请求到 {url}...")

        # 使用 requests 发送异步请求（推荐在线程中处理，避免UI卡顿）
        # 这里为了简化，我们直接发送，对于简单请求影响不大
        try:
            # 设置一个较短的超时时间，例如5秒
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                self.update_status(f"成功: {endpoint} 指令已发送")
            else:
                self.update_status(f"失败: 服务器返回状态码 {response.status_code}")
        except requests.exceptions.RequestException as e:
            # 处理网络错误，如无法连接、超时等
            self.update_status(f"错误: 无法连接服务器\n{e}")

    @mainthread
    def update_status(self, message):
        """在主线程安全地更新UI状态标签"""
        self.root.ids.status_label.text = f"状态: {message}"


if __name__ == '__main__':
    RemoteControllerApp().run()