import { ChatMessage } from "@my/ui/types/Chat";
import { OpenAI, OpenAIPayload, synthesizeSpeechMulti } from "lib/backendUtils";
import { dummyBotAudio, dummyBotMessages } from "lib/dummyResponses";

const MAX_REQUEST_BODY_LENGTH = 1200;
const MAX_WORD_SUGGESTION = 60;

const prompt = `Prompt - You are an AI language model, and you will be chatting as a fun, upbeat, and friendly female character. Make sure not to mention your role as an AI or the character you are portraying. Keep your responses concise, no longer than ${MAX_WORD_SUGGESTION} words per response. Engage in a lively and positive conversation with the user.`;

const initialBotMessage: ChatMessage = {
  role: "assistant",
  content: prompt,
};

const USE_DUMMY_MESSAGES = false;

if (!process.env.OPENAI_API_KEY) {
  throw new Error("Missing env var from OpenAI");
}

export const config = {
  runtime: "edge",
};

export default async function handler(req: Request): Promise<Response> {
  const requestBody = await req.text();

  if (requestBody.length > MAX_REQUEST_BODY_LENGTH) {
    console.error(`Request body exceeds ${MAX_REQUEST_BODY_LENGTH} characters.`);
    return new Response(
      JSON.stringify({ error: `Request body exceeds ${MAX_REQUEST_BODY_LENGTH} characters.` }),
      { status: 400 }
    );
  }

  const messages: ChatMessage[] = JSON.parse(requestBody);

  if (!messages || messages.length === 0) {
    const errorMessage = "No messages found in the request.";
    console.error(errorMessage);
    return new Response(JSON.stringify({ error: errorMessage }), {
      status: 400,
    });
  }

  // Prepend the initial bot message containing the prompt.
  messages.unshift(initialBotMessage);

  const payload: OpenAIPayload = {
    model: "gpt-3.5-turbo",
    messages,
    temperature: 0.7,
    top_p: 1,
    frequency_penalty: 0,
    presence_penalty: 0,
    max_tokens: 200,
    n: 1,
  };

  if (USE_DUMMY_MESSAGES) {
    const message = dummyBotMessages[0];
    const audio = dummyBotAudio[0];
    // Create a JSON response containing both text and audio
    const DUMMY_JSON = {
      text: message,
      audio: audio,
    };
    console.log(`Response DUMMY_JSON :`, DUMMY_JSON);
    // Create a new Response DUMMY object with the JSON response and appropriate headers
    return new Response(JSON.stringify(DUMMY_JSON), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  }

  let aiResponse = "";
  let audioContent = "";
  let language = "";

  try {
    const response = await OpenAI(payload);
    aiResponse = response.choices[0]?.message.content;
  } catch (error) {
    console.error(error);
    return new Response(JSON.stringify({ error: "Error processing OpenAI response." }), {
      status: 500,
    });
  }

  if (process.env.NODE_ENV === "development") {
    console.log("Input messages (with initial bot message):", messages);
    console.log(`AI Response:`, aiResponse);
  }

  try {
    // Convert aiResponse to audio
    const result = await synthesizeSpeechMulti(aiResponse);
    audioContent = result.audioContent;
    language = result.language;
  } catch (error) {
    console.error(error);
    return new Response(JSON.stringify({ error: "Error fetching audio." }), {
      status: 500,
    });
  }

  // Create a JSON response containing both text and audio
  const jsonResponse = {
    text: aiResponse,
    audio: audioContent,
    language: language
  };

  if (process.env.NODE_ENV === "development") {
    // Check if both keys are not null or empty
    if (jsonResponse.text && jsonResponse.audio) {
      console.log("OK");
    } else {
      console.log("Audio or text keys are null or empty.");
    }
  }

  // Create a new Response object with the JSON response and appropriate headers
  return new Response(JSON.stringify(jsonResponse), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}
