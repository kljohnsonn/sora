# Sora: An Interactive Discord Bot

Sora is a Discord bot that integrates with the Open Router API to facilitate conversation in Discord servers. It's designed to provide users with a more interactive chat experience by using AI models for response generation. Sora allows users to engage in conversations, manage contexts, and choose from various models to customize their interactions.

## Features

- **AI-Powered Chat Responses:** Utilizes the Open Router API for generating chat responses based on the ongoing conversation context.
- **Model Customization:** Offers users the ability to select their preferred AI model for response generation.
- **Conversation Context Management:** Keeps track of conversation history for each user to maintain a coherent dialogue.
- **Configurable Interaction:** Can be set to respond in all channels or restricted to specific channels within a server.

![Sora in Action](/images/showcase.png)

## Getting Started

### Prerequisites

- Python 3.8+
- A Discord Bot Token ([Creating a Discord Bot](https://discordpy.readthedocs.io/en/latest/discord.html))
- An Open Router API Key

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/mintsuku/sora.git
   cd sora
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Configure your environment variables:
   - `DISCORD_TOKEN`: Your Discord Bot Token.
   - `API_KEY`: Your Open Router API Key.

4. Start the bot:
   ```sh
   python main.py
   ```

![Bot Startup](/images/startup.png)

## Usage

After launching Sora on your server, you can use the following commands:

- `/set_channel <channel_id|all>`: Configure the bot to respond in a specific channel or all channels.
- `/list_models`: Displays a list of available AI models.
- `/set_model <model_id>`: Selects a specific AI model for generating responses.
- `/clear_context`: Clears the current conversation context to start afresh.

## To-Do

- [ ] Develop a dashboard for detailed analytics on bot interaction and usage patterns.
- [ ] Create a setup wizard for easier bot configuration and deployment.
- [ ] Allow server admins to create custom commands without needing to code, making the bot more customizable for individual server needs.
- [ ] Add voice command capabilities or allow the bot to participate in voice channels, providing responses or playing audio content based on user interactions.

## Contributing

Contributions are welcome! If you have suggestions or improvements, please follow these steps:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

## Disclaimer

This project was initially created for personal enjoyment and to address specific issues I encountered, tailored to my own convenience. It's shared in its current form, without guarantees. Originally, I hadn't planned on a public release, so it might not be the pinnacle of user-friendliness. However, I'm actively working to improve its accessibility and ease of use!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.