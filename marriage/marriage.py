import discord
import asyncio
import random
import datetime
import typing

from redbot.core import Config, checks, commands
from redbot.core.utils.chat_formatting import humanize_list, box
from redbot.core.utils.predicates import MessagePredicate

class Marriage(commands.Cog):
    """
    Marriage cog with some extra stuff.
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234580008135, force_registration=True)

        self.config.register_guild(
            multi=False
        )

        self.config.register_member(
            married = False,
            divorced = False,
            parent = False,
            child = False,
            current = [],
            children = [],
            parents = [],
            exes = [],
            about = "I'm mysterious.",
            marcount = 0,
            dircount = 0,
            kidcount = 0,
            parcount = 0
        )
            
    @commands.group(autohelp=True)
    @commands.guild_only()
    @checks.admin()
    async def marriage(self, ctx: commands.Context):
        f"""Various Marriage settings."""

    @marriage.command(name="set")
    async def marriage_set(self, ctx: commands.Context, member: typing.Optional[discord.Member], var, state: bool):
        """Set member variables for a user."""
        if var == "married":
            await self.config.member(member).married.set(state)
            await ctx.send(f"Set {member.mention}'s status to {'married!' if state else 'unmarried!'}")
        if var == "divorced":
            await self.config.member(member).divorced.set(state)
            await ctx.send(f"Set {member.mention}'s status to {'divorced!' if state else 'undivorced!'}")
        
    @marriage.command(name="multiple")
    async def marriage_multiple(self, ctx: commands.Context, state: bool):
        """Enable/disable whether members can be married to multiple people at once."""
        await self.config.guild(ctx.guild).multi.set(state)
        await ctx.send(f"Members {'can' if state else 'cannot'} marry multiple people.")

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def about(
        self, ctx: commands.Context, member: typing.Optional[discord.Member]
    ):
        """Display your or someone else's about"""
        if not member:
            member = ctx.author
        is_married = await self.config.member(member).married()
        is_parent = await self.config.member(member).parent()
        kids_header = ""
        kids_text = ""
        spouse_header = ""
        spouse_text = ""
        if not is_married:
            if await self.config.member(member).parent():
                if await self.config.member(member).divorced():
                    rs_status = "Widow"
                else:
                    rs_status = "Single Parent"
            elif await self.config.member(member).divorced(): 
                rs_status = "Divorced"
            else:
                rs_status = "Single" 
        else:
            if await self.config.member(member).parent():
                async with self.config.member(ctx.author).children() as children:
                    if children != []:
                        for child in children:
                            async with self.config.member(child).children() as grandchildren:
                                if grandchildren != []:
                                    for grandchild in grandchildren:
                                        async with self.config.member(grandchild).children() as greatgrandchildren:
                                            if grandchild != []:
                                                rs_status = "Old Fuck"
                                            else:
                                                rs_status = "Great-Grandparent"
                                else:
                                    rs_status = "Grandparent"
                    else:
                        rs_status = "Parent"
            else:
                rs_status = "Married"
                
            spouse_ids = await self.config.member(member).current()
            spouses = []
            
            for spouse_id in spouse_ids:
                spouse = self.bot.get_user(spouse_id)
                if spouse:
                    spouses.append(spouse.name)
            if spouses == []:
                spouse_header = "Spouse:"
                spouse_text = "None"
            else:
                spouse_text = humanize_list(spouses)
                spouse_header = "Spouse:" if len(spouses) == 1 else "Spouses:"
                
            children_ids = await self.config.member(member).children()
            kids = []
            
            for children_id in children_ids:
                kid = self.bot.get_user(children_id)
                if kid:
                    kids.append(kid.name)
            if kids == []:
                kids_header = "Children:"
                kids_text = "None"
            else:
                kids_text = humanize_list(kids)
                kids_header = "Child:" if len(kids) == 1 else "Children:"
        marcount = await self.config.member(member).marcount()
        been_married = f"{marcount} time" if marcount == 1 else f"{marcount} times"
        if marcount != 0:
            exes_ids = await self.config.member(member).exes()
            if exes_ids == []:
                ex_text = "None"
            else:
                exes = list()
                for ex_id in exes_ids:
                    ex = self.bot.get_user(ex_id)
                    if not ex:
                        continue
                    ex = ex.name
                    exes.append(ex)
                ex_text = "None" if exes == [] else humanize_list(exes)
        e = discord.Embed(colour=member.color)
        e.set_author(name=f"{member.name}'s Profile", icon_url=member.avatar_url)
        e.set_footer(text=f"{member.name}#{member.discriminator} ({member.id})")
        e.set_thumbnail(url=member.avatar_url)
        e.add_field(name="About:", value=await self.config.member(member).about(), inline=False)
        e.add_field(name="Status:", value=rs_status)
        if is_married:
            e.add_field(name=spouse_header, value=spouse_text)
        if is_parent:
            e.add_field(name=kids_header, value=kids_text)
        e.add_field(name="Been married:", value=been_married)
        if await self.config.member(member).marcount() != 0:
            e.add_field(name="Ex spouses:", value=ex_text)

        await ctx.send(embed=e)

    @commands.guild_only()
    @commands.command()
    async def exes(
        self, ctx: commands.Context, member: typing.Optional[discord.Member]
    ):
        """Display your or someone else's exes."""
        if not member:
            member = ctx.author
        exes_ids = await self.config.member(member).exes()
        exes = list()
        for ex_id in exes_ids:
            ex = self.bot.get_user(ex_id)
            if ex:
                exes.append(ex.name)
        ex_text = "None" if exes == [] else humanize_list(exes)
        await ctx.send(f"{member.mention}'s exes are: {ex_text}")

    @commands.guild_only()
    @commands.command()
    async def spouses(
        self, ctx: commands.Context, member: typing.Optional[discord.Member]
    ):
        if not member:
            member = ctx.author
        spouses_ids = await self.config.member(member).current()
        sp_text = ""
        for s_id in spouses_ids:
            spouse = self.bot.get_user(s_id)
            if spouse:
                sp_text += f"{spouse.name}\n"
        if sp_text == "":
            sp_text = "None"
        await ctx.send(
            box(
                f"""= {member.name}'s spouses = {sp_text.strip()}""",
                lang="asciidoc",
            )
        )

    @commands.max_concurrency(1, commands.BucketType.channel, wait=True)
    @commands.guild_only()
    @commands.command()
    async def marry(self, ctx: commands.Context, member: discord.Member):
        """Marry the love of your life!"""
        if member.id == ctx.author.id:
            return await ctx.send("You cannot marry yourself!")
        if member.id in await self.config.member(ctx.author).current():
            return await ctx.send("You two are already married!")
        if not await self.config.guild(ctx.guild).multi():
            if await self.config.member(ctx.author).married():
                return await ctx.send("You're already married!")
            if await self.config.member(member).married():
                return await ctx.send("They're already married!")
        await ctx.send(
            f"{ctx.author.mention} has asked {member.mention} to marry them!\n"
            f"{member.mention}, what do you say?"
        )
        pred = MessagePredicate.yes_or_no(ctx, ctx.channel, member)
        try:
            await self.bot.wait_for("message", timeout=120, check=pred)
        except asyncio.TimeoutError:
            return await ctx.send("Oh no... I was looking forward to the cerenomy...")
        if not pred.result:
            return await ctx.send("Oh no... I was looking forward to the cerenomy...")
        author_marcount = await self.config.member(ctx.author).marcount()
        target_marcount = await self.config.member(member).marcount()

        await self.config.member(ctx.author).marcount.set(author_marcount + 1)
        await self.config.member(member).marcount.set(target_marcount + 1)

        await self.config.member(ctx.author).married.set(True)
        await self.config.member(member).married.set(True)

        await self.config.member(ctx.author).divorced.clear()
        await self.config.member(member).divorced.clear()

        async with self.config.member(ctx.author).current() as acurrent:
            acurrent.append(member.id)
        async with self.config.member(member).current() as tcurrent:
            tcurrent.append(ctx.author.id)
        await ctx.send(f":church: {ctx.author.mention} and {member.mention} are now a happy married couple! ")

    @commands.max_concurrency(1, commands.BucketType.channel, wait=True)
    @commands.guild_only()
    @commands.command()
    async def divorce(
        self, ctx: commands.Context, member: discord.Member
    ):
        """Divorce your current spouse"""
        if member.id == ctx.author.id:
            return await ctx.send("You cannot divorce yourself!")
        if member.id not in await self.config.member(ctx.author).current():
            return await ctx.send("You two aren't married!")
        await ctx.send(
            f"{ctx.author.mention} wants to divorce you, {member.mention}, do you accept?\n"
        )
        pred = MessagePredicate.yes_or_no(ctx, ctx.channel, member)
        await self.bot.wait_for("message", check=pred)
        if not pred.result:
            await ctx.send(f"Too bad! Proceeding with divorce...\n")
        async with self.config.member(ctx.author).current() as acurrent:
            acurrent.remove(member.id)
        async with self.config.member(member).current() as tcurrent:
            tcurrent.remove(ctx.author.id)
        async with self.config.member(ctx.author).exes() as aexes:
            aexes.append(member.id)
        async with self.config.member(member).exes() as texes:
            texes.append(ctx.author.id)
        if len(await self.config.member(ctx.author).current()) == 0:
            await self.config.member(ctx.author).married.clear()
            await self.config.member(ctx.author).divorced.set(True)
        if len(await self.config.member(member).current()) == 0:
            await self.config.member(member).married.clear()
            await self.config.member(member).divorced.set(True)
        await ctx.send(
            f":broken_heart: {ctx.author.mention} and {member.mention} got divorced...\n"
        )
        
    @commands.max_concurrency(1, commands.BucketType.channel, wait=True)
    @commands.guild_only()
    @commands.command()
    async def adopt(self, ctx: commands.Context, member: discord.Member):
        """Adopt a vegan!"""
        if member.id == ctx.author.id:
            return await ctx.send("You cannot adopt yourself!")
        if member.id in await self.config.member(ctx.author).parents():
            return await ctx.send("You cannot adopt your own parent!")
        if member.id in await self.config.member(ctx.author).current():
            return await ctx.send("You cannot adopt your own spouse!")
        if member.id in await self.config.member(ctx.author).children():
            return await ctx.send("You've already adopted them!")
        if await self.config.member(member).parents():
            return await ctx.send("They're already adopted!")
        await ctx.send(
            f"{ctx.author.mention} has asked to adopt {member.mention}!\n"
            f"{member.mention}, what do you say?"
        )
        pred = MessagePredicate.yes_or_no(ctx, ctx.channel, member)
        try:
            await self.bot.wait_for("message", timeout=120, check=pred)
        except asyncio.TimeoutError:
            return await ctx.send("Oh no... hopefully they'll find a good home soon...")
        if not pred.result:
            return await ctx.send("Oh no... hopefully they'll find a good home soon...")
            
        author_kidcount = await self.config.member(ctx.author).kidcount()
        target_parcount = await self.config.member(member).parcount()

        await self.config.member(ctx.author).kidcount.set(author_kidcount + 1)
        await self.config.member(member).parcount.set(target_parcount + len(await self.config.member(ctx.author).current()))

        await self.config.member(ctx.author).parent.set(True)
        await self.config.member(member).child.set(True)

        # add CHILD to PARENT'S children
        async with self.config.member(ctx.author).children() as children:
            children.append(member.id)
            
        # add PARENT to CHILD'S parents
        async with self.config.member(member).parents() as parents:
            parents.append(ctx.author.id)
            
        # add CHILD to PARENT'S SPOUSE(S) children
        async with self.config.member(ctx.author).current() as spouses:
            for x in spouses:
                async with self.config.member(self.bot.get_user(x)).children() as children:
                    children.append(member.id)
                    await self.config.member(self.bot.get_user(x)).parent.set(True)
        
        # add PARENT'S SPOUSE(S) to CHILD'S parents 
        async with self.config.member(member).parent() as parents:
            async with self.config.member(ctx.author).current() as spouses:
                for x in spouses:
                    async with self.config.member(self.bot.get_user(x)).children() as children:
                        children.append(member.id)
        await ctx.send(f":classical_building: {ctx.author.mention} has adopted {member.mention}! ")