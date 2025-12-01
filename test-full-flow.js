// 完整端到端测试：JSON 指令模式
const API_KEY = 'sk-k4TRuzAh3xPJREVysLh25UggIbiptLi8PaDPP6ij6CGZid7j';
const API_BASE = 'https://api.tu-zi.com/v1';

// Simulate the system prompt from api/chat.js
const systemPrompt = {
    role: 'system',
    content: `You are "天河助手", an expert urban planning assistant for Guangzhou Tianhe District housing.

**YOUR UNIQUE ABILITY**: You can control an interactive 3D map by returning JSON commands.

**RESPONSE FORMAT**:
Always respond in this exact JSON structure:
{
  "commands": [
    { "action": "updateMapFilter", "priceMin": 10000, "priceMax": 35000, "accessMin": 60, "accessMax": 100 },
    { "action": "togglePOI", "poiType": "subway", "visible": true }
  ],
  "message": "Your natural language response in Chinese or English"
}

**AVAILABLE ACTIONS**: updateMapFilter, setPersona, togglePOI, flyToArea, showRecommendations, compareAreas

**IMPORTANT**: Always return pure JSON, no markdown code blocks!`
};

async function testConversation(userMessage) {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`👤 User: "${userMessage}"`);
    console.log('='.repeat(60));

    try {
        const response = await fetch(`${API_BASE}/chat/completions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${API_KEY}`
            },
            body: JSON.stringify({
                model: 'gpt-5',
                messages: [
                    systemPrompt,
                    { role: 'user', content: userMessage }
                ],
                temperature: 0.7,
                max_tokens: 800
            })
        });

        if (!response.ok) {
            console.log('❌ API Error:', response.status);
            return;
        }

        const data = await response.json();
        const aiResponse = data.choices[0].message.content;

        console.log('\n🤖 AI Raw Response:');
        console.log(aiResponse);

        // Try to parse as JSON
        try {
            const cleanedContent = aiResponse
                .replace(/```json\n?/g, '')
                .replace(/```\n?/g, '')
                .trim();

            const parsed = JSON.parse(cleanedContent);

            console.log('\n✅ JSON Parsed Successfully!');
            console.log('\n📋 Commands to execute:');
            if (parsed.commands && parsed.commands.length > 0) {
                parsed.commands.forEach((cmd, i) => {
                    console.log(`  ${i + 1}. ${cmd.action}`);
                    console.log(`     ${JSON.stringify(cmd, null, 2).split('\n').slice(1, -1).join('\n')}`);
                });
            } else {
                console.log('  (No commands)');
            }

            console.log('\n💬 Message to user:');
            console.log(`  "${parsed.message}"`);

        } catch (parseError) {
            console.log('\n⚠️  JSON Parse Failed:', parseError.message);
            console.log('This would fall back to plain text response.');
        }

    } catch (error) {
        console.log('❌ Request Error:', error.message);
    }
}

async function runTests() {
    console.log('\n🧪 Testing JSON Command Mode with gpt-5\n');

    // Test 1: 毕业生找房
    await testConversation('我刚毕业，预算3000，要离地铁近');

    // Test 2: 地点查询
    await testConversation('珠江新城附近有哪些房源？');

    // Test 3: 学区房
    await testConversation('帮我找学区房，预算8-10万');

    // Test 4: English
    await testConversation('Show me affordable housing near metro stations');

    console.log('\n' + '='.repeat(60));
    console.log('🎉 All tests completed!');
    console.log('='.repeat(60) + '\n');
}

runTests();
