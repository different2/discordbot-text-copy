import discord
from discord.ext import commands

# Set up bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Bot is in {len(bot.guilds)} servers")
    print("Bot is ready and listening for reactions!")

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Check if the message has any embeds
    if message.embeds:
        try:
            # Add the printer reaction to any embed message
            await message.add_reaction("🖨️")
            print(f"Added printer reaction to embed message")
        except Exception as e:
            print(f"Error adding reaction: {e}")
    
    # Process commands (if you have any)
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    print(f"Reaction detected: {reaction.emoji} by {user.name}")
    
    # Ignore the bot's own reactions
    if user == bot.user:
        print("Ignoring bot's own reaction")
        return
    
    # Only respond to printer reaction
    if str(reaction.emoji) != "🖨️":
        print(f"Reaction {reaction.emoji} is not the printer emoji")
        return
    
    # Check if the message has embeds
    if reaction.message.embeds:
        print(f"Message has {len(reaction.message.embeds)} embeds")
        
        try:
            # Extract all text content from ALL embeds
            all_embed_text = []
            
            for embed_index, embed in enumerate(reaction.message.embeds):
                embed_text = []
                
                # Add embed separator if there are multiple embeds
                if len(reaction.message.embeds) > 1:
                    embed_text.append(f"=== EMBED {embed_index + 1} ===")
                
                # Add title if it exists
                if embed.title:
                    embed_text.append(f"**{embed.title}**")
                
                # Add author if it exists
                if embed.author and embed.author.name:
                    embed_text.append(f"Author: {embed.author.name}")
                
                # Add description if it exists
                if embed.description:
                    embed_text.append(embed.description)
                
                # Add fields if they exist
                if embed.fields:
                    for field in embed.fields:
                        if field.name and field.value:
                            embed_text.append(f"**{field.name}**\n{field.value}")
                
                # Add footer if it exists
                if embed.footer and embed.footer.text:
                    embed_text.append(f"Footer: {embed.footer.text}")
                
                # Add URL if it exists
                if embed.url:
                    embed_text.append(f"URL: {embed.url}")
                
                # Add this embed's text to the collection
                if embed_text:
                    all_embed_text.extend(embed_text)
            
            if all_embed_text:
                # Join all text with double newlines for readability
                full_text = "\n\n".join(all_embed_text)
                
                # Split into chunks if the message is too long (Discord has a 2000 character limit)
                max_length = 1900  # Leave some room for the "Copied embed text:" prefix
                
                if len(full_text) <= max_length:
                    await reaction.message.channel.send(f"Copied embed text:\n```\n{full_text}\n```")
                else:
                    # Split into multiple messages
                    chunks = [full_text[i:i+max_length] for i in range(0, len(full_text), max_length)]
                    for i, chunk in enumerate(chunks):
                        if i == 0:
                            await reaction.message.channel.send(f"Copied embed text (part {i+1}/{len(chunks)}):\n```\n{chunk}\n```")
                        else:
                            await reaction.message.channel.send(f"Part {i+1}/{len(chunks)}:\n```\n{chunk}\n```")
                
                print(f"Sent text from {len(reaction.message.embeds)} embeds successfully")
            else:
                await reaction.message.channel.send("No text content found in any embeds.")
                print("No text content found in any embeds")
                
        except Exception as e:
            print(f"Error processing embeds: {e}")
            await reaction.message.channel.send("Error processing the embed text.")
    else:
        print("Message has no embeds")

# Use environment variable or config file for token instead of hardcoding
# bot.run('YOUR_BOT_TOKEN_HERE')
bot.run('MTM4MzMzMjY5NDkyMjEwNDgzMg.GuHD5F.VM_kbwztNE4jAbS7HmXlmvIQmiac9FEEEPYnTg')