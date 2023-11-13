export async function recordVoice(): Promise<{ audioBlob: Blob; stopRecording: () => void }> {
  return new Promise((resolve) => {
    const chunks: Blob[] = [];
    let mediaRecorder: MediaRecorder | null = null;

    navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.start();

      mediaRecorder.addEventListener("dataavailable", (event) => {
        chunks.push(event.data);
      });

      const stopRecording = () => {
        mediaRecorder?.stop();
        stream.getAudioTracks().forEach((track) => track.stop());

        const audioBlob = new Blob(chunks, { type: "audio/wav" });
        resolve({ audioBlob, stopRecording });
      };

      const recordButton = document.getElementById("record-button");
      if (recordButton) {
        recordButton.addEventListener("mouseup", stopRecording);
        recordButton.addEventListener("touchend", stopRecording);
      }
    });
  });
}

export function speechToText(audioBlob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const audioData = reader.result as string;
      const audioContent = audioData.split(",")[1];

      const apiKey = process.env.GOOGLE_API_KEY;
      const apiURL = `https://speech.googleapis.com/v1/speech:recognize?key=${apiKey}`;
      const requestBody = {
        config: {
          encoding: "LINEAR16",
          sampleRateHertz: 16000,
          languageCode: "en-US",
        },
        audio: {
          content: audioContent,
        },
      };

      const xhr = new XMLHttpRequest();
      xhr.open("POST", apiURL, true);
      xhr.setRequestHeader("Content-Type", "application/json");
      xhr.onload = () => {
        if (xhr.status === 200) {
          const response = JSON.parse(xhr.responseText);
          const transcript = response.results[0]?.alternatives[0]?.transcript || "";
          resolve(transcript);
        } else {
          reject(new Error("Error converting speech to text."));
        }
      };
      xhr.onerror = () => {
        reject(new Error("Error converting speech to text."));
      };
      xhr.send(JSON.stringify(requestBody));
    };
    reader.onerror = () => {
      reject(new Error("Error reading audio file."));
    };
    reader.readAsDataURL(audioBlob);
  });
}

export async function recordAndTranscribe(): Promise<string> {
  //const { audioBlob, stopRecording } = await recordVoice();
  //stopRecording();
  //const transcribedText = await speechToText(audioBlob);
  const transcribedText = 'Hello'
  return transcribedText;
}


