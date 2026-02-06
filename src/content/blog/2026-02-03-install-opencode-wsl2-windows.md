---
title: "在Windows上完美运行OpenCode：WSL2安装完整指南 | How to Install OpenCode on Windows with WSL2"
pubDate: 2026-02-03
category: 技术杂谈
tags: [OpenCode, WSL2, Windows, 开发工具, DevTools, 教程, Tutorial]
description: 详细介绍如何在Windows系统上通过WSL2安装和配置OpenCode AI编程助手，解决Windows原生运行的各种问题
heroImage: ../../assets/images/2026-02-03-generative-coding.jpg
---

## 在Windows上完美运行OpenCode：WSL2安装完整指南

OpenCode 是一款强大的 AI 编程助手，但在 Windows 上直接运行会遇到一些已知问题。本文将介绍如何通过 WSL2（Windows Subsystem for Linux 2）在 Windows 上完美运行 OpenCode。

### 为什么要用 WSL2？

**关键问题：OpenCode v1.1.48 内嵌的 Bun v1.3.5 在 Windows 上存在严重的 bug**

根据 [GitHub Issue #11648](https://github.com/anomalyco/opencode/issues/11648)，OpenCode 的 Windows 独立可执行文件内嵌了 Bun v1.3.5，但这个版本在 Windows 上 spawn 子进程时会段错误崩溃，导致：
- ❌ 所有 LSP 功能无法使用（代码补全、诊断等）
- ❌ 无法正常启动子进程
- ❌ 用户体验极差

**解决方案：使用 WSL2**

在 WSL2 的 Linux 环境中：
- ✅ 完全避开 Windows Bun bug
- ✅ 使用 Linux 原生的 opencode（`npm install -g opencode-ai`）
- ✅ LSP 功能完全正常
- ✅ 性能优于 Windows 原生运行

### 完整安装步骤

#### 第一步：安装 WSL2

打开管理员 PowerShell，运行：

```powershell
# 一键安装 WSL2、Ubuntu 和 Windows Terminal
wsl --install
```

按提示重启电脑，完成后从开始菜单启动 Ubuntu 完成首次设置。

**可选：启用 systemd（推荐）**
```bash
sudo tee /etc/wsl.conf << EOF
[boot]
systemd=true
EOF
wsl --shutdown  # 然后重新打开 Ubuntu
```

#### 第二步：安装 Node.js 和 npm

在 Ubuntu 终端中运行：

```bash
# 更新包管理器
sudo apt update && sudo apt upgrade -y

# 安装基础工具
sudo apt install -y curl build-essential

# 安装 Node.js LTS（需要 >= 18）
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs

# 验证安装
node --version   # 应显示 v24.x.x
npm --version    # 应显示 10.x.x
```

#### 第三步：安装 OpenCode

```bash
# 配置 npm 使用用户目录（避免权限问题）
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# 安装 opencode
npm install -g opencode-ai

# 验证安装（路径应该是 /home/用户名/.npm-global/bin/opencode）
which opencode
```

#### 第四步：配置 API 凭证

选择你有 API Key 的提供商：

**OpenAI：**
```bash
echo 'export OPENAI_API_KEY="你的密钥"' >> ~/.bashrc
echo 'export OPENCODE_MODEL="gpt-4o"' >> ~/.bashrc
```

**Google Gemini：**
```bash
echo 'export GOOGLE_API_KEY="你的密钥"' >> ~/.bashrc
echo 'export OPENCODE_MODEL="google/gemini-2.5-pro"' >> ~/.bashrc
```

**Anthropic Claude：**
```bash
echo 'export ANTHROPIC_API_KEY="你的密钥"' >> ~/.bashrc
echo 'export OPENCODE_MODEL="claude-sonnet-4-20250514"' >> ~/.bashrc
```

重新加载配置：
```bash
source ~/.bashrc
```

#### 第五步：运行 OpenCode

```bash
opencode
```

### 在 Windows 项目中使用 OpenCode

#### 方法1：移动项目到 WSL 文件系统（推荐✅）

**性能优势**：比 `/mnt/c/` 挂载快 10 倍

```bash
# 在 WSL 中创建代码目录
mkdir -p ~/code

# 复制 Windows 项目
cp -r /mnt/c/Users/Administrator/your-project ~/code/

# 进入项目
cd ~/code/your-project
opencode
```

#### 方法2：直接在 Windows 目录使用

```bash
# Windows 路径转换规则：
# C:\Users\Administrator\project → /mnt/c/Users/Administrator/project
cd /mnt/c/Users/Administrator/your-project
opencode
```

⚠️ **注意**：性能较慢（跨文件系统访问）

#### 方法3：VS Code + Remote WSL（最佳体验🔥）

1. 在 Windows 安装 [VS Code](https://code.visualstudio.com/)
2. 安装 **WSL 扩展**（Remote Development 包里）
3. 在 WSL 项目目录中运行：
   ```bash
   cd ~/code/your-project
   code .
   ```
4. VS Code 会以 WSL 模式打开，集成终端自动用 WSL，`opencode` 直接可用

### 常见问题与解决方案

#### 1. EACCES 权限错误

**问题**：`npm install -g opencode-ai` 提示权限不足

**解决**：
```bash
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
npm install -g opencode-ai
```

#### 2. opencode 命令指向 Windows 路径

**问题**：`which opencode` 显示 `/mnt/c/...`

**原因**：PATH 环境变量包含了 Windows 路径

**解决**：确保在 WSL 中安装了 opencode，并检查 `~/.npm-global/bin` 在 PATH 中

#### 3. LSP 功能不可用

**问题**：jdtls 等语言服务器找不到

**解决**：
```bash
# 安装 JDK 21
sudo apt install -y openjdk-21-jdk

# 如果 jdtls 仍然报错，可以禁用 LSP 或手动安装
# 方案1：禁用 LSP（如果只需要 AI 功能）
cat > ~/.config/opencode/config.json << 'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "lsp": false
}
EOF

# 方案2：手动安装 jdtls（需要完整 IDE 功能）
mkdir -p ~/.jdtls
cd ~/.jdtls
wget https://download.eclipse.org/jdtls/snapshots/jdt-language-server-latest.tar.gz
tar -xzf jdt-language-server-latest.tar.gz
rm jdt-language-server-latest.tar.gz
```

#### 4. apt 包管理器被锁定

**问题**：`Could not get lock /var/lib/dpkg/lock-frontend`

**解决**：
```bash
# 等待 unattended-upgrade 完成（推荐）
# 或终止进程
sudo kill 4721  # 替换为实际进程ID
sudo rm /var/lib/dpkg/lock-frontend
sudo dpkg --configure -a
```

### 总结

通过 WSL2 在 Windows 上运行 OpenCode 是目前最稳定的方案：
- ✅ 避开 Windows Bun bug
- ✅ 完整的 LSP 支持
- ✅ 原生 Linux 性能
- ✅ 与 Windows 文件系统无缝集成

如果你需要在 Windows 上使用 AI 编程助手，OpenCode + WSL2 是值得尝试的方案。

### 参考资料

- [OpenCode 官方文档 - LSP 服务器](https://opencode.ai/docs/lsp/)
- [GitHub - OpenCode Windows WSL2 设置指南](https://github.com/SweetLoou/OpenCodeWindows)
- [Issue #11648 - Windows Bun 段错误问题](https://github.com/anomalyco/opencode/issues/11648)

---

## How to Install OpenCode on Windows with WSL2: Complete Guide

OpenCode is a powerful AI programming assistant, but running it directly on Windows encounters some known issues. This article introduces how to perfectly run OpenCode on Windows through WSL2 (Windows Subsystem for Linux 2).

### Why Use WSL2?

**Critical Issue: OpenCode v1.1.48 ships with Bun v1.3.5 embedded, which has serious bugs on Windows**

According to [GitHub Issue #11648](https://github.com/anomalyco/opencode/issues/11648), OpenCode's Windows standalone executable embeds Bun v1.3.5, but this version crashes with segmentation faults when spawning child processes on Windows, leading to:
- ❌ All LSP features unusable (code completion, diagnostics, etc.)
- ❌ Cannot start child processes normally
- ❌ Poor user experience

**Solution: Use WSL2**

In the WSL2 Linux environment:
- ✅ Completely avoid Windows Bun bug
- ✅ Use native Linux opencode (`npm install -g opencode-ai`)
- ✅ LSP features fully functional
- ✅ Better performance than native Windows

### Complete Installation Steps

#### Step 1: Install WSL2

Open Administrator PowerShell and run:

```powershell
# One-click install WSL2, Ubuntu, and Windows Terminal
wsl --install
```

Restart when prompted, then launch Ubuntu from the Start menu to complete first-time setup.

**Optional: Enable systemd (recommended)**
```bash
sudo tee /etc/wsl.conf << EOF
[boot]
systemd=true
EOF
wsl --shutdown  # Then reopen Ubuntu
```

#### Step 2: Install Node.js and npm

In Ubuntu terminal:

```bash
# Update package manager
sudo apt update && sudo apt upgrade -y

# Install basic tools
sudo apt install -y curl build-essential

# Install Node.js LTS (requires >= 18)
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs

# Verify installation
node --version   # Should show v24.x.x
npm --version    # Should show 10.x.x
```

#### Step 3: Install OpenCode

```bash
# Configure npm to use user directory (avoid permission issues)
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Install opencode
npm install -g opencode-ai

# Verify installation (path should be /home/username/.npm-global/bin/opencode)
which opencode
```

#### Step 4: Configure API Credentials

Choose the provider you have an API key for:

**OpenAI:**
```bash
echo 'export OPENAI_API_KEY="your-key"' >> ~/.bashrc
echo 'export OPENCODE_MODEL="gpt-4o"' >> ~/.bashrc
```

**Google Gemini:**
```bash
echo 'export GOOGLE_API_KEY="your-key"' >> ~/.bashrc
echo 'export OPENCODE_MODEL="google/gemini-2.5-pro"' >> ~/.bashrc
```

**Anthropic Claude:**
```bash
echo 'export ANTHROPIC_API_KEY="your-key"' >> ~/.bashrc
echo 'export OPENCODE_MODEL="claude-sonnet-4-20250514"' >> ~/.bashrc
```

Reload configuration:
```bash
source ~/.bashrc
```

#### Step 5: Run OpenCode

```bash
opencode
```

### Using OpenCode with Windows Projects

#### Method 1: Move Project to WSL File System (Recommended✅)

**Performance advantage**: 10x faster than `/mnt/c/` mounts

```bash
# Create code directory in WSL
mkdir -p ~/code

# Copy Windows project
cp -r /mnt/c/Users/Administrator/your-project ~/code/

# Enter project
cd ~/code/your-project
opencode
```

#### Method 2: Use Directly in Windows Directory

```bash
# Windows path conversion rule:
# C:\Users\Administrator\project → /mnt/c/Users/Administrator/project
cd /mnt/c/Users/Administrator/your-project
opencode
```

⚠️ **Note**: Slower performance (cross-filesystem access)

#### Method 3: VS Code + Remote WSL (Best Experience🔥)

1. Install [VS Code](https://code.visualstudio.com/) on Windows
2. Install **WSL extension** (in Remote Development pack)
3. Run in WSL project directory:
   ```bash
   cd ~/code/your-project
   code .
   ```
4. VS Code opens in WSL mode, integrated terminal uses WSL, `opencode` works directly

### Common Issues and Solutions

#### 1. EACCES Permission Error

**Problem**: `npm install -g opencode-ai` reports insufficient permissions

**Solution**:
```bash
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
npm install -g opencode-ai
```

#### 2. opencode Command Points to Windows Path

**Problem**: `which opencode` shows `/mnt/c/...`

**Reason**: PATH environment variable includes Windows paths

**Solution**: Ensure opencode is installed in WSL and `~/.npm-global/bin` is in PATH

#### 3. LSP Features Unavailable

**Problem**: jdtls and other language servers not found

**Solution**:
```bash
# Install JDK 21
sudo apt install -y openjdk-21-jdk

# If jdtls still errors, disable LSP or install manually
# Option 1: Disable LSP (if only AI features needed)
cat > ~/.config/opencode/config.json << 'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "lsp": false
}
EOF

# Option 2: Manually install jdtls (for full IDE features)
mkdir -p ~/.jdtls
cd ~/.jdtls
wget https://download.eclipse.org/jdtls/snapshots/jdt-language-server-latest.tar.gz
tar -xzf jdt-language-server-latest.tar.gz
rm jdt-language-server-latest.tar.gz
```

#### 4. apt Package Manager Locked

**Problem**: `Could not get lock /var/lib/dpkg/lock-frontend`

**Solution**:
```bash
# Wait for unattended-upgrade to complete (recommended)
# Or kill process
sudo kill 4721  # 替换为 actual process ID
sudo rm /var/lib/dpkg/lock-frontend
sudo dpkg --configure -a
```

### Conclusion

Running OpenCode on Windows through WSL2 is currently the most stable solution:
- ✅ Avoid Windows Bun bug
- ✅ Complete LSP support
- ✅ Native Linux performance
- ✅ Seamless integration with Windows file system

If you need to use an AI programming assistant on Windows, OpenCode + WSL2 is a solution worth trying.

### References

- [OpenCode Official Docs - LSP Servers](https://opencode.ai/docs/lsp/)
- [GitHub - OpenCode Windows WSL2 Setup Guide](https://github.com/SweetLoou/OpenCodeWindows)
- [Issue #11648 - Windows Bun Segfault Issue](https://github.com/anomalyco/opencode/issues/11648)
