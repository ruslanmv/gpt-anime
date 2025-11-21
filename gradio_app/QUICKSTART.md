# ⚡ Quick Start Guide

Get your 3D Anime Chatbot running in 5 minutes!

## 🎯 For the Impatient

### Option 1: Hugging Face Spaces (No Installation)

Just visit the live demo:
👉 **[https://huggingface.co/spaces/YOUR_USERNAME/3d-anime-chatbot](#)**

That's it! Start chatting immediately! 🎉

---

### Option 2: Local Setup (5 Minutes)

#### Step 1: Clone the Repository

```bash
git clone https://github.com/ruslanmv/gpt-anime.git
cd gpt-anime/gradio_app
```

#### Step 2: Run Setup Script

**Linux/Mac:**
```bash
bash setup.sh
```

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### Step 3: Launch the App

```bash
python app.py
```

#### Step 4: Open Your Browser

Visit: **http://localhost:7860**

**Done! 🎊**

---

### Option 3: Docker (One Command)

```bash
docker-compose up
```

Then visit: **http://localhost:7860**

---

## 🎮 First Steps

### 1. Say Hello!

Type in the chat box:
```
Hello!
```

Watch the 3D avatar respond! 👋

### 2. Try Different Commands

```
What time is it?
Tell me a joke
Can you dance?
Who are you?
```

### 3. Play with Emotions

Click the emotion buttons to see the avatar react:
- 😊 Happy
- 😢 Sad
- 😠 Angry
- 😲 Surprised
- 💃 Dance

### 4. Interact with the 3D Model

- **Rotate**: Click and drag
- **Zoom**: Scroll wheel
- **Pan**: Right-click and drag (desktop)

---

## 🎨 Customization Quick Tips

### Change Avatar Response

Edit `app.py`, find `generate_response()` function:

```python
def generate_response(user_input):
    if 'your keyword' in user_input:
        return "Your custom response!"
    # ... rest of code
```

### Change Avatar Model

In `app.py`, find the `loadAvatar()` section:

```javascript
loader.load(
    'YOUR_MODEL_URL.glb',  // Change this URL
    function (gltf) {
        // ...
    }
);
```

### Change Colors/Theme

Modify the CSS in `create_avatar_html()` function:

```css
background: linear-gradient(135deg, #YOUR_COLOR_1, #YOUR_COLOR_2);
```

---

## 🚨 Troubleshooting

### Issue: Port 7860 already in use

**Solution:** Change the port in `app.py`:
```python
demo.launch(server_port=7861)  # Use a different port
```

### Issue: Module not found

**Solution:** Reinstall requirements:
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: Avatar not loading

**Solution:**
1. Check internet connection (model loads from CDN)
2. Wait 30 seconds for initial load
3. Refresh the page

### Issue: Can't see 3D model

**Solution:**
- Use a modern browser (Chrome, Firefox, Edge)
- Enable WebGL in browser settings
- Update your graphics drivers

---

## 📱 Mobile Usage

The chatbot works on mobile devices!

1. Open your mobile browser
2. Visit the URL (Hugging Face or your local IP)
3. Tap to interact with the 3D model
4. Use pinch-to-zoom gesture

---

## 🔥 Advanced Quick Starts

### Add Voice Input (Coming Soon)

```python
# In app.py
with gr.Row():
    audio_input = gr.Audio(source="microphone", type="numpy")
```

### Connect to ChatGPT

```python
import openai

def generate_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )
    return response.choices[0].message.content
```

### Add Authentication

```python
demo.launch(
    auth=("username", "password"),
    auth_message="Enter credentials to access the chatbot"
)
```

---

## 📊 Performance Tips

### Faster Loading

1. **Use local 3D models:**
   - Download the GLB file
   - Place in `static/models/` folder
   - Update path in code

2. **Enable caching:**
   ```python
   demo.launch(enable_queue=True)
   ```

3. **Reduce model quality:**
   - Use compressed textures
   - Lower polygon count models

---

## 🎓 Learning Path

New to the project? Follow this path:

1. ✅ **Run the app** (you're here!)
2. 📖 Read [README.md](README.md) for features
3. 🔧 Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment
4. 🤝 See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
5. 💡 Explore the code in `app.py`

---

## 🆘 Need Help?

- 📖 **Full Documentation**: [README.md](README.md)
- 🐛 **Report Issues**: [GitHub Issues](https://github.com/ruslanmv/gpt-anime/issues)
- 💬 **Ask Questions**: [GitHub Discussions](https://github.com/ruslanmv/gpt-anime/discussions)
- 📧 **Email**: support@gpt-anime.com

---

## 🎉 What's Next?

Now that you're up and running:

- ⭐ Star the repository on GitHub
- 🐦 Share on social media
- 🤝 Contribute improvements
- 🚀 Deploy to production

---

## 💡 Quick Tips

| Tip | Description |
|-----|-------------|
| **Ctrl+C** | Stop the local server |
| **F5** | Refresh to see code changes |
| **Ctrl+Shift+I** | Open browser DevTools for debugging |
| **Check Console** | View JavaScript errors in browser console |

---

## 🌟 Example Use Cases

### Customer Service
Set up as a virtual assistant on your website

### Education
Use as an interactive tutor for students

### Entertainment
Create a fun chatbot for your community

### Prototyping
Test 3D avatar interactions for your app

---

**Ready to chat? Let's go! 🚀**

[⬆ Back to Top](#-quick-start-guide)
