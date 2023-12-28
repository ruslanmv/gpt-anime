import { ChatMessage } from "@my/ui/types/Chat";
import { createParser, ParsedEvent, ReconnectInterval } from "eventsource-parser";

export type OpenAIStreamPayload = {
  model: string;
  messages: ChatMessage[];
  temperature: number;
  top_p: number;
  frequency_penalty: number;
  presence_penalty: number;
  max_tokens: number;
  stream: boolean;
  n: number;
};

export async function OpenAIStream(payload: OpenAIStreamPayload) {
  const encoder = new TextEncoder();
  const decoder = new TextDecoder();

  let counter = 0;

  const res = await fetch("https://api.openai.com/v1/chat/completions", {
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${process.env.OPENAI_API_KEY ?? ""}`,
    },
    method: "POST",
    body: JSON.stringify(payload),
  });

  const stream = new ReadableStream({
    async start(controller) {
      // callback
      function onParse(event: ParsedEvent | ReconnectInterval) {
        if (event.type === "event") {
          const data = event.data;
          // https://beta.openai.com/docs/api-reference/completions/create#completions/create-stream
          if (data === "[DONE]") {
            controller.close();
            return;
          }

          try {
            const json = JSON.parse(data);
            const text = json.choices[0].delta?.content || "";
            if (counter < 2 && (text.match(/\n/) || []).length) {
              // this is a prefix character (i.e., "\n\n"), do nothing
              return;
            }
            const queue = encoder.encode(text);
            controller.enqueue(queue);
            counter++;
          } catch (e) {
            // maybe parse error
            controller.error(e);
          }
        }
      }

      // stream response (SSE) from OpenAI may be fragmented into multiple chunks
      // this ensures we properly read chunks and invoke an event for each SSE event stream
      const parser = createParser(onParse);
      // https://web.dev/streams/#asynchronous-iteration
      for await (const chunk of res.body as any) {
        parser.feed(decoder.decode(chunk));
      }
    },
  });

  return stream;
}


export type OpenAIPayload = {
  model: string;
  messages: Array<{ role: string; content: string }>;
  temperature: number;
  top_p: number;
  frequency_penalty: number;
  presence_penalty: number;
  max_tokens: number;
  n: number;
};

export type OpenAIResponse = {
  id: string;
  object: string;
  created: number;
  model: string;
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
  choices: Array<{
    message: {
      role: string;
      content: string;
    };
    finish_reason: string;
    index: number;
  }>;
};

export const OpenAI = async (payload: OpenAIPayload): Promise<OpenAIResponse> => {
  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(`OpenAI API Error: ${errorData.error.message}`);
  }

  return await response.json();
};


////// For testing purposes.

export function recursiveStreamEnqueue(
  controller: ReadableStreamDefaultController<any>,
  messageTokens: string[],
  index: number,
  timeBetweenTokens = 100
) {
  if (index >= messageTokens.length) {
    controller.close();
    return;
  }

  setTimeout(function () {
    console.log(messageTokens[index]);
    var enc = new TextEncoder();
    controller.enqueue(enc.encode(messageTokens[index] + " "));
    recursiveStreamEnqueue(controller, messageTokens, ++index);
  }, timeBetweenTokens);
}

export function streamMock(messageTokens: string[]): ReadableStream {
  return new ReadableStream({
    start(controller) {
      recursiveStreamEnqueue(controller, messageTokens, 0);
    },
  });
}
////////////

export async function synthesizeSpeech(text: string): Promise<string> {
  if (!process.env.GOOGLE_API_KEY) {
    throw new Error("GOOGLE_API_KEY not found in the environment");
  }
  if (typeof text !== "string") {
    throw new Error(`Invalid input type: ${typeof text}. Type has to be text or SSML.`);
  }
  const apiKey = process.env.GOOGLE_API_KEY;
  const apiURL = `https://texttospeech.googleapis.com/v1/text:synthesize?key=${apiKey}`;
  const requestBody = {
    input: {
      text,
    },
    voice: { languageCode: 'en-US', name: 'en-US-Neural2-H', ssmlGender: 'FEMALE' },
    //voice: { languageCode: 'it-IT', name: 'it-IT-Standard-B', ssmlGender: 'FEMALE' },
    audioConfig: {
      audioEncoding: "MP3",
    },
  };
  const response = await fetch(apiURL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestBody),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(`Google Cloud TTS API Error: ${errorData.error.message}`);
  }
  const responseData = await response.json();
  const audioContent = responseData.audioContent;

  return audioContent;
}

import { franc } from 'franc';
// Language Detector Function
async function detectLanguage(text: string): Promise<string> {
  const supportedLanguages: Record<string, string> = {
    eng: 'english',
    spa: 'spanish',
    ita: 'italian',
    rus: 'russian',
    deu: 'german',
    jpn: 'japanese',
  };

  // For simplicity, let's assume the language is determined based on the first character of the text
  const firstChar = text.charAt(0);

  if (/[áéíóúñ]/.test(firstChar)) {
    return "spanish";
  } else if (/[àèìòù]/.test(firstChar)) {
    return "italian";
  } else if (/[дйцукенгшщзхъё]/.test(firstChar)) {
    return "russian";
  } else if (/[äöüß]/.test(firstChar)) {
    return "german";
  } else if (/[あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん]/.test(firstChar)) {
    return "japanese";
  } else {
    const detectedLanguageCode: string = franc(text);
    console.log('detected language code :', detectedLanguageCode);
    const detectedLanguage: string = supportedLanguages[detectedLanguageCode] || 'english';
    console.log('detected language :', detectedLanguage);
    return detectedLanguage;
  }
}

// Modified synthesizeSpeechMulti function
export async function synthesizeSpeechMulti(text: string): Promise<{ audioContent: string, language: string }> {
  if (!process.env.GOOGLE_API_KEY) {
    throw new Error("GOOGLE_API_KEY not found in the environment");
  }
  if (typeof text !== "string") {
    throw new Error(`Invalid input type: ${typeof text}. Type has to be text or SSML.`);
  }
  const language = await detectLanguage(text);

  let languageCode;
  let voiceName;
  let ssmlGender;
  //https://cloud.google.com/text-to-speech/docs/voices
  switch (language) {
    case "english":
      languageCode = "en-US";
      voiceName = "en-US-Neural2-H";
      ssmlGender = "FEMALE";
      break;
    case "spanish":
      languageCode = "es-US";
      voiceName = "es-US-Neural2-A";
      ssmlGender = "FEMALE";
      break;
    case "italian":
      languageCode = "it-IT";
      voiceName = "it-IT-Neural2-A";
      ssmlGender = "FEMALE";
      break;
    case "russian":
      languageCode = "ru-RU";
      voiceName = "ru-RU-Standard-C";
      ssmlGender = "FEMALE";
      break;
    case "german":
      languageCode = "de-DE";
      voiceName = "de-DE-Neural2-F";
      ssmlGender = "FEMALE";
      break;
    case "japanese":
      languageCode = "ja-JP";
      voiceName = "ja-JP-Neural2-B";
      ssmlGender = "FEMALE";
      break;
    default:
      throw new Error(`Unsupported language: ${language}`);
  }

  const apiKey = process.env.GOOGLE_API_KEY;
  const apiURL = `https://texttospeech.googleapis.com/v1/text:synthesize?key=${apiKey}`;
  const requestBody = {
    input: {
      text,
    },
    voice: {
      languageCode,
      name: voiceName,
      ssmlGender,
    },
    audioConfig: {
      audioEncoding: "MP3",
    },
  };

  const response = await fetch(apiURL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestBody),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(`Google Cloud TTS API Error: ${errorData.error.message}`);
  }

  const responseData = await response.json();
  const audioContent = responseData.audioContent;

  return { audioContent, language };
}
