services:
  - type: web
    name: customer-service-bot  # Ensure this name is correct (your bot's name)
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python bot.py"
    branch: main
    envVars:
      - key: TELEGRAM_API_TOKEN
        value: "your_telegram_bot_token"  # Replace with actual token
      - key: RENDER_URL
        value: "https://customer-service-bot.onrender.com"  # Your Render service URL
