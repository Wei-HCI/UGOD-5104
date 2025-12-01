# 🚀 GitHub Pages 部署指南（纯前端版本）

## ⚠️ 重要说明

这是**纯前端版本**，API Key 直接写在代码中：
- ✅ 适合：内部分享、小范围使用
- ❌ 不适合：公开项目、大规模使用
- ⚠️ 风险：API key 可见，可能被滥用

---

## 📋 部署步骤

### 1. 测试本地功能

在部署前先测试一下：

```bash
# 方式 A: 直接打开测试页面
# 在浏览器打开：test-github-pages.html
# 点击所有测试按钮，确保都通过

# 方式 B: 用 Python 启动本地服务器
cd C:\Users\adminroot\Documents\GitHub\UGOD-5104
python -m http.server 8000
# 访问 http://localhost:8000/index.html
```

### 2. 推送到 GitHub

```bash
# 1. 确保在项目目录
cd C:\Users\adminroot\Documents\GitHub\UGOD-5104

# 2. 添加所有文件
git add .

# 3. 提交
git commit -m "Add AI chatbot (GitHub Pages version)"

# 4. 推送到 GitHub
git push origin main
```

### 3. 启用 GitHub Pages

1. 打开你的 GitHub 仓库页面
2. 点击 **Settings** （设置）
3. 左侧菜单找到 **Pages**
4. 在 "Source" 下拉菜单选择：
   - Branch: `main`
   - Folder: `/ (root)`
5. 点击 **Save**
6. 等待 1-2 分钟，页面会显示：
   ```
   Your site is live at https://yourusername.github.io/UGOD-5104/
   ```

### 4. 访问测试

打开你的 GitHub Pages 链接：
```
https://yourusername.github.io/UGOD-5104/index.html
```

点击左下角紫色聊天按钮，测试 AI 功能！

---

## 🧪 功能测试清单

访问页面后，依次测试：

### ✅ 基础功能
- [ ] 地图正常加载
- [ ] 可以拖动/缩放地图
- [ ] 左侧控制面板显示正常
- [ ] 左下角有紫色聊天按钮

### ✅ AI 对话功能
- [ ] 点击聊天按钮能打开面板
- [ ] 输入消息能发送
- [ ] AI 能正常回复
- [ ] 地图能根据 AI 指令更新

### ✅ 测试对话
```
"我刚毕业，预算3000，要离地铁近"
→ 应该筛选地图 + 显示地铁站

"珠江新城附近有哪些？"
→ 应该飞到珠江新城

"帮我找学区房"
→ 应该显示学校图层
```

---

## 🔧 常见问题

### Q1: 聊天按钮没反应
**A:** 按 F12 打开控制台，看看有没有错误：
- 如果看到 **CORS error**：这是正常的，说明 API 有跨域限制
  - 解决方案：联系 API 提供商开启 CORS
- 如果看到 **401 Unauthorized**：API key 可能失效
- 如果看到 **网络错误**：检查网络连接

### Q2: AI 回复很慢
**A:** 正常现象，gpt-5 需要 3-10 秒响应时间

### Q3: AI 没有控制地图
**A:** 控制台输入：
```javascript
// 检查 JSON 解析
console.log('Last AI response:', messages[messages.length - 1]);
```
如果 AI 返回的不是 JSON 格式，可能需要调整 System Prompt

### Q4: 想隐藏 API Key
**A:** 两个方案：
1. **GitHub 私有仓库**：Settings → Danger Zone → Change visibility → Private
2. **用 Vercel**：推荐，更安全

---

## 📊 查看 API 使用情况

建议定期检查 API 用量，防止超支：

1. 登录你的 API 提供商后台
2. 查看 Usage / Billing 页面
3. 设置用量警报

---

## 🔒 安全建议

### 最小化风险：

1. **GitHub 私有仓库**（如果可能）
   ```bash
   # 在 GitHub 设置页面
   Settings → Danger Zone → Change visibility → Private
   ```

2. **限制分享范围**
   - 只分享给内部同事
   - 不要发到公开论坛/社交媒体

3. **监控用量**
   - 每周检查 API 用量
   - 如发现异常立即更换 key

4. **考虑迁移到 Vercel**
   - 如果使用频繁，建议迁移到 Vercel
   - 更安全，不暴露 key

---

## 📁 文件说明

```
UGOD-5104/
├── index.html                      # ✅ 主应用（已改为前端直调 API）
├── test-github-pages.html          # ✅ 测试页面（快速验证功能）
├── api/chat.js                     # ⚠️  不需要了（GitHub Pages 不用）
├── final_academic_tianhe_blocks.csv
├── house1-4.png
└── ...
```

**部署到 GitHub Pages 只需要：**
- ✅ `index.html`
- ✅ `final_academic_tianhe_blocks.csv`
- ✅ `house1-4.png` 等图片
- ❌ `api/` 文件夹不需要

---

## 🎯 下一步

1. **本地测试**：打开 `test-github-pages.html`，运行所有测试
2. **推送代码**：`git push origin main`
3. **启用 Pages**：GitHub Settings → Pages → 选择 main 分支
4. **分享链接**：把 GitHub Pages 链接分享给同事

---

## 🆘 需要帮助？

遇到问题？检查：
1. **浏览器控制台**（F12 → Console）- 看错误信息
2. **网络请求**（F12 → Network）- 看 API 调用状态
3. **测试页面**（`test-github-pages.html`）- 单独测试 AI 功能

---

**部署时间**: < 5 分钟
**维护成本**: 零（静态托管）
**费用**: GitHub Pages 免费 + API 调用费

🎉 **祝部署顺利！**
