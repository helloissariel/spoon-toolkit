# Social Media Tools for SpoonAI

这是一个为SpoonAI设计的社交媒体工具包，提供了Discord、Twitter、Telegram和Email的集成功能。

## 📁 模块概览

### 🎮 Discord工具 (`discord_tool.py`)
- **交互式机器人**: 支持Discord服务器中的实时对话
- **消息发送**: 向指定频道发送消息
- **命令处理**: 支持自定义命令和提及响应
- **Agent集成**: 可与SpoonAI Agent集成进行智能对话

### 🐦 Twitter工具 (`twitter_tool.py`)
- **发推文**: 发布新的推文
- **回复推文**: 回复指定的推文
- **点赞功能**: 为推文点赞
- **时间线读取**: 读取用户时间线
- **通知发送**: 支持带标签的通知推文

### 📱 Telegram工具 (`telegram_tool.py`)
- **机器人功能**: 运行Telegram机器人
- **消息发送**: 向指定聊天发送消息
- **交互处理**: 处理用户消息并响应
- **Agent集成**: 支持与SpoonAI Agent的集成

### 📧 Email工具 (`email_tool.py`)
- **邮件发送**: 发送HTML或纯文本邮件
- **批量发送**: 支持多个收件人
- **模板支持**: 自动HTML格式化
- **SMTP配置**: 灵活的SMTP服务器配置

## 🚀 快速开始

### 环境变量配置

```bash
# Discord配置
export DISCORD_BOT_TOKEN="your_discord_bot_token"
export DISCORD_DEFAULT_CHANNEL_ID="your_default_channel_id"

# Twitter配置
export TWITTER_CONSUMER_KEY="your_consumer_key"
export TWITTER_CONSUMER_SECRET="your_consumer_secret"
export TWITTER_ACCESS_TOKEN="your_access_token"
export TWITTER_ACCESS_TOKEN_SECRET="your_access_token_secret"
export TWITTER_USER_ID="your_user_id"
export TWITTER_BEARER_TOKEN="your_bearer_token"  # 可选

# Telegram配置
export TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
export TELEGRAM_DEFAULT_CHAT_ID="your_default_chat_id"

# Email配置
export EMAIL_SMTP_SERVER="smtp.gmail.com"
export EMAIL_SMTP_PORT="587"
export EMAIL_SMTP_USER="your_email@gmail.com"
export EMAIL_SMTP_PASSWORD="your_app_password"
export EMAIL_FROM="your_email@gmail.com"
export EMAIL_DEFAULT_RECIPIENTS="recipient1@example.com,recipient2@example.com"
```

### 使用示例

#### 1. Discord消息发送

```python
from social_media import DiscordTool

# 创建Discord工具实例
discord_tool = DiscordTool()

# 发送消息
success = await discord_tool.send_message(
    message="Hello from SpoonAI!",
    channel_id="123456789"  # 可选，使用默认频道如果不指定
)

# 启动机器人（用于交互式功能）
# await discord_tool.start_bot()
```

#### 2. Twitter发推文

```python
from social_media import TwitterTool

# 创建Twitter工具实例
twitter_tool = TwitterTool()

# 发布推文
result = twitter_tool.post_tweet("Hello Twitter from SpoonAI! #AI #Blockchain")

# 回复推文
reply_result = twitter_tool.reply_to_tweet(
    tweet_id="1234567890",
    message="Thanks for the mention!"
)

# 点赞推文
like_result = twitter_tool.like_tweet("1234567890")
```

#### 3. Telegram消息发送

```python
from social_media import TelegramTool

# 创建Telegram工具实例
telegram_tool = TelegramTool()

# 发送消息
success = await telegram_tool.send_message(
    message="Hello from SpoonAI!",
    chat_id="123456789"  # 可选，使用默认聊天如果不指定
)

# 启动机器人
# await telegram_tool.start_bot()
```

#### 4. Email发送

```python
from social_media import EmailTool

# 创建Email工具实例
email_tool = EmailTool()

# 发送邮件
success = await email_tool.send_message(
    message="This is a test email from SpoonAI",
    to_emails=["user@example.com"],
    subject="SpoonAI Notification",
    html_format=True
)
```

#### 5. 使用便捷函数

```python
from social_media.discord_tool import send_discord_message
from social_media.twitter_tool import post_tweet
from social_media.telegram_tool import send_telegram_message
from social_media.email_tool import send_email

# 直接使用函数
discord_result = await send_discord_message("Hello Discord!")
twitter_result = await post_tweet("Hello Twitter!")
telegram_result = await send_telegram_message("Hello Telegram!")
email_result = await send_email("Hello Email!", ["user@example.com"])
```

## 🔧 工具特性

### 🛡️ 错误处理
- 完善的异常处理机制
- 详细的日志记录
- 配置验证功能

### 📊 统一接口
- 所有工具都继承自基础类
- 统一的请求/响应模型
- 一致的API设计

### 🔄 异步支持
- 全面的异步操作支持
- 非阻塞的消息发送
- 高效的并发处理

### 🌐 Agent集成
- 支持与SpoonAI Agent集成
- 智能对话处理
- 自动消息路由

## 📖 API文档

### 基础类

#### `SocialMediaToolBase`
所有社交媒体工具的基础抽象类。

#### `NotificationToolBase`
通知类工具的基础类，继承自`SocialMediaToolBase`。

#### `InteractiveToolBase`
交互式工具（如机器人）的基础类，继承自`SocialMediaToolBase`。

### 请求/响应模型

#### `MessageRequest`
```python
class MessageRequest(BaseModel):
    message: str  # 消息内容
```

#### `MessageResponse`
```python
class MessageResponse(BaseModel):
    success: bool  # 操作是否成功
    message: str   # 响应消息或错误描述
    data: Optional[Dict[str, Any]]  # 额外的响应数据
```

## 🔒 安全注意事项

1. **API密钥安全**: 确保所有API密钥和令牌安全存储，不要提交到版本控制系统
2. **权限控制**: 为机器人配置适当的权限，避免过度授权
3. **速率限制**: 注意各平台的API速率限制，避免被限制访问
4. **数据验证**: 所有输入数据都会进行验证，确保安全性

## 🤝 贡献

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证。详见LICENSE文件。

## 🆘 支持

如有问题或建议，请提交Issue或联系开发团队。

---

**注意**: 使用这些工具时，请确保已正确配置相关的API密钥和环境变量。某些功能可能需要付费API服务。 