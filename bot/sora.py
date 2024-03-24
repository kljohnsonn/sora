import discord
from discord.ext import commands
import shutil
from api.context_manager import ContextManager
from api.openrouter import OpenRouterAPI
from bot.ui import ModelListView

class Sora:
    def __init__(self, token, api_key):
        self.bot = commands.Bot(intents=discord.Intents.all(), command_prefix="")
        self.api = OpenRouterAPI(api_key)
        self.context_manager = ContextManager()
        self.token = token
        self.channel_id = None
        self.allow_user_model_selection = False
        self.default_model = "teknium/openhermes-2.5-mistral-7b"
        self.setup()

    def setup(self):
        @self.bot.event
        async def on_ready():
            terminal_width = shutil.get_terminal_size().columns  # Get the width of the terminal

            # Calculate the padding needed to center the message
            padding = (terminal_width - 60) // 2

            print("\n" + " " * padding + "\033[94m╔══════════════════════════════════════════════════════╗\033[0m")
            print(" " * padding + "\033[94m║\033[0m                                                      \033[94m║\033[0m")
            print(" " * padding + "\033[94m║\033[0m                   \033[1m\033[96mSora Bot\033[0m                       \033[94m║\033[0m")
            print(" " * padding + "\033[94m║\033[0m                    \033[96m\033[0m                       \033[94m║\033[0m")
            print(" " * padding + "\033[94m╠══════════════════════════════════════════════════════╣\033[0m")
            print(" " * padding + "\033[94m║\033[0m                                                      \033[94m║\033[0m")
            print(" " * padding + f"\033[94m║\033[0m \033[1m\033[96mLogged in as:\033[0m \033[96mSora\033[0m                  \033[94m║\033[0m")
            print(" " * padding + f"\033[94m║\033[0m \033[1m\033[96mUser ID:\033[0m      \033[96m{self.bot.user.id}\033[0m                    \033[94m║\033[0m")
            print(" " * padding + "\033[94m║\033[0m                                                      \033[94m║\033[0m")
            print(" " * padding + "\033[94m╚══════════════════════════════════════════════════════╝\033[0m")
            print("\n")
            print(" " * padding + "\033[96m         Let's engage in delightful conversations! \033[0m\n")

            await self.bot.tree.sync()  # Sync slash commands

        @self.bot.tree.command(name="set_channel", description="Set the channel ID for the bot to respond to")
        async def set_channel(interaction: discord.Interaction, channel: str):
            if channel.lower() == "all":
                self.channel_id = None
                await interaction.response.send_message("Bot will now respond to messages in all channels.")
            else:
                try:
                    self.channel_id = int(channel)
                    await interaction.response.send_message(f"Bot will now respond to messages in channel ID: {self.channel_id}")
                except ValueError:
                    await interaction.response.send_message("Invalid channel ID. Please provide a valid channel ID or 'all'.")

        @self.bot.tree.command(name="list_models", description="Retrieve the list of available models")
        async def list_models(interaction: discord.Interaction):
            response = self.api.get_models()
            if response.status_code == 200:
                models = response.json()["data"]
                
                # Format the model list with custom styling
                model_list = []
                for model in models:
                    # Truncate the description if it exceeds 100 characters
                    description = model['description'][:100] + "..." if len(model['description']) > 100 else model['description']
                    
                    model_info = (
                        f"🤖 **{model['name']}**\n"
                        f"  ╰ *Model ID:* `{model['id']}`\n"
                    )
                    model_list.append(model_info)
                
                # Split the model list into chunks of 5 models per page
                chunk_size = 5
                model_chunks = [model_list[i:i+chunk_size] for i in range(0, len(model_list), chunk_size)]
                
                # Create the paginated embed
                embed = discord.Embed(
                    title="📚 Available Models",
                    description="Browse the list of available models using the buttons below.",
                    color=discord.Color.blue()
                )
                
                def update_embed(page):
                    embed.clear_fields()
                    embed.add_field(name="Models", value="\n".join(model_chunks[page]), inline=False)
                    embed.set_footer(text=f"Page {page + 1}/{len(model_chunks)}")
                
                update_embed(0)
                
                view = ModelListView(model_chunks, update_embed, embed)
                await interaction.response.send_message(embed=embed, view=view)
            else:
                await interaction.response.send_message("Failed to retrieve the list of models.")

        @self.bot.tree.command(name="set_model", description="Set the model to use")
        async def set_model(interaction: discord.Interaction, model_id: str):
            user_id = interaction.user.id
            if self.allow_user_model_selection or interaction.user.guild_permissions.administrator:
                self.context_manager.set_user_model(user_id, model_id)
                await interaction.response.send_message(f"Model set to: {model_id}")
            else:
                await interaction.response.send_message("You don't have permission to set the model.")
        
        @self.bot.tree.command(name="set_default_model", description="Set the default model for all users (admin only)")
        async def set_default_model(interaction: discord.Interaction, model_id: str):
            if interaction.user.guild_permissions.administrator:
                self.default_model = model_id
                await interaction.response.send_message(f"Default model set to: {model_id}")
            else:
                await interaction.response.send_message("You don't have permission to set the default model.")
        
        @self.bot.tree.command(name="toggle_user_model_selection", description="Toggle user model selection (admin only)")
        async def toggle_user_model_selection(interaction: discord.Interaction):
            if interaction.user.guild_permissions.administrator:
                self.allow_user_model_selection = not self.allow_user_model_selection
                status = "enabled" if self.allow_user_model_selection else "disabled"
                await interaction.response.send_message(f"User model selection {status}.")
            else:
                await interaction.response.send_message("You don't have permission to toggle user model selection.")
        
        @self.bot.tree.command(name="clear_context", description="Clear the conversation context")
        async def clear_context(interaction: discord.Interaction):
            user_id = interaction.user.id
            self.context_manager.clear_context(user_id)
            await interaction.response.send_message("Conversation context cleared.")

        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return

            if self.channel_id is not None and message.channel.id != self.channel_id:
                return

            user_id = message.author.id
            question = message.content

            messages = self.context_manager.get_context(user_id)
            messages.append({"role": "user", "content": question})

            user_model = self.context_manager.get_user_model(user_id)
            if not user_model:
                user_model = self.default_model

            response = self.api.chat_completion(messages, user_model)

            if response.status_code == 200:
                response_data = response.json()
                ai_response = response_data["choices"][0]["message"]["content"]

                # Update the context
                self.context_manager.update_context(user_id, question, ai_response)

                await message.reply(ai_response)  # Reply to the user's message
            else:
                await message.reply("An error occurred while processing your request.")

    def run(self):
        self.bot.run(self.token)