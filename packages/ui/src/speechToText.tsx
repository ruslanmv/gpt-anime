
export class AudioRecorder {
  private recorder: MediaRecorder;
  private audioChunks: Blob[];

  constructor(stream: MediaStream) {
    this.recorder = new MediaRecorder(stream);
    this.audioChunks = [];

    this.recorder.addEventListener('dataavailable', this.handleDataAvailable);
  }

  private handleDataAvailable = (event: BlobEvent) => {
    if (event.data.size > 0) {
      this.audioChunks.push(event.data);
    }
  };

  start() {
    this.recorder.start();
  }

  stop(): Promise<Blob> {
    return new Promise((resolve) => {
      this.recorder.addEventListener('stop', () => {
        resolve(new Blob(this.audioChunks));
      });

      this.recorder.stop();
    });
  }
}

export async function recordAndTranscribe(): Promise<string> {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const audioRecorder = new AudioRecorder(stream);

  audioRecorder.start();

  return new Promise<string>(async (resolve, reject) => {
    setTimeout(async () => {
      try {
        const audioBlob = await audioRecorder.stop();
        console.log('audioBlob:', audioBlob); // Print audioBlob in the log

        // Play the recorded sound
        const audioURL = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioURL);
        audio.play();

        const transcription = await speechToText(audioBlob);
        if (typeof transcription === 'string') {
          resolve(transcription);
        } else {
          reject(new Error('Invalid transcription'));
        }
      } catch (error) {
        reject(error);
      }
    }, 5000);
  });
}

// Function to convert audio blob to base64 encoded string
const audioBlobToBase64 = (blob) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const arrayBuffer = reader.result;
      let base64Audio;

      if (typeof arrayBuffer === 'string') {
        base64Audio = btoa(arrayBuffer);
      } else if (arrayBuffer instanceof ArrayBuffer) {
        const uint8Array = new Uint8Array(arrayBuffer);
        base64Audio = btoa(
          uint8Array.reduce(
            (data, byte) => data + String.fromCharCode(byte),
            ''
          )
        );
      } else {
        reject('Invalid array buffer');
        return;
      }

      resolve(base64Audio);
    };
    reader.onerror = reject;
    reader.readAsArrayBuffer(blob);
  });
};

// Function to convert audio blob to text
async function speechToText(audioBlob) {
  return new Promise(async (resolve, reject) => {


    if (!process.env.GOOGLE_API_KEY) {
      throw new Error("GOOGLE_API_KEY not found in theprocess.env environment");
    }

    const apiKey = process.env.GOOGLE_API_KEY;

    try {
      const base64Audio = await audioBlobToBase64(audioBlob);
      //console.log('Base64 audio:', base64Audio);

      const startTime = performance.now();

      const requestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          config: {
            encoding: 'WEBM_OPUS',
            sampleRateHertz: 48000,
            languageCode: 'en-US',
          },
          audio: {
            content: base64Audio,
          },
        }),
      };

      const response = await fetch(
        `https://speech.googleapis.com/v1/speech:recognize?key=${apiKey}`,
        requestOptions
      );

      const data = await response.json();
      const endTime = performance.now();
      const elapsedTime = endTime - startTime;

      // console.log('API response:', data);
      console.log('Voice Recognition - Time taken (ms):', elapsedTime);

      if (data.results && data.results.length > 0) {
        const transcription = data.results[0].alternatives[0].transcript;
        resolve(transcription);
      } else {
        reject('No transcription available');
      }
    } catch (error) {
      reject(error);
    }
  });
}