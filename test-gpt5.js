// 快速测试 gpt-5 模型
const API_KEY = 'sk-k4TRuzAh3xPJREVysLh25UggIbiptLi8PaDPP6ij6CGZid7j';
const API_BASE = 'https://api.tu-zi.com/v1';

async function testGPT5() {
    console.log('Testing gpt-5 model...\n');

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
                    { role: 'user', content: 'Hello! Say "gpt-5 working" if you can read this.' }
                ],
                max_tokens: 50
            })
        });

        const data = await response.json();

        if (response.ok) {
            console.log('✅ gpt-5 model available!');
            console.log(`Model: ${data.model}`);
            console.log(`Response: ${data.choices[0].message.content}`);
        } else {
            console.log('❌ gpt-5 not available');
            console.log(`Error: ${data.error?.message || JSON.stringify(data)}`);
        }
    } catch (error) {
        console.log('❌ Error:', error.message);
    }
}

testGPT5();
