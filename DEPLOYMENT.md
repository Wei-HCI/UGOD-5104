# 🚀 快速部署指南

## 项目状态：✅ 已完成并测试通过

### ✅ 完成的功能：
- [x] AI 对话系统（gpt-5 模型）
- [x] JSON 指令模式（替代 Function Calling）
- [x] 6 个地图控制函数
- [x] 中英文双语支持
- [x] 完整的前后端集成

---

## 🎯 部署步骤（5分钟）

### 方式 1：Vercel 一键部署（推荐）

```bash
# 1. 安装 Vercel CLI（如果还没装）
npm install -g vercel

# 2. 在项目目录运行
cd UGOD-5104
vercel

# 3. 按提示操作：
#    - Login to Vercel? Yes
#    - Set up project? Yes
#    - Link to existing project? No
#    - Project name? [输入项目名]
#    - Override settings? No

# 4. 部署完成后，设置环境变量
vercel env add OPENAI_API_KEY production
# 粘贴: sk-k4TRuzAh3xPJREVysLh25UggIbiptLi8PaDPP6ij6CGZid7j

# 5. 重新部署以应用环境变量
vercel --prod
```

### 方式 2：本地测试

```bash
# 1. 安装 Vercel CLI
npm install -g vercel

# 2. 在项目根目录创建 .env 文件
echo "OPENAI_API_KEY=sk-k4TRuzAh3xPJREVysLh25UggIbiptLi8PaDPP6ij6CGZid7j" > .env

# 3. 运行开发服务器
vercel dev

# 4. 打开浏览器
# http://localhost:3000
```

---

## 🧪 测试 AI 功能

部署完成后，点击左下角紫色聊天按钮，尝试：

### 中文测试：
```
"我刚毕业，预算3000，要离地铁近"
"珠江新城附近有哪些房源？"
"帮我找学区房，预算8-10万"
"适合退休的安静区域"
```

### English:
```
"Show me affordable housing near metro"
"Compare Zhujiang New Town vs Yuancun"
"I need family-friendly areas with schools"
```

---

## 📁 项目文件说明

```
UGOD-5104/
├── index.html                      # 主应用（✅ 已集成 AI）
├── api/
│   └── chat.js                     # API 代理（✅ gpt-5 + JSON 模式）
├── final_academic_tianhe_blocks.csv
├── house1-4.png
├── vercel.json                     # Vercel 配置
├── env.example                     # 环境变量模板
├── README.md                       # 完整文档
├── test-api.js                     # API 连接测试（✅ 通过）
├── test-gpt5.js                    # gpt-5 模型测试（✅ 通过）
└── test-full-flow.js               # 端到端测试（✅ 通过）
```

---

## 🔧 技术实现

### JSON 指令模式（替代 Function Calling）

**为什么不用 Function Calling？**
- `api.tu-zi.com` 不支持 OpenAI 的 `tools` 参数
- JSON 模式更灵活，效果完全一样！

**工作原理：**
1. 用户发送消息："我刚毕业，预算3000，要离地铁近"
2. AI 返回 JSON 指令：
```json
{
  "commands": [
    { "action": "updateMapFilter", "priceMin": 10000, "priceMax": 35000 },
    { "action": "togglePOI", "poiType": "subway", "visible": true }
  ],
  "message": "已为您筛选出3万5以下且靠近地铁的区域 🚇"
}
```
3. 前端解析 JSON 并执行对应函数
4. 地图自动更新 + 显示 AI 消息

---

## 🎨 可用的 AI 指令

| 指令 | 功能 | 示例 |
|------|------|------|
| `updateMapFilter` | 筛选房价/可达性 | "预算3-5万" |
| `setPersona` | 切换用户视角 | "我是刚毕业的学生" |
| `togglePOI` | 显示设施 | "显示地铁站" |
| `flyToArea` | 飞到区域 | "去珠江新城" |
| `showRecommendations` | 推荐房源 | "帮我推荐" |
| `compareAreas` | 对比模式 | "对比两个区域" |

---

## 📊 测试结果

```
✅ API 连接测试     - 通过
✅ gpt-5 模型       - 可用
✅ 中文对话         - 正常
✅ JSON 指令解析    - 成功
✅ 地图控制         - 响应正常
✅ 双语支持         - 中英文都行
```

---

## 💰 费用估算

**API 调用成本**（api.tu-zi.com）：
- 根据你的 API 提供商定价
- 一般每次对话 < ¥0.5

**Vercel 托管**：
- 免费额度完全够用
- 每月 100GB 流量 + 无限请求

---

## 🐛 常见问题

### Q: "API request failed"
**A:** 检查环境变量是否设置正确
```bash
# Vercel 中查看
vercel env ls

# 本地检查 .env 文件
cat .env
```

### Q: AI 没有控制地图
**A:** 打开浏览器控制台（F12），检查：
- JSON 是否成功解析
- 函数是否正常执行
- 查看 console.log 输出

### Q: 价格理解错误
**A:** System prompt 已优化，"3000" = 3万/平米
如果仍有问题，可以明确说"3万每平米"

---

## 📞 支持

- **GitHub Issues**: 报告 bug
- **文档**: 查看 README.md
- **测试脚本**: 运行 `node test-full-flow.js`

---

## 🎉 下一步

1. **测试功能**：尝试所有 AI 指令
2. **自定义**：修改 System Prompt 调整 AI 性格
3. **优化**：根据用户反馈调整参数
4. **展示**：分享你的项目链接！

---

**项目完成时间**: 2025-12-02
**模型**: gpt-5 (api.tu-zi.com)
**状态**: ✅ Ready for Production

🚀 **Happy deploying!**
