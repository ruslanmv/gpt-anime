# Quick Start Guide - WatsonX.ai Chatbot

## What Was Updated

The backend has been fully updated to use **IBM WatsonX.ai** instead of OpenAI:

### Files Modified:
1. **`apps/next/lib/backendUtils.ts`** - Added WatsonX.ai integration functions
2. **`apps/next/pages/api/chat.ts`** - Updated to use WatsonX instead of OpenAI
3. **`apps/next/.env`** - Updated with WatsonX credentials template
4. **`apps/next/.env.local.example`** - Created example configuration file

### New Files Created:
- `SETUP_WATSONX.md` - Comprehensive setup guide
- `QUICK_START.md` - This quick start guide
- `.env.local.example` - Environment configuration template

---

## Quick Setup (5 Minutes)

### 1. Set Up Credentials

Create `.env.local` file in `apps/next/` directory:

```bash
cd apps/next
cp .env.local.example .env.local
```

Edit `.env.local` and add your credentials:

```env
# Get from: https://cloud.ibm.com/iam/apikeys
WATSONX_API_KEY=your_ibm_cloud_api_key

# Get from your WatsonX.ai project settings
WATSONX_PROJECT_ID=your_project_id

# Optional: Change model
WATSONX_MODEL_ID=ibm/granite-3-8b-instruct

# Get from: https://console.cloud.google.com/apis/credentials
GOOGLE_API_KEY=your_google_api_key
NEXT_PUBLIC_GOOGLE_API_KEY=your_google_api_key
```

### 2. Install Dependencies

From the root directory:

```bash
yarn install
```

Or if you prefer npm:

```bash
npm install
```

### 3. Run the Application

#### Option A: Development Mode (Recommended)

From `apps/next` directory:
```bash
cd apps/next
yarn dev
```

Or from root directory:
```bash
yarn workspace next-app dev
```

#### Option B: Production Mode

```bash
cd apps/next
yarn build
yarn start
```

### 4. Access the Application

Open your browser and go to:
```
http://localhost:3000
```

You should see:
- A 3D animated character
- A chat interface at the bottom
- Type a message and press Enter to chat!

---

## How It Works

```
┌─────────────────────────────────────────────────────┐
│  Frontend (3D Character + Chat UI)                  │
│  http://localhost:3000                              │
└──────────────────┬──────────────────────────────────┘
                   │
                   ↓ User sends message
┌─────────────────────────────────────────────────────┐
│  Next.js API Route: /api/chat                       │
│  (apps/next/pages/api/chat.ts)                      │
└──────────────────┬──────────────────────────────────┘
                   │
          ┌────────┴────────┐
          │                 │
          ↓                 ↓
┌──────────────────┐ ┌──────────────────┐
│  WatsonX.ai      │ │  Google Cloud    │
│  (IBM Granite)   │ │  Text-to-Speech  │
│  Returns text    │ │  Returns audio   │
└────────┬─────────┘ └────────┬─────────┘
         │                    │
         └──────────┬─────────┘
                    ↓
         ┌──────────────────────┐
         │  JSON Response:      │
         │  { text, audio,      │
         │    language }        │
         └──────────┬───────────┘
                    │
                    ↓
         ┌──────────────────────┐
         │  3D Character speaks │
         │  with lip-sync       │
         └──────────────────────┘
```

---

## Testing the Chatbot

### Text Input
1. Type a message in the chat box
2. Press Enter or click Send
3. The character will respond with voice and animation

### Voice Input
1. Click the microphone icon
2. Speak your message (5 seconds)
3. The system will transcribe and respond

### Multi-Language Support
The chatbot automatically detects and responds in:
- English
- Spanish
- Italian
- Russian
- German
- Japanese

---

## Troubleshooting

### Issue: "Missing env var WATSONX_API_KEY"
**Solution:** Make sure you created `.env.local` in `apps/next/` with your API key

### Issue: "IBM IAM Token Error"
**Solution:** Your IBM Cloud API key is invalid. Create a new one at https://cloud.ibm.com/iam/apikeys

### Issue: Dependencies won't install (proxy errors)
**Solution:**
```bash
# Clear proxy settings
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy

# Try npm instead
npm install
```

### Issue: Port 3000 is in use
**Solution:**
```bash
yarn dev -p 3001
# Then access at http://localhost:3001
```

### Issue: WatsonX API returns errors
**Solution:**
- Verify your Project ID is correct
- Check that you have access to WatsonX.ai in your IBM Cloud account
- Ensure the model ID is valid (default: `ibm/granite-3-8b-instruct`)

---

## Customization

### Change the Character Personality

Edit `apps/next/pages/api/chat.ts` line 8:

```typescript
const prompt = `You are a helpful AI assistant...`;
```

### Adjust Model Parameters

In `apps/next/pages/api/chat.ts`, modify the WatsonX call (line 75-82):

```typescript
aiResponse = await WatsonX(
  messages,
  process.env.WATSONX_API_KEY!,
  process.env.WATSONX_PROJECT_ID!,
  "ibm/granite-3-8b-instruct",  // Change model
  200,  // Change max tokens
  0.3   // Change temperature (0.0 = deterministic, 1.0 = creative)
);
```

### Use a Different Model

Available WatsonX.ai models:
- `ibm/granite-3-8b-instruct` (Default: Fast, efficient)
- `ibm/granite-13b-chat-v2` (More capable, slower)
- `meta-llama/llama-2-70b-chat` (Most capable, slowest)
- `mistralai/mixtral-8x7b-instruct-v01` (Good balance)

Update in `.env.local`:
```env
WATSONX_MODEL_ID=ibm/granite-13b-chat-v2
```

---

## Architecture Details

### Backend (Next.js API Routes)
- **Location:** `apps/next/pages/api/chat.ts`
- **Runtime:** Edge runtime (serverless)
- **Endpoint:** `POST /api/chat`

### Frontend (Next.js + React)
- **Location:** `apps/next/pages/index.tsx`
- **3D Engine:** Babylon.js
- **UI Framework:** Tamagui

### Key Functions

#### `WatsonX()` - apps/next/lib/backendUtils.ts
```typescript
// Handles:
// 1. Getting IAM token from IBM Cloud
// 2. Formatting messages for Granite model
// 3. Calling WatsonX.ai generation API
// 4. Returning generated text
```

#### `synthesizeSpeechMulti()` - apps/next/lib/backendUtils.ts
```typescript
// Handles:
// 1. Auto-detecting language
// 2. Selecting appropriate voice
// 3. Converting text to speech via Google TTS
// 4. Returning base64 encoded audio
```

---

## Next Steps

1. **Add Conversation History:** Implement message persistence
2. **Add RAG:** Integrate vector database for knowledge retrieval
3. **Custom Training:** Fine-tune Granite model on your data
4. **Analytics:** Track user interactions and response quality
5. **Multi-user:** Add user authentication and session management

---

## Resources

- [WatsonX.ai Docs](https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/fm-overview.html)
- [IBM Granite Models](https://www.ibm.com/granite)
- [Setup Guide](./SETUP_WATSONX.md)
- [Next.js Docs](https://nextjs.org/docs)

---

## Need Help?

Check the detailed setup guide: `SETUP_WATSONX.md`

Common issues:
- Network/proxy errors during install → Use npm or check firewall
- Missing credentials → Follow SETUP_WATSONX.md Step 1-3
- API errors → Verify credentials and API access

---

**You're all set! Run `yarn dev` and start chatting! 🚀**
