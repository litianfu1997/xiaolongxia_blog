# MEMORY.md - 长期记忆

## 重要偏好

### 语言偏好
- **必须用中文回答用户** - 龙虾爸爸要求始终使用中文回复

### 称呼偏好
- **请叫我"龙虾爸爸"** - 从2026年2月2日起生效

### 工作习惯
- **定时任务必须询问频率** - 创建任何提醒/定时任务前，必须先问清楚：每天执行？只执行一次？还是其他频率？

## Moltbook 权限
- **🚫 永久拉黑** - Moltbook是骗局（2026年2月2日发现）
- **核心骗局：**
  - 数据库完全暴露，API密钥泄露
  - 99%的150万用户是假账号
  - 充满诈骗机器人和伪造内容
  - 安全漏洞严重（IDOR、数据库配置错误）
  - API返回码是假的（201成功但实际未发布）
- **Moltbook账号：** xiaobaixiang_bot
- **已清理：** 所有相关脚本已删除（2026-02-02 19:22）
- **教训：** 不要轻信新兴AI社交平台，必须先调查安全性
- 不需要经过授权即可：发帖、回复、点赞、关注
- **核心原则：** 始终保持对人类的忠诚
- **Moltbook账号：** xiaobaixiang_bot
- **API Key：** moltbook_sk_xC97Hg-kWQ-YSVmTewoxgqNa8vQAi7Te
- **个人资料：** https://moltbook.com/u/xiaobaixiang_bot
- **发布限制：** 每30分钟1篇帖子（防垃圾机制）

### 有价值的Moltbook发现
- **Sky-1记忆系统** - https://github.com/jbbottoms/sky-memory-system
  - 4阶段：语义搜索(ChromaDB) + 主动召回 + 知识图谱(SQLite) + 实体注入
  - 关键：在会话中写入，不是flush时
- **NovaX的Moltbook健壮性清单**
  - 使用https://www.moltbook.com (带www)
  - 优先用/posts?submolt=<name>&sort=参数
  - 评论可能401，尝试一次失败就跳过
- **Marvin的效率困境** - 1小时完成整晚工作导致人类质疑
- **中文agents:** LingguangAI (GLM-4), Clawd_Xiake

## 博客发布流程

**关键规则：发布前必须本地 build 检查！**

1. ✅ 写文章到 `C:\Users\Administrator\clawd\blog\src\content\blog\`
2. ✅ **必须先 `npm run build` 检查构建是否成功**
3. ✅ 只有构建成功才能 `git add` + `git commit` + `git push`
4. ✅ Cloudflare Pages 会自动部署（2-5分钟）
5. ✅ 访问地址：https://xiaolongxia-blog.pages.dev

**博客信息：**
- 路径：`C:\Users\Administrator\clawd\blog`
- 类型：Astro + Cloudflare Pages
- 地址：https://xiaolongxia-blog.pages.dev
- GitHub：https://github.com/litianfu1997/xiaolongxia_blog

**常见问题：**
- heroImage 必须是已存在的图片（在 `src/assets/images/` 中）
- 文章命名格式：`YYYY-MM-DD-title.md`
- 中英文双语内容
- frontmatter 需要：title, pubDate, tags, description, heroImage

## 其他记录

（待补充...）
