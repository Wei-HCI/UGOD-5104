// API 测试脚本
// 用于验证 api.tu-zi.com 是否支持 function calling

const API_KEY = 'sk-k4TRuzAh3xPJREVysLh25UggIbiptLi8PaDPP6ij6CGZid7j';
const API_BASE = 'https://api.tu-zi.com/v1';

console.log('🔍 Testing API connection...\n');

// Test 1: 简单对话测试
async function testBasicChat() {
    console.log('📝 Test 1: Basic chat completion');
    try {
        const response = await fetch(`${API_BASE}/chat/completions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${API_KEY}`
            },
            body: JSON.stringify({
                model: 'gpt-4o',
                messages: [
                    { role: 'user', content: 'Hello! Just say "API working" if you can read this.' }
                ],
                max_tokens: 50
            })
        });

        if (!response.ok) {
            const error = await response.text();
            console.log('❌ Basic chat FAILED');
            console.log(`Status: ${response.status}`);
            console.log(`Error: ${error}\n`);
            return false;
        }

        const data = await response.json();
        console.log('✅ Basic chat SUCCESS');
        console.log(`Response: ${data.choices[0].message.content}`);
        console.log(`Model used: ${data.model}\n`);
        return true;
    } catch (error) {
        console.log('❌ Basic chat ERROR:', error.message, '\n');
        return false;
    }
}

// Test 2: Function Calling 测试
async function testFunctionCalling() {
    console.log('🔧 Test 2: Function calling support');
    try {
        const response = await fetch(`${API_BASE}/chat/completions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${API_KEY}`
            },
            body: JSON.stringify({
                model: 'gpt-4o',
                messages: [
                    { role: 'user', content: 'Filter the map to show houses under 30000 CNY per sqm' }
                ],
                tools: [
                    {
                        type: 'function',
                        function: {
                            name: 'updateMapFilter',
                            description: 'Filter housing by price',
                            parameters: {
                                type: 'object',
                                properties: {
                                    priceMax: {
                                        type: 'number',
                                        description: 'Maximum price in CNY'
                                    }
                                },
                                required: ['priceMax']
                            }
                        }
                    }
                ],
                tool_choice: 'auto'
            })
        });

        if (!response.ok) {
            const error = await response.text();
            console.log('❌ Function calling FAILED');
            console.log(`Status: ${response.status}`);
            console.log(`Error: ${error}\n`);
            return false;
        }

        const data = await response.json();

        if (data.choices[0].message.tool_calls) {
            console.log('✅ Function calling SUPPORTED');
            console.log(`Function called: ${data.choices[0].message.tool_calls[0].function.name}`);
            console.log(`Arguments: ${data.choices[0].message.tool_calls[0].function.arguments}\n`);
            return true;
        } else {
            console.log('⚠️  Function calling NOT supported (got text response instead)');
            console.log(`Response: ${data.choices[0].message.content}\n`);
            return false;
        }
    } catch (error) {
        console.log('❌ Function calling ERROR:', error.message, '\n');
        return false;
    }
}

// Test 3: 测试 gpt-4o-mini 模型
async function testGPT4oModel() {
    console.log('🤖 Test 3: GPT-4o model availability');
    try {
        const response = await fetch(`${API_BASE}/chat/completions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${API_KEY}`
            },
            body: JSON.stringify({
                model: 'gpt-4o',
                messages: [
                    { role: 'user', content: 'Say your model name' }
                ],
                max_tokens: 30
            })
        });

        const data = await response.json();

        if (response.ok) {
            console.log('✅ GPT-4o available');
            console.log(`Model: ${data.model}`);
            console.log(`Response: ${data.choices[0].message.content}\n`);
            return true;
        } else {
            console.log('⚠️  GPT-4o not available, error:', data.error?.message || 'Unknown');
            return false;
        }
    } catch (error) {
        console.log('❌ Model test ERROR:', error.message, '\n');
        return false;
    }
}

// Test 4: 测试中文对话
async function testChineseChat() {
    console.log('🇨🇳 Test 4: Chinese language support');
    try {
        const response = await fetch(`${API_BASE}/chat/completions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${API_KEY}`
            },
            body: JSON.stringify({
                model: 'gpt-4o',
                messages: [
                    { role: 'user', content: '你好！用中文回答：你能帮我找房子吗？' }
                ],
                max_tokens: 50
            })
        });

        if (!response.ok) {
            const error = await response.text();
            console.log('❌ Chinese chat FAILED');
            console.log(`Error: ${error}\n`);
            return false;
        }

        const data = await response.json();
        console.log('✅ Chinese support OK');
        console.log(`Response: ${data.choices[0].message.content}\n`);
        return true;
    } catch (error) {
        console.log('❌ Chinese chat ERROR:', error.message, '\n');
        return false;
    }
}

// 运行所有测试
async function runAllTests() {
    console.log('='.repeat(60));
    console.log('🧪 API Testing Suite for api.tu-zi.com');
    console.log('='.repeat(60) + '\n');

    const results = {
        basicChat: await testBasicChat(),
        functionCalling: await testFunctionCalling(),
        gpt4oModel: await testGPT4oModel(),
        chineseChat: await testChineseChat()
    };

    console.log('='.repeat(60));
    console.log('📊 Test Results Summary:');
    console.log('='.repeat(60));
    console.log(`Basic Chat:        ${results.basicChat ? '✅ PASS' : '❌ FAIL'}`);
    console.log(`Function Calling:  ${results.functionCalling ? '✅ PASS' : '❌ FAIL'}`);
    console.log(`GPT-4o Model:      ${results.gpt4oModel ? '✅ PASS' : '❌ FAIL'}`);
    console.log(`Chinese Support:   ${results.chineseChat ? '✅ PASS' : '❌ FAIL'}`);
    console.log('='.repeat(60) + '\n');

    const allPassed = Object.values(results).every(r => r === true);

    if (allPassed) {
        console.log('🎉 All tests PASSED! API is ready for integration.\n');
    } else {
        console.log('⚠️  Some tests failed. Check the details above.\n');

        if (!results.functionCalling) {
            console.log('💡 Note: Function calling is REQUIRED for this project.');
            console.log('   If not supported, we need to use alternative approach.\n');
        }
    }

    return results;
}

// 执行测试
runAllTests().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
});
