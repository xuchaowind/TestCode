# 网络测试脚本

这是一个全面的网络诊断工具，用于测试网络连通性和性能。

## 功能特性

✓ **Ping 测试** - 检查网络连通性  
✓ **DNS 解析测试** - 验证DNS功能  
✓ **HTTP 请求测试** - 检查Web服务器连接  
✓ **端口测试** - 检查特定端口是否��放  
✓ **网络延迟测试** - 测试网络延迟  
✓ **结果保存** - 将测试结果导出为JSON格式  

## 系统要求

- Python 3.6+
- Windows / Linux / macOS
- 网络访问权限

## 安装

```bash
# 克隆或下载本仓库
git clone https://github.com/xuchaowind/TestCode.git
cd TestCode

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

### 运行完整测试

```bash
python network_test.py
```

### 自定义测试

编辑 `network_test.py` 中的 `main()` 函数，修改测试项目：

```python
# 修改DNS测试的域名
tester.dns_test("example.com")

# 修改Ping测试的主机
tester.ping_test("1.1.1.1")

# 修改HTTP测试的URL
tester.http_test("https://example.com")

# 修改端口测试
tester.port_test("example.com", 80)
```

## 输出示例

```
============================================================
网络测试脚本 v1.0
============================================================

[DNS TEST] 测试域名: github.com
✓ DNS 解析成功
  github.com -> 140.82.113.4

[PING TEST] 测试主机: 8.8.8.8
✓ 8.8.8.8 可达
PING 8.8.8.8 (8.8.8.8): 56 data bytes
...

[HTTP TEST] 测试URL: https://github.com
✓ HTTP 请求成功
  状态码: 200
  响应时间: 0.45秒
  Content-Type: text/html; charset=utf-8

[PORT TEST] 测试端口: github.com:443
✓ 端口 443 开放

[LATENCY TEST] 测试网络延迟到: 8.8.8.8
✓ 延迟测试成功
...

============================================================
网络测试完成
============================================================
```

## 结果文件

测试完成后，结果将保存到 `network_test_results.json` 文件：

```json
{
  "timestamp": "2026-05-19T15:30:00.123456",
  "tests": {
    "dns": {
      "status": "success",
      "domain": "github.com",
      "ip": "140.82.113.4"
    },
    "ping": {
      "status": "success",
      "host": "8.8.8.8",
      "details": "..."
    },
    ...
  }
}
```

## 常见问题

**Q: 脚本需要管理员权限吗？**  
A: 某些操作系统的某些测试可能需要，但大多数测试不需要。如果遇到权限问题，请以管理员身份运行。

**Q: 可以测试内网IP吗？**  
A: 可以。修改测试中的IP地址为内网地址即可。

**Q: 如何处理超时？**  
A: 可以修改 `timeout` 参数，单位为秒。

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
