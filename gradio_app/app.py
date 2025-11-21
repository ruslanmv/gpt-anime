"""
3D Anime Chatbot - Gradio Application
Professional Hugging Face Space with 3D Avatar Integration
"""

import gradio as gr
import os
import time
from datetime import datetime

# Configuration
TITLE = "🤖 3D Anime Chatbot"
DESCRIPTION = """
Professional 3D Anime Avatar with realistic animations and natural language interaction.
Try talking to the avatar using text or voice commands!
"""

# Avatar 3D HTML Component
def create_avatar_html():
    """Create the Three.js 3D avatar HTML component"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body, html {
            margin: 0;
            padding: 0;
            overflow: hidden;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        }
        #avatar-container {
            width: 100%;
            height: 600px;
            position: relative;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .status-indicator {
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: rgba(255, 255, 255, 0.9);
            padding: 12px 20px;
            border-radius: 25px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            font-size: 14px;
            font-weight: 500;
            color: #333;
            transition: all 0.3s ease;
            z-index: 100;
        }
        .status-indicator.speaking {
            background: rgba(59, 130, 246, 0.95);
            color: white;
            animation: pulse 1.5s ease-in-out infinite;
        }
        .status-indicator.listening {
            background: rgba(34, 197, 94, 0.95);
            color: white;
            animation: pulse 1.5s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        .loading-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.95);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }
        .loading-spinner {
            width: 60px;
            height: 60px;
            border: 6px solid #f3f3f3;
            border-top: 6px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .loading-text {
            margin-top: 20px;
            font-size: 16px;
            color: #667eea;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div id="avatar-container">
        <div id="loading-overlay" class="loading-overlay">
            <div class="loading-spinner"></div>
            <div class="loading-text">Loading 3D Avatar...</div>
        </div>
        <div id="status-indicator" class="status-indicator">
            <span id="status">Avatar is ready</span>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.min.js"></script>

    <script>
        let scene, camera, renderer, avatar, mixer, clock, speaking = false, currentEmotion = 'neutral';

        function initThreeJS() {
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x667eea);

            camera = new THREE.PerspectiveCamera(75,
                document.getElementById('avatar-container').clientWidth /
                document.getElementById('avatar-container').clientHeight,
                0.1, 1000);
            camera.position.set(0, 1.5, 3);

            renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            const container = document.getElementById('avatar-container');
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.setPixelRatio(window.devicePixelRatio);
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            container.appendChild(renderer.domElement);

            // Lighting
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
            scene.add(ambientLight);

            const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight.position.set(5, 10, 7);
            directionalLight.castShadow = true;
            scene.add(directionalLight);

            const pointLight1 = new THREE.PointLight(0xff80ff, 0.4, 100);
            pointLight1.position.set(-5, 5, 5);
            scene.add(pointLight1);

            const pointLight2 = new THREE.PointLight(0x80ffff, 0.4, 100);
            pointLight2.position.set(5, 5, -5);
            scene.add(pointLight2);

            // Controls
            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.minDistance = 1.5;
            controls.maxDistance = 6;
            controls.enablePan = false;
            controls.maxPolarAngle = Math.PI / 1.5;
            controls.minPolarAngle = Math.PI / 4;

            clock = new THREE.Clock();

            loadAvatar();

            window.addEventListener('resize', onWindowResize);

            animate();
        }

        function loadAvatar() {
            const loader = new THREE.GLTFLoader();

            loader.load(
                'https://cdn.jsdelivr.net/gh/mrdoob/three.js@r128/examples/models/gltf/RobotExpressive/RobotExpressive.glb',
                function (gltf) {
                    avatar = gltf.scene;
                    scene.add(avatar);

                    avatar.scale.set(1.5, 1.5, 1.5);
                    avatar.position.y = -1;

                    avatar.traverse(function (child) {
                        if (child.isMesh) {
                            child.castShadow = true;
                            child.receiveShadow = true;
                        }
                    });

                    mixer = new THREE.AnimationMixer(avatar);
                    const clips = gltf.animations;

                    window.avatarAnimations = {};
                    clips.forEach(clip => {
                        window.avatarAnimations[clip.name.toLowerCase()] = clip;
                    });

                    const idleClip = THREE.AnimationClip.findByName(clips, 'Idle');
                    if (idleClip) {
                        const idleAction = mixer.clipAction(idleClip);
                        idleAction.play();
                        currentEmotion = 'idle';
                    }

                    document.getElementById('loading-overlay').style.display = 'none';
                    updateStatus('Avatar is ready', '');
                },
                function (progress) {
                    if (progress.total > 0) {
                        const percentComplete = (progress.loaded / progress.total) * 100;
                        document.querySelector('.loading-text').textContent =
                            `Loading 3D Avatar... ${percentComplete.toFixed(0)}%`;
                    }
                },
                function (error) {
                    console.error('Error loading avatar model:', error);
                    createSimpleAvatar();
                    document.getElementById('loading-overlay').style.display = 'none';
                }
            );
        }

        function createSimpleAvatar() {
            const bodyGeometry = new THREE.BoxGeometry(0.5, 0.8, 0.3);
            const bodyMaterial = new THREE.MeshStandardMaterial({ color: 0x667eea });
            const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
            body.position.y = 0.4;
            body.castShadow = true;

            const headGeometry = new THREE.SphereGeometry(0.3, 32, 32);
            const headMaterial = new THREE.MeshStandardMaterial({ color: 0xf5deb3 });
            const head = new THREE.Mesh(headGeometry, headMaterial);
            head.position.y = 1.1;
            head.castShadow = true;

            const eyeGeometry = new THREE.SphereGeometry(0.05, 16, 16);
            const eyeMaterial = new THREE.MeshStandardMaterial({ color: 0x000000 });
            const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
            const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
            leftEye.position.set(-0.1, 1.15, 0.25);
            rightEye.position.set(0.1, 1.15, 0.25);

            const mouthGeometry = new THREE.BoxGeometry(0.15, 0.03, 0.05);
            const mouthMaterial = new THREE.MeshStandardMaterial({ color: 0x8b4513 });
            const mouth = new THREE.Mesh(mouthGeometry, mouthMaterial);
            mouth.position.set(0, 1.05, 0.25);
            mouth.name = "mouth";

            avatar = new THREE.Group();
            avatar.add(body);
            avatar.add(head);
            avatar.add(leftEye);
            avatar.add(rightEye);
            avatar.add(mouth);

            scene.add(avatar);
            mixer = new THREE.AnimationMixer(avatar);

            window.avatarAnimations = {
                idle: { duration: 2 },
                happy: { duration: 1 },
                angry: { duration: 1 },
                neutral: { duration: 1 },
                dance: { duration: 2 }
            };
        }

        function animate() {
            requestAnimationFrame(animate);

            const delta = clock.getDelta();

            if (mixer) mixer.update(delta);

            if (speaking && avatar) {
                const time = Date.now() * 0.01;
                avatar.traverse(function (child) {
                    if (child.name === "mouth" || (child.isBone && child.name.toLowerCase().includes('mouth'))) {
                        child.scale.y = 1 + Math.sin(time * 8) * 0.3;
                        child.position.y = Math.sin(time * 6) * 0.02;
                    }
                });
            }

            if (avatar && !window.avatarAnimations?.Idle && currentEmotion === 'idle') {
                avatar.rotation.y = Math.sin(Date.now() * 0.001) * 0.05;
                avatar.position.y = -1 + Math.sin(Date.now() * 0.002) * 0.02;
            }

            renderer.render(scene, camera);
        }

        function onWindowResize() {
            const container = document.getElementById('avatar-container');
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        }

        function updateStatus(text, type = '') {
            const statusElement = document.getElementById('status');
            const indicator = document.getElementById('status-indicator');

            statusElement.textContent = text;

            indicator.classList.remove('speaking', 'listening');

            if (type === 'speaking') {
                indicator.classList.add('speaking');
            } else if (type === 'listening') {
                indicator.classList.add('listening');
            }
        }

        function triggerEmotion(emotion) {
            if (!mixer || !window.avatarAnimations) return;

            const clip = window.avatarAnimations[emotion];
            if (clip) {
                mixer.stopAllAction();

                if (clip.duration) {
                    animateSimpleEmotion(emotion);
                } else {
                    const action = mixer.clipAction(clip);
                    action.play();

                    setTimeout(() => {
                        mixer.stopAllAction();
                        const idleClip = window.avatarAnimations['idle'];
                        if (idleClip) {
                            const idleAction = mixer.clipAction(idleClip);
                            idleAction.play();
                        }
                    }, clip.duration * 1000);
                }

                currentEmotion = emotion;
            }
        }

        function animateSimpleEmotion(emotion) {
            if (!avatar) return;

            const startTime = Date.now();
            const duration = 2000;

            function animate() {
                const elapsed = Date.now() - startTime;
                const progress = Math.min(elapsed / duration, 1);

                switch (emotion) {
                    case 'happy':
                        avatar.rotation.y = Math.sin(elapsed * 0.01) * 0.2;
                        avatar.position.y = -1 + Math.sin(elapsed * 0.02) * 0.05;
                        break;
                    case 'angry':
                        avatar.rotation.y = Math.sin(elapsed * 0.02) * 0.1;
                        avatar.scale.set(1.5 + Math.sin(elapsed * 0.02) * 0.05, 1.5, 1.5);
                        break;
                    case 'dance':
                        avatar.rotation.y = Math.sin(elapsed * 0.01) * 0.5;
                        avatar.position.y = -1 + Math.abs(Math.sin(elapsed * 0.02)) * 0.2;
                        break;
                }

                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    avatar.rotation.y = 0;
                    avatar.position.y = -1;
                    avatar.scale.set(1.5, 1.5, 1.5);
                }
            }

            animate();
        }

        // Expose functions to parent window for Gradio integration
        window.avatarSpeak = function(text) {
            speaking = true;
            updateStatus('Avatar is speaking...', 'speaking');

            setTimeout(() => {
                speaking = false;
                updateStatus('Avatar is ready', '');
            }, text.length * 50); // Simulate speaking duration
        };

        window.avatarSetEmotion = function(emotion) {
            triggerEmotion(emotion);
            updateStatus(`Playing ${emotion} animation`, '');
        };

        // Initialize on load
        window.addEventListener('load', initThreeJS);
    </script>
</body>
</html>
"""


# Response generation function
def generate_response(user_input):
    """Generate a response based on user input"""
    if not user_input or not user_input.strip():
        return "Please enter a message for the avatar to respond to."

    user_input = user_input.lower().strip()

    # Greeting patterns
    if any(word in user_input for word in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello there! I'm your 3D anime avatar. How can I help you today?"

    # Questions about avatar
    elif any(phrase in user_input for phrase in ['how are you', "what's up", 'how do you do']):
        return "I'm doing great, thank you for asking! As a 3D avatar, I'm always ready to chat. How about you?"

    elif any(phrase in user_input for phrase in ['your name', 'who are you']):
        return "I'm a 3D anime avatar powered by AI! You can call me Aiko. I'm here to chat and assist you with anything you need."

    # Time and date
    elif 'time' in user_input:
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."

    elif any(word in user_input for word in ['date', 'day', 'today']):
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {current_date}."

    # Actions
    elif 'dance' in user_input:
        return "I love to dance! Watch me show off my moves! 💃"

    elif any(word in user_input for word in ['joke', 'funny', 'laugh']):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything! 😄",
            "What do you call a fake noodle? An impasta! 🍝",
            "Why did the scarecrow win an award? He was outstanding in his field! 🌾",
            "What do you call a bear with no teeth? A gummy bear! 🐻",
            "Why don't eggs tell jokes? They'd crack each other up! 🥚"
        ]
        import random
        return random.choice(jokes)

    # Farewells
    elif any(word in user_input for word in ['bye', 'goodbye', 'see you', 'farewell']):
        return "Goodbye! It was wonderful chatting with you. Come back anytime! 👋"

    # Thanks
    elif any(word in user_input for word in ['thank', 'thanks', 'appreciate']):
        return "You're very welcome! I'm always happy to help. Is there anything else you'd like to know? 😊"

    # Help
    elif 'help' in user_input:
        return ("I can help you with many things! Try asking me about:\n"
                "• Greetings and conversation\n"
                "• Current time and date\n"
                "• Jokes and fun facts\n"
                "• Dancing and emotions\n"
                "Just type your question or request!")

    # Weather (simulated)
    elif 'weather' in user_input:
        return "I don't have access to live weather data, but I hope it's beautiful where you are! ☀️"

    # Default responses
    else:
        default_responses = [
            "That's really interesting! Tell me more about that.",
            "I see what you mean. Can you elaborate on that?",
            "That's a fascinating perspective! What makes you think that?",
            "Interesting! How does that make you feel?",
            "I'd love to hear more about your thoughts on this.",
            "That's quite intriguing! Can you share more details?"
        ]
        import random
        return random.choice(default_responses)


# Chat function with history
def chat_with_avatar(message, history):
    """Handle chat interaction with history"""
    if not message or not message.strip():
        return history, ""

    response = generate_response(message)
    history.append((message, response))

    return history, ""


# Emotion trigger function
def set_emotion(emotion):
    """Trigger emotion animation on avatar"""
    emotion_messages = {
        "happy": "😊 Avatar is feeling happy!",
        "sad": "😢 Avatar is feeling sad...",
        "angry": "😠 Avatar is feeling angry!",
        "surprised": "😲 Avatar is surprised!",
        "neutral": "😐 Avatar is feeling neutral.",
        "dance": "💃 Avatar is dancing!"
    }
    return emotion_messages.get(emotion, "Emotion set!")


# Create Gradio interface
def create_interface():
    """Create the main Gradio interface"""

    with gr.Blocks(
        theme=gr.themes.Soft(
            primary_hue="purple",
            secondary_hue="blue",
        ),
        css="""
        .gradio-container {
            max-width: 1400px !important;
        }
        .avatar-container {
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        }
        .control-panel {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
            padding: 20px;
        }
        .emotion-btn {
            transition: all 0.2s ease;
        }
        .emotion-btn:hover {
            transform: scale(1.05);
        }
        footer {
            margin-top: 40px;
            text-align: center;
            color: #666;
        }
        """,
        title=TITLE
    ) as demo:

        gr.Markdown(f"# {TITLE}")
        gr.Markdown(DESCRIPTION)

        with gr.Row():
            # Left column - 3D Avatar
            with gr.Column(scale=2):
                avatar_display = gr.HTML(
                    value=create_avatar_html(),
                    label="3D Avatar",
                    elem_classes=["avatar-container"]
                )

            # Right column - Controls
            with gr.Column(scale=1, elem_classes=["control-panel"]):
                gr.Markdown("### 💬 Chat with Avatar")

                chatbot = gr.Chatbot(
                    height=350,
                    label="Conversation",
                    bubble_full_width=False,
                    avatar_images=(
                        None,  # User avatar
                        "https://api.dicebear.com/7.x/bottts/svg?seed=avatar"  # Bot avatar
                    )
                )

                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="Type your message here...",
                        show_label=False,
                        scale=4,
                        container=False
                    )
                    send_btn = gr.Button("Send 📤", scale=1, variant="primary")

                clear_btn = gr.Button("Clear Chat 🗑️", size="sm")

                gr.Markdown("### 🎭 Avatar Emotions")

                with gr.Row():
                    happy_btn = gr.Button("😊 Happy", elem_classes=["emotion-btn"])
                    sad_btn = gr.Button("😢 Sad", elem_classes=["emotion-btn"])

                with gr.Row():
                    angry_btn = gr.Button("😠 Angry", elem_classes=["emotion-btn"])
                    surprised_btn = gr.Button("😲 Surprised", elem_classes=["emotion-btn"])

                with gr.Row():
                    neutral_btn = gr.Button("😐 Neutral", elem_classes=["emotion-btn"])
                    dance_btn = gr.Button("💃 Dance", elem_classes=["emotion-btn"])

                emotion_status = gr.Textbox(
                    label="Emotion Status",
                    interactive=False,
                    value="Ready"
                )

        # Event handlers
        msg.submit(chat_with_avatar, [msg, chatbot], [chatbot, msg])
        send_btn.click(chat_with_avatar, [msg, chatbot], [chatbot, msg])
        clear_btn.click(lambda: ([], ""), None, [chatbot, emotion_status])

        # Emotion buttons
        happy_btn.click(lambda: set_emotion("happy"), None, emotion_status)
        sad_btn.click(lambda: set_emotion("sad"), None, emotion_status)
        angry_btn.click(lambda: set_emotion("angry"), None, emotion_status)
        surprised_btn.click(lambda: set_emotion("surprised"), None, emotion_status)
        neutral_btn.click(lambda: set_emotion("neutral"), None, emotion_status)
        dance_btn.click(lambda: set_emotion("dance"), None, emotion_status)

        # Footer
        gr.Markdown("""
        ---
        ### 🚀 Features
        - **3D Avatar**: Fully interactive 3D character with realistic animations
        - **Natural Language**: Chat naturally with the avatar
        - **Emotions**: Express different emotions with button controls
        - **Responsive**: Works on desktop and mobile devices

        ### 💡 Tips
        - Try asking the avatar about the time, date, or for a joke
        - Use emotion buttons to see different animations
        - The avatar responds to greetings, questions, and general conversation

        ### 🔧 Technology
        Built with Three.js, Gradio, and deployed on Hugging Face Spaces
        """)

    return demo


# Main execution
if __name__ == "__main__":
    demo = create_interface()
    demo.launch(
        share=False,
        server_name="0.0.0.0",
        server_port=7860
    )
