import discord


async def handle_dm_message(channel: discord.DMChannel, issue_channel: discord.TextChannel, answerer_role_id: int):
    await channel.send("Here is your list of options:", view=MenuView(issue_channel, answerer_role_id))
    await channel.send("If you are reporting a bug, or wish to discuss ban/unban status with the moderators, "
                       "please click the appropriate option. Otherwise, please open an issue.")
    return


class MenuView(discord.ui.View):
    def __init__(self, issue_channel: discord.TextChannel, role_id: int):
        super().__init__()
        self.issue_channel = issue_channel
        self.answer_role_id = role_id

    @discord.ui.button(label="Open Issue", style=discord.ButtonStyle.primary, emoji="📝")
    async def button_callback_open_issue(self, interaction, button: discord.Button):
        await interaction.response.send_modal(
            CreateThreadModal(title="Open Issue", channel=self.issue_channel, should_add_user=True, answer_role_id=self.answer_role_id))

    @discord.ui.button(label="Report Bug", style=discord.ButtonStyle.secondary, emoji="🐛")
    async def button_callback_report_bug(self, interaction, button: discord.Button):
        await interaction.response.send_modal(
            CreateThreadModal(title="Report Bug", channel=self.issue_channel, should_add_user=False, answer_role_id=self.answer_role_id))

    @discord.ui.button(label="Request Unban", style=discord.ButtonStyle.secondary, emoji="🔨")
    async def button_callback_opt2(self, interaction, button: discord.Button):
        await interaction.response.send_modal(
            CreateThreadModal(title="Request Unban", channel=self.issue_channel, should_add_user=True, answer_role_id=self.answer_role_id))


class CreateThreadModal(discord.ui.Modal):
    summary = discord.ui.TextInput(label='Short Description', placeholder="Summary", required=True)
    paragraph = discord.ui.TextInput(label='Long Description', style=discord.TextStyle.paragraph, required=False)

    def __init__(self, title, channel: discord.TextChannel, should_add_user: bool, answer_role_id: int):
        super().__init__(title=title)
        self.issue_channel = channel
        self.add_user = should_add_user
        self.answer_role_id = answer_role_id

    async def on_submit(self, interaction: discord.Interaction) -> None:
        short_desc = self.summary.value
        long_desc = self.paragraph.value

        thread = await self.issue_channel.create_thread(name=short_desc, message=None)
        if long_desc:
            await thread.send(long_desc)
        if self.add_user:
            await thread.add_user(interaction.user)

        # Add users with specific role
        role = self.issue_channel.guild.get_role(self.answer_role_id)
        if role:
            member_list = role.members
            for member in member_list:
                await thread.add_user(member)
        else:
            await thread.send("Could not find moderators to answer your request! Please notify the server "
                              "administrators about this bug.")

        await interaction.response.send_message("Thread has been successfully created.")
