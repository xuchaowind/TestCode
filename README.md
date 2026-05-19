# 网络测试脚本 (Network Test Script)

完整的Python网络测试工具，用于检测网络连通性、DNS解析、HTTP响应、端口连通性和网络延迟。

## 功能特性

- 🔍 **DNS解析测试** - 验证域名是否能正确解析到IP地址
- 📡 **Ping测试** - 检查主机的网络连通性
- 🌐 **HTTP测试** - 发送HTTP请求并测量响应时间
- 🔌 **端口连通性测试** - 检查特定端口是否开放
- ⏱️ **网络延迟测试** - 测试到目标主机的平均延迟
- 💾 **结果保存** - 将所有测试结果保存为JSON格式

## 系统要求

- Python 3.6+
- 支持系统：Linux、macOS、Windows

## 安装

### 1. 克隆或下载项目
```bash
git clone https://github.com/xuchaowind/TestCode.git
cd TestCode
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

## 使用方法

### 基础使用
```bash
python network_test.py
```

脚本会自动执行所有测试，并将结果保存到 `network_test_results.json`

### 在Python代码中使用

```python
from network_test import NetworkTester

# 创建测试实例
tester = NetworkTester(timeout=5)

# 运行单个测试
tester.test_dns_resolution('example.com')
tester.test_ping('example.com')
tester.test_http_request('https://example.com')
tester.test_port_connectivity('example.com', 443)
tester.test_network_latency('example.com')

# 保存结果
tester.save_results('my_results.json')
tester.print_summary()
```

## 输出示例

### 命令行输出
```
============================================================
Starting Network Tests
============================================================

[DNS Resolution Tests]
✓ DNS Test: github.com -> 140.82.121.4
✓ DNS Test: google.com -> 172.217.174.46
✓ DNS Test: cloudflare.com -> 104.16.132.229

[Ping Connectivity Tests]
✓ Ping Test: github.com is reachable
✓ Ping Test: google.com is reachable

[HTTP Request Tests]
✓ HTTP Test: https://github.com - Status 200 (234.56ms)
✓ HTTP Test: https://www.google.com - Status 200 (125.34ms)
✓ HTTP Test: https://www.cloudflare.com - Status 200 (98.76ms)

[Port Connectivity Tests]
✓ Port Test: github.com:22 is open
✓ Port Test: github.com:443 is open
✓ Port Test: 8.8.8.8:53 is open

[Network Latency Tests]
✓ Latency Test: github.com - Avg 45.23ms
✓ Latency Test: google.com - Avg 32.15ms

============================================================
Network Tests Completed
============================================================
```

### JSON结果文件 (network_test_results.json)

```json
{
  "timestamp": "2026-05-19T15:30:00.123456",
  "system": "Linux",
  "tests": {
    "dns": {
      "github.com": {
        "status": "success",
        "hostname": "github.com",
        "ip_address": "140.82.121.4"
      }
    },
    "ping": {
      "github.com": {
        "status": "success",
        "host": "github.com",
        "output": "..."
      }
    },
    "http": {
      "https://github.com": {
        "status": "success",
        "url": "https://github.com",
        "status_code": 200,
        "response_time_ms": 234.56,
        "content_length": 45678
      }
    },
    "ports": {
      "github.com_22": {
        "status": "success",
        "host": "github.com",
        "port": 22,
        "message": "Port 22 is open"
      }
    },
    "latency": {
      "github.com": {
        "status": "success",
        "host": "github.com",
        "avg_ms": 45.23,
        "min_ms": 42.15,
        "max_ms": 48.67,
        "count": 4
      }
    }
  }
}
```

## 默认测试目标

### DNS 解析测试
- github.com
- google.com
- cloudflare.com

### Ping 测试
- github.com
- google.com

### HTTP 请求测试
- https://github.com
- https://www.google.com
- https://www.cloudflare.com

### 端口连通性测试
- github.com:22 (SSH)
- github.com:443 (HTTPS)
- 8.8.8.8:53 (DNS)

### 延迟测试
- github.com
- google.com

## 自定义测试

编辑 `network_test.py` 文件中的 `run_all_tests()` 方法来自定义测试目标和参数：

```python
def run_all_tests(self) -> Dict[str, Any]:
    # 修改下面的列表
    for hostname in ['your.domain.com', 'another.domain.com']:
        self.test_dns_resolution(hostname)
    # ...
```

## 故障排除

### 权限问题
如果遇到权限错误（特别是ping测试），可能需要以管理员身份运行脚本：

**Linux/macOS:**
```bash
sudo python network_test.py
```

**Windows:**
- 右键点击命令提示符或PowerShell，选择"以管理员身份运行"
- 然后执行：`python network_test.py`

### 超时问题
如果测试超时，请检查：
1. 网络连接是否正常
2. 防火墙是否阻止了出站连接
3. DNS是否正常工作
4. 目标主机是否在线

### 导入错误
确保已正确安装依赖：
```bash
pip install --upgrade -r requirements.txt
```

### 跨平台兼容性
脚本会自动检测操作系统并使用相应的系统命令。如果遇到特定平台的问题，请在Issue中报告。

## API 说明

### NetworkTester 类

#### `__init__(timeout=5)`
初始化测试器
- `timeout`: 网络操作的超时时间（秒）

#### `test_dns_resolution(hostname)`
测试DNS解析
- 返回：包含状态和IP地址的字典

#### `test_ping(hostname)`
测试Ping连通性
- 返回：包含状态的字典

#### `test_http_request(url)`
测试HTTP请求
- 返回：包含状态码和响应时间的字典

#### `test_port_connectivity(host, port)`
测试端口连通性
- 返回：包含端口状态的字典

#### `test_network_latency(host, count=4)`
测试网络延迟
- 返回：包含平均/最小/最大延迟的字典

#### `run_all_tests()`
运行所有测试
- 返回：包含所有结果的字典

#### `save_results(filename)`
保存结果到JSON文件
- `filename`: 输出文件名（默认为 network_test_results.json）

#### `print_summary()`
打印测试摘要

## 许可证

MIT License

## 作者

Created by xuchaowind

## 贡献

欢迎提交Issue和Pull Request！
