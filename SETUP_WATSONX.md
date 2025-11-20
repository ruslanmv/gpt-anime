# WatsonX.ai Setup Guide

This guide will help you set up and run the GPT Anime chatbot with IBM WatsonX.ai integration.

## Prerequisites

- Node.js 16+ and Yarn installed
- IBM Cloud account
- Google Cloud account (for Text-to-Speech)

## Step 1: Get IBM Cloud API Key

1. Go to [IBM Cloud API Keys](https://cloud.ibm.com/iam/apikeys)
2. Click **"Create"** to create a new API key
3. Give it a name (e.g., "WatsonX Chatbot")
4. Click **"Create"** and copy the API key immediately (you won't be able to see it again!)
5. Save it securely

## Step 2: Get WatsonX.ai Project ID

1. Go to [WatsonX.ai](https://dataplatform.cloud.ibm.com/wx/home)
2. Create a new project or open an existing project
3. Click on the **"Manage"** tab
4. Click on **"General"**
5. Copy the **"Project ID"**

## Step 3: Get Google Cloud API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create a new project or select an existing one
3. Click **"Create Credentials"** > **"API Key"**
4. Copy the API key
5. Enable the following APIs:
   - Cloud Text-to-Speech API
   - Cloud Speech-to-Text API

## Step 4: Configure Environment Variables

1. Navigate to the Next.js app directory:
   ```bash
   cd apps/next
   ```

2. Copy the example environment file:
   ```bash
   cp .env.local.example .env.local
   ```

3. Edit `.env.local` with your credentials:
   ```bash
   nano .env.local
   # or use your preferred editor
   ```

4. Fill in the values:
   ```env
   WATSONX_API_KEY=your_actual_ibm_cloud_api_key
   WATSONX_PROJECT_ID=your_actual_project_id
   WATSONX_MODEL_ID=ibm/granite-3-8b-instruct
   GOOGLE_API_KEY=your_google_cloud_api_key
   NEXT_PUBLIC_GOOGLE_API_KEY=your_google_cloud_api_key
   ```

## Step 5: Install Dependencies

From the root directory of the project:

```bash
yarn install
```

This will install all dependencies for the entire monorepo.

## Step 6: Run the Backend and Frontend

The project uses Next.js, so the backend (API routes) and frontend run together.

### Development Mode

From the `apps/next` directory:

```bash
cd apps/next
yarn dev
```

Or from the root directory:

```bash
yarn workspace next-app dev
```

The application will start on **http://localhost:3000**

### Production Mode

```bash
cd apps/next
yarn build
yarn start
```

## Step 7: Test the Chatbot

1. Open your browser and go to **http://localhost:3000**
2. You should see the 3D animated character
3. Type a message in the chat box and press Enter
4. The chatbot will:
   - Send your message to WatsonX.ai (Granite model)
   - Get a response from the AI
   - Convert the response to speech using Google TTS
   - Animate the 3D character speaking

## Available Models

You can change the model in your `.env.local` file:

```env
WATSONX_MODEL_ID=ibm/granite-3-8b-instruct
```

Popular WatsonX.ai models:
- `ibm/granite-3-8b-instruct` (default, fast, efficient)
- `ibm/granite-13b-chat-v2` (more capable, slower)
- `meta-llama/llama-2-70b-chat` (most capable, slowest)

## Troubleshooting

### Error: "Missing env var WATSONX_API_KEY"

Make sure your `.env.local` file exists in `apps/next/` and contains the correct API key.

### Error: "IBM IAM Token Error"

Your IBM Cloud API key might be invalid. Create a new one and update `.env.local`.

### Error: "WatsonX API Error"

- Check that your Project ID is correct
- Verify you have access to the WatsonX.ai service in your IBM Cloud account
- Ensure the model ID is valid

### Error: "Google Cloud TTS API Error"

- Check that your Google API key is valid
- Verify the Text-to-Speech API is enabled in your Google Cloud project

### Port 3000 already in use

Change the port:
```bash
yarn dev -p 3001
```

## Architecture

```
User Browser
    ↓
Next.js Frontend (3D Character + Chat UI)
    ↓
Next.js API Route (/api/chat)
    ↓
    ├─→ WatsonX.ai (IBM Granite) → AI Response
    └─→ Google Cloud TTS → Audio
    ↓
3D Character speaks with lip-sync
```

## Features

- ✅ IBM WatsonX.ai integration with Granite 3 model
- ✅ 3D animated character with Babylon.js
- ✅ Multi-language support (English, Spanish, Italian, Russian, German, Japanese)
- ✅ Text-to-Speech with Google Cloud
- ✅ Speech-to-Text for voice input
- ✅ Lip-sync animations
- ✅ Responsive chat interface

## Next Steps

1. Customize the chatbot personality by editing the prompt in `apps/next/pages/api/chat.ts`
2. Adjust the model parameters (temperature, max_tokens) in the same file
3. Modify the 3D character model in `apps/next/lib/models/`
4. Add custom animations in `apps/next/lib/babylonjs/Humanoid.ts`

## Resources

- [WatsonX.ai Documentation](https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/fm-overview.html)
- [IBM Granite Models](https://www.ibm.com/granite)
- [Google Cloud TTS Documentation](https://cloud.google.com/text-to-speech/docs)
- [Next.js Documentation](https://nextjs.org/docs)
- [Babylon.js Documentation](https://doc.babylonjs.com/)

## Support

For issues or questions:
- Check the console logs in your browser (F12)
- Check the terminal logs where you ran `yarn dev`
- Review the error messages and follow the troubleshooting steps above
