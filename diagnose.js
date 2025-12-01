// 诊断脚本 - 在浏览器控制台运行
console.log('=== 诊断 AI 聊天功能 ===\n');

// 检查 1: 当前页面 URL
console.log('1. 页面 URL:', window.location.href);
if (window.location.protocol === 'file:') {
    console.error('❌ 错误：你直接打开了 HTML 文件！');
    console.log('✅ 解决方案：需要用 vercel dev 启动服务器');
    console.log('\n在终端运行：');
    console.log('  cd UGOD-5104');
    console.log('  vercel dev');
    console.log('  然后访问 http://localhost:3000\n');
} else {
    console.log('✅ URL 正确\n');
}

// 检查 2: 测试 API 连接
console.log('2. 测试 API 连接...');
fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        messages: [{ role: 'user', content: 'test' }]
    })
})
.then(response => {
    console.log('API 响应状态:', response.status);
    if (response.ok) {
        console.log('✅ API 连接成功！');
        return response.json();
    } else {
        console.error('❌ API 返回错误:', response.status);
        return response.text().then(text => {
            console.error('错误详情:', text);
        });
    }
})
.then(data => {
    if (data) {
        console.log('✅ API 返回数据:', data);
    }
})
.catch(error => {
    console.error('❌ API 请求失败:', error.message);
    console.log('\n可能原因：');
    console.log('1. vercel dev 没有运行');
    console.log('2. API 路由配置错误');
    console.log('3. 网络问题');
});

// 检查 3: React 组件状态
setTimeout(() => {
    console.log('\n3. 检查聊天组件...');
    const chatToggle = document.querySelector('.ai-chat-toggle');
    const chatPanel = document.querySelector('.ai-chat-panel');

    if (chatToggle) {
        console.log('✅ 聊天按钮已加载');
    } else {
        console.error('❌ 找不到聊天按钮');
    }

    if (chatPanel) {
        console.log('✅ 聊天面板已加载');
    } else {
        console.error('❌ 找不到聊天面板');
    }

    console.log('\n=== 诊断完成 ===');
}, 1000);
