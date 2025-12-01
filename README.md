# Tianhe Housing Analytics - AI Enhanced Version 🏠🤖

An interactive 3D visualization tool for analyzing housing prices and accessibility in Guangzhou Tianhe District, **now powered by AI conversation interface**.

## 🎯 New Features: AI Chatbot Integration

### What's New?
- **Natural Language Control**: Talk to the map! Instead of manually adjusting filters, just describe what you're looking for
- **LLM Function Calling**: The AI assistant can control the map by calling functions (filter, highlight areas, show POIs, etc.)
- **Persona-based Recommendations**: AI understands different user needs (fresh graduate, young family, retiree)
- **Bilingual Support**: Works in both English and Chinese

### Example Interactions

**User**: "我刚毕业，预算3000，要离地铁近"
**AI**: *[Automatically filters map to show housing <35k/sqm near metro stations]*
"已为您筛选出3万5以下且靠近地铁的区域 🚇 推荐您看看员村和石牌桥，性价比非常高！"

**User**: "帮我找学区房，预算8-10万"
**AI**: *[Filters price 80-100k, shows school POIs, switches to family persona]*
"这些区域教育资源丰富，非常适合有孩子的家庭 🏫"

## 🚀 Quick Start

### Option 1: Deploy to Vercel (Recommended)

1. **Fork this repository**

2. **Get API Key**
   - This project uses a custom OpenAI-compatible API endpoint: `https://api.tu-zi.com/v1`
   - Get your API key from your API provider
   - Copy the key (usually starts with `sk-...`)

3. **Deploy to Vercel**
   ```bash
   # Install Vercel CLI
   npm i -g vercel

   # Deploy
   vercel
   ```

4. **Set Environment Variable**
   - Go to your Vercel Dashboard → Project Settings → Environment Variables
   - Add: `OPENAI_API_KEY` = `sk-your-actual-key`
   - Redeploy the project

5. **Done!** Your app is live at `https://your-project.vercel.app`

### Option 2: Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/UGOD-5104.git
   cd UGOD-5104
   ```

2. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

4. **Run development server**
   ```bash
   vercel dev
   ```

5. **Open browser**: http://localhost:3000

## 🛠 Technical Architecture

### Frontend (Vanilla React + Deck.gl)
- **3D Visualization**: Deck.gl for high-performance WebGL rendering
- **Map Controls**: React state management for filters, personas, POI layers
- **Chat UI**: Custom-built chat interface with typing indicators and quick prompts

### Backend (Vercel Serverless Functions)
- **API Proxy**: `/api/chat.js` - Securely calls OpenAI API (hides your API key)
- **Function Calling**: Defines 6 map control functions AI can invoke:
  - `updateMapFilter()` - Filter by price/accessibility
  - `setPersona()` - Switch viewing persona
  - `togglePOI()` - Show/hide amenity layers
  - `flyToArea()` - Navigate to specific neighborhoods
  - `showRecommendations()` - Highlight top matches
  - `compareAreas()` - Compare two locations

### AI System Prompt
Located in `api/chat.js`, the system prompt defines:
- **Role**: Urban planning assistant specializing in Tianhe District
- **Personality**: Warm, professional, concise (2-3 sentences max)
- **Behavior**: Always execute functions FIRST, then explain
- **Knowledge**: Understands Chinese area names, local context, user personas

## 📊 Features Overview

### Map Visualization
- **Bubble Size** = Housing Price
- **Bubble Color** = Accessibility Score (gradient from purple to green)
- **Interactive**: Click to select, hover for details
- **POI Layers**: Metro 🚇, Malls 🛍️, Schools 🏫, Parks 🌳, Hospitals 🏥

### User Personas
- **Fresh Graduate** 👨‍🎓: Budget-conscious (<4w/sqm), needs metro access
- **Young Family** 👨‍👩‍👧: Values schools/parks, higher budget (5-10w/sqm)
- **Retiree** 👴: Needs hospitals/parks, prefers quiet areas

### Accessibility Analysis
- **Static Buffer**: 1km radius circle
- **Dynamic Isochrone**: 15-minute walking catchment (real road network)

### Comparison Mode
- Select two points to compare side-by-side
- Price gap visualization
- Access score comparison
- Value ratio analysis

## 🎨 AI Conversation Design Principles

### 1. Action-First Philosophy
The AI doesn't just talk—it acts. When users describe needs, the AI immediately calls functions to update the map before responding.

### 2. Context-Aware Responses
The AI understands:
- Chinese colloquialisms (3000 = 30,000 CNY/sqm, "地铁" = metro)
- Area names (珠江新城, 员村, 石牌桥, etc.)
- Implicit needs (graduate = budget-sensitive, family = needs schools)

### 3. Progressive Disclosure
- **Quick Prompts**: Show 4 example queries on first interaction
- **Function Actions**: Display which functions were called
- **Natural Follow-up**: AI can ask clarifying questions

## 📂 File Structure

```
UGOD-5104/
├── index.html                  # Main app (React + Deck.gl)
├── api/
│   └── chat.js                 # OpenAI API proxy (Vercel Function)
├── final_academic_tianhe_blocks.csv  # Housing data
├── house1-4.png                # Housing images
├── vercel.json                 # Vercel deployment config
├── env.example                 # Environment variables template
└── README.md                   # This file
```

## 🧪 Testing the AI

### Test Queries (English)
```
"I'm a fresh grad, budget 3000, need metro access"
"Show me family-friendly areas with good schools"
"Compare Zhujiang New Town vs Yuancun"
"Fly to Tianhe Park area"
```

### Test Queries (Chinese)
```
"我刚毕业，预算3000，要离地铁近"
"帮我找学区房，预算8-10万"
"珠江新城和员村哪个性价比高？"
"飞到天河公园附近"
```

## 🔧 Customization

### Modify AI Personality
Edit the `systemPrompt` in `api/chat.js`:
```javascript
const systemPrompt = {
  role: 'system',
  content: `You are a [your custom persona]...`
};
```

### Add New Functions
1. Define function in `api/chat.js` → `tools` array
2. Implement handler in `index.html` → `mapControlFunctions`

### Change Area Names
Update `flyToArea()` coordinates in `index.html`:
```javascript
const areas = {
  your_area: { longitude: XX.XXX, latitude: XX.XXX, zoom: 14 }
};
```

## 💰 Cost Estimation

**API Costs** (Custom endpoint: api.tu-zi.com):
- Check with your API provider for pricing details
- Costs typically based on token usage

**Standard OpenAI pricing reference** (if applicable):
- Input: $2.50 per 1M tokens
- Output: $10.00 per 1M tokens

**Average conversation** (~10 messages):
- ~5,000 tokens total
- Cost varies by provider

**Vercel Hosting**: Free tier (sufficient for prototype)

## 🐛 Troubleshooting

### "API request failed"
- **Check**: Is `OPENAI_API_KEY` set correctly in Vercel?
- **Check**: Is your API key valid? Test at https://platform.openai.com/playground

### Functions not executing
- **Check**: Browser console for errors (`F12` → Console tab)
- **Check**: API response - does it include `tool_calls`?

### Map not updating
- **Check**: React state in DevTools
- **Try**: Refresh the page and retry

## 📚 Learn More

- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Deck.gl Documentation](https://deck.gl/)
- [Vercel Serverless Functions](https://vercel.com/docs/functions)

## 📝 Assignment Context

**Course**: UGOD 5104 - Urban Geography & Data Science
**Topic**: Spatial Analysis of Housing Affordability vs. Accessibility
**Authors**: Lingcen Liao, Wei He

**Research Question**: How does proximity to urban amenities affect housing prices in Guangzhou's CBD?

**Novel Contribution**: This project demonstrates how LLM-powered interfaces can democratize complex spatial analysis tools, making urban planning insights accessible to non-experts through natural conversation.

## 📄 License

MIT License - Feel free to use for educational purposes.

## 🙏 Acknowledgments

- OpenAI GPT-4 for function calling capabilities
- Deck.gl team for amazing visualization framework
- Vercel for free hosting and serverless infrastructure

---

**Need help?** Open an issue on GitHub or contact the authors.

🚀 **Happy exploring Tianhe housing with AI!**
