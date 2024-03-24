from discord import ui
import discord

class ModelListView(ui.View):
    def __init__(self, model_chunks, update_embed, embed):
        super().__init__()
        self.model_chunks = model_chunks
        self.current_page = 0
        self.update_embed = update_embed
        self.embed = embed

    @ui.button(label="Previous", style=discord.ButtonStyle.blurple)
    async def previous_page(self, interaction: discord.Interaction, button: ui.Button):
        self.current_page = max(0, self.current_page - 1)
        self.update_embed(self.current_page)
        await interaction.response.edit_message(embed=self.embed, view=self)

    @ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def next_page(self, interaction: discord.Interaction, button: ui.Button):
        self.current_page = min(len(self.model_chunks) - 1, self.current_page + 1)
        self.update_embed(self.current_page)
        await interaction.response.edit_message(embed=self.embed, view=self)