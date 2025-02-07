import os
import asyncio
import nest_asyncio
import interactions as it
from interactions import Client, Button, ButtonStyle, SelectMenu, SelectOption, ActionRow
from interactions import CommandContext as CC
from interactions import ComponentContext as CPC

import time
import math

from db_helper import *
from evy_helper import *
from test_helper import *
import logging



nest_asyncio.apply()


event_log = {}
pager_reg = {}
g_pager_reg = {}
leag_reg = {}
add_reg = {}
delete_reg = {}
#global lock_state
#lock_state = True     


skill_afx = ["-melee",'-magic','-mining', '-smithing', '-woodcutting', '-crafting', '-fishing', '-cooking','-tailoring']
skills = ['melee','magic','mining', 'smithing', 'woodcutting', 'crafting', 'fishing', 'cooking','tailoring']




first_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="⏪", 
                custom_id="first_button", )               
backward_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="◀", 
                custom_id="backward_button", )
stop_b = Button(
                style=ButtonStyle.DANGER, 
                label="◼",
                custom_id="stop_button", )
forward_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="▶", 
                custom_id="forward_button", )
last_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="⏩", 
                custom_id="last_button", )
b_row = ActionRow(
                components=[
                            first_b,
	                        backward_b,
	                        stop_b,
	                        forward_b,
	                        last_b
                            ]
                )


g_first_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="⏪", 
                custom_id="g_first_button", )               
g_backward_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="◀", 
                custom_id="g_backward_button", )
g_stop_b = Button(
                style=ButtonStyle.DANGER, 
                label="◼",
                custom_id="g_stop_button", )
g_forward_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="▶", 
                custom_id="g_forward_button", )
g_last_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="⏩", 
                custom_id="g_last_button", )
g_b_row = ActionRow(
                components=[
                            g_first_b,
	                        g_backward_b,
	                        g_stop_b,
	                        g_forward_b,
	                        g_last_b
                            ]
                )


add_row = ActionRow(
                components=[
                            Button(
                                style=ButtonStyle.PRIMARY, 
                                label="Yes", 
                                custom_id="add_yes_button", 
                                    ),
	                        Button(
                                style=ButtonStyle.DANGER, 
                                label="No", 
                                custom_id="add_no_button", 
                                    )
                            ]
                )

delete_row = ActionRow(
                components=[
                            Button(
                                style=ButtonStyle.PRIMARY, 
                                label="Yes", 
                                custom_id="delete_yes_button", 
                                    ),
	                        Button(
                                style=ButtonStyle.DANGER, 
                                label="No", 
                                custom_id="delete_no_button", 
                                    )
                            ]
                )

txt = it.TextInput(
    style=it.TextStyleType.PARAGRAPH,
    label="Why you chosed our guild among the others ?",
    custom_id="join_reason",
    min_length=3,
    max_length=900,
)
txt2 = it.TextInput(
    style=it.TextStyleType.PARAGRAPH,
    label="Explain your sense of humor : ",
    custom_id="humore_sense",
    min_length=3,
    max_length=900,
)

tt_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="update id", 
                custom_id="tt_b", )


l_first_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="⏪", 
                custom_id="l_first_button", )               
l_backward_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="◀", 
                custom_id="l_backward_button", )
l_stop_b = Button(
                style=ButtonStyle.DANGER, 
                label="◼",
                custom_id="l_stop_button", )
l_forward_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="▶", 
                custom_id="l_forward_button", )
l_last_b = Button(
                style=ButtonStyle.PRIMARY, 
                label="⏩", 
                custom_id="l_last_button", )
l_b_row = ActionRow(
                components=[
                          l_first_b,
                          l_backward_b,
                          l_stop_b,
                          l_forward_b,
                          l_last_b
                            ]
                )



presence = it.PresenceActivity(name="Leaderboard", type=it.PresenceActivityType.WATCHING)
bot = Client(os.getenv("TOKEN"),presence=it.ClientPresence(activities=[presence]),disable_sync=False)
#logging.basicConfig(level=logging.DEBUG)

@bot.event
async def on_ready():
    
    #global lock_state
    #print('Logging in as {0.user}'.format(bot))
    print("Logged in !")
    #settings = retrieve('settings')
    #lock_state = settings['lock']









@bot.command(
             name="leagues",
             description="Show members devided into leagues based on their xp"
            )        
async def leagues(ctx:CC):
    await ctx.defer()
    
    await ctx.send("Fetching Data ...")

    members_log = asyncio.run(makelogT("OWO"))
    l1 = League(members_log,"total")
    l1.sort_by_avg()
    embeded_leag = LeagueHelper(l1)
    embededs = embeded_leag.make_embeds()
    
    l_pager = embeded_leag.leagues_pager("l_pager_menu")


    user = ctx.author.user.username
    l_row = ActionRow(components=[l_pager])
    leag_reg[str(user)]=[0,0,l_row,embededs]
    await ctx.edit("Finished !",embeds=[embededs[0][0],embededs[0][1][0]],components=[l_row,l_b_row])

@bot.component("l_pager_menu")
async def l_pager_response(ctx:CPC,blah):
    cur_leag = int(ctx.data.values[0])
    data = leag_reg[str(ctx.author.user.username)] 
    main_embed = data[3][cur_leag][0]
    #cur_embed_num = data[0]
    cur_embed = data[3][cur_leag][1][0]
    leag_reg[str(ctx.author.user.username)][1]=cur_leag
    m_row = data[2]
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,l_b_row])

@bot.component("l_first_button")
async def l_first_response(ctx:CPC):
    data = leag_reg[str(ctx.author.user.username)] 
    leag_reg[str(ctx.author.user.username)][0] = 0
    cur_leag = data[1]
    cur_embed =  data[3][cur_leag][1][0]
    main_embed = data[3][cur_leag][0]
    m_row = data[2]
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,l_b_row])              

@bot.component("l_last_button")
async def l_last_response(ctx:CPC):
    data = leag_reg[str(ctx.author.user.username)] 
    cur_leag = data[1]
    last_embed_num = len(data[3][cur_leag][1]) - 1
    leag_reg[str(ctx.author.user.username)][0] = last_embed_num
    cur_embed =  data[3][cur_leag][1][last_embed_num]
    main_embed = data[3][cur_leag][0]
    m_row = data[2]
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,l_b_row])

@bot.component("l_backward_button")
async def l_backward_response(ctx:CPC):                  
    data = leag_reg[str(ctx.author.user.username)] 
    if data[0]>0:
        cur_embed_num = data[0]-1
    elif data[0] == 0:
        cur_embed_num = 0
    leag_reg[str(ctx.author.user.username)][0] = cur_embed_num
    cur_leag = data[1]
    cur_embed =  data[3][cur_leag][1][cur_embed_num]
    main_embed = data[3][cur_leag][0]
    m_row = data[2]
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,l_b_row])

@bot.component("l_forward_button")
async def l_forward_response(ctx:CPC):
    print(leag_reg)
    data = leag_reg[str(ctx.author.user.username)] 
    cur_leag = data[1]
    if data[0]<len(data[3][cur_leag][1])-1:
        cur_embed_num = data[0] + 1
    elif data[0] == len(data[3][cur_leag][1])-1:
        cur_embed_num = data[0]
    leag_reg[str(ctx.author.user.username)][0] = cur_embed_num
    print(leag_reg)
    cur_embed =  data[3][cur_leag][1][cur_embed_num]
    main_embed = data[3][cur_leag][0]
    m_row = data[2]
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,l_b_row])

@bot.component("l_stop_button")
async def l_stop_response(ctx:CPC):
    data = leag_reg[str(ctx.author.user.username)]
    cur_leag = data[1]
    cur_embed_num = data[0]
    cur_embed =  data[3][cur_leag][1][cur_embed_num]
    main_embed = data[3][cur_leag][0]
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[])














@bot.command(name="add_player",
            description="add new player to the event database",
            scope=922854662141526037,
            options=[
                it.Option(
                        name="player_name",
                        description="player's name to add the database",
            	        type=it.OptionType.STRING,
            	        required=True,
                          	),  
                ],		
            )
async def add_player(ctx:CC,player_name:str):
    exist = False
    await ctx.send(f'checking if {player_name} already exist in database ...')
    log = retrieve('0000')
    for player in log:
        if player.lower() == player_name.lower():
            exist = True
            break
    if exist:
        await ctx.edit(f"{player} already exist in database")
    else:
        await ctx.edit(f'checking if {player_name} exist in website ...')
        name = asyncio.run(checkName(player_name.lower()))
        if name == 'none':
            await ctx.edit(f"Player {name} not found.\nMake sure the pronounciation is correct.")
        else :
            add_reg[str(ctx.author.user.username)]=name
            await ctx.edit(f"found player {name}\nWanna add him/her to event database ?",components=add_row)

@bot.command(name="delete_player",
            description="delete player  the event database",
            scope=922854662141526037,
            options=[
                it.Option(
                        name="player_name",
                        description="player's name to detele from database",
         		        type=it.OptionType.STRING,
         		        required=True,
          	              	),  
                    ],
    		)
async def delete_player(ctx:CC,player_name:str):
    await ctx.send(f'checking if {player_name} exist ...')
    log = retrieve('0000')
    exist = False
    for player in log:
        if player.lower() == player_name.lower():
            delete_reg[str(ctx.author.user.username)]=player
            exist = True
            await ctx.edit(f"found player {player}\nWanna remove him/her from event database ?",components=delete_row)
            break
        else :
            pass
    if not exist :
        await ctx.edit(f"Player {player_name} not found.\nMake sure the pronounciation is correct.")

@bot.component("add_yes_button")
async def add_yes(ctx:CPC):
    res = False
    player_name = add_reg[str(ctx.author.user.username)]
    add_reg.pop(str(ctx.author.user.username))
    await ctx.edit(f"adding player {player_name} ....",components=[])
    member_log = asyncio.run(getPlayer(player_name))
    await ctx.edit(f'saving player {player_name} to db')
    log = retrieve('0000')
    log[player_name]=member_log
    updated_log = jsing(log)
    res = update('0000',updated_log)
    if res:
        add_msg = f"playerlayer {player_name} added successfully"
    else:
        add_msg = f"en error happened while adding {player_name}.\ntry again or later."
    await ctx.edit(add_msg)


@bot.component("add_no_button")
async def add_no(ctx:CPC):
    player_name = add_reg[ctx.author.user.username]
    add_reg.pop(str(ctx.author.user.username))
    await ctx.edit(f"you canceled adding player {player_name} ",components=[])

@bot.component("delete_yes_button")
async def delete_yes(ctx:CPC):
    state = False
    player_name = delete_reg[str(ctx.author.user.username)]    
    delete_reg.pop(str(ctx.author.user.username))
    await ctx.edit(f"deleting player {player_name} ....",components=[])
    log = retrieve('0000')
    log.pop(player_name)
    updated_log = jsing(log)
    state = update('0000',updated_log)
    if state:
        del_msg = f"player {player_name} deleted successfully"
    else:
        del_msg = f"en error happened while deleting {player_name}.\ntry again or later."
    await ctx.edit(del_msg)


@bot.component("delete_no_button")
async def delete_no(ctx:CPC):
    player_name = delete_reg[str(ctx.author.user.username)]
    delete_reg.pop(str(ctx.author.user.username))
    await ctx.edit(f"you canceled deleting player {player_name} ",components=[])




@bot.command(name="testing",description="test 1 2 3",scope=839662151010353172)
async def testing(ctx:CC):
    guilds = bot.guilds
    x=1
    for guild in guilds:
        print(x)
        x+=1
        print(dir(guild))
        print("///////////////")
        print(guild._json)
        await ctx.send("done")
    #await ctx.send("admin")

###############xp's gain leaderboard in skills########################

"""
@bot.command(name="gains",
            description="Show Guild's Leaderboard In (Total/Specific Skill)'s Xp Gain",
            options=[
                    it.Option(
                            name="skill",
                            description="The Leaderboard Skill",
             		        type=it.OptionType.STRING,
             		        required=True,
             		        choices=[
             			        it.Choice(name="Total",value="total"),
                	                it.Choice(name="Melee",value="melee"),
                	                it.Choice(name="Magic",value="magic"),
            	                    it.Choice(name="Mining",value="mining"),
           	                        it.Choice(name="Smithing",value="smithing"),
             	                    it.Choice(name="Woodcutting",value="woodcutting"),
           	                        it.Choice(name="Crafting",value="crafting"),              
             	                    it.Choice(name="Fishing",value="fishing"),
           	                        it.Choice(name="Cooking",value="cooking"),
                	                it.Choice(name="Tailoring",value="tailoring"),
             	                    ],
              	              	),  
                    ],		
            )        
async def gains(ctx:CC,skill:str):
    await ctx.defer()
    start = time.time()
    await ctx.send("Fetching newest records ...")
    old_record = retrieve("0000")
    players_list = []
    for i in old_record:
        players_list.append(i)
    if skill.lower() == 'total':
        if players_list != []:
            new_record = asyncio.run(makelogT(players_list))
        else :
            new_record = old_record
        unranked_data = SortUp('total',old_record,new_record)

        result = listFormater(unranked_data)
        embeds = makeEmbeds(result,"GoD","Total Xp")
        ranking_embeds = embeds[1]
        main_embed = embeds[0]
    else:
        if players_list != [] :
            new_record = asyncio.run(makelog(skill.lower(),players_list))
        else:
            new_record = old_record
        unranked_data = SortUp(skill.lower(),old_record,new_record)

        result = listFormater(unranked_data)
        embeds = makeEmbeds(result,"GoD",skill.capitalize())
        ranking_embeds = embeds[1]
        main_embed = embeds[0]
    user = ctx.author.user.username
    g_m_count = len(result[0])
    g_pager_reg[str(user)]=[0,g_m_count,ranking_embeds,main_embed]
    g_pager_m = pagerMaker(0,g_m_count,"g_pager_menu")
    g_m_row = ActionRow(components=[g_pager_m])
    end = time.time()
    t = math.ceil(end - start)
    await ctx.edit(f"Done in {t} seconds.",embeds=[main_embed,ranking_embeds[0]],components=[g_m_row,g_b_row])
"""

@bot.component("g_pager_menu")
async def g_pager_response(ctx:CPC,blah):
    chosen_page = int(ctx.data.values[0])
    data = g_pager_reg[str(ctx.author.user.username)] 
    count = data[1]
    cur_embed = data[2][chosen_page]
    main_embed = data[3]
    g_pager_reg[str(ctx.author.user.username)][0]=chosen_page
    g_n_pager = pagerMaker(chosen_page,count,'g_pager_menu')
    g_m_row = ActionRow(components=[g_n_pager])
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[g_m_row,g_b_row])

@bot.component("g_first_button")
async def g_first_response(ctx:CPC):
    print(str(ctx._json))
    data = g_pager_reg[str(ctx.author.user.username)] 
    g_pager_reg[str(ctx.author.user.username)][0] = 0
    count = data[1]
    cur_embed = data[2][0]
    main_embed = data[3]
    g_n_pager = pagerMaker(0,count,'g_pager_menu')
    g_m_row = ActionRow(components=[g_n_pager])
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[g_m_row,g_b_row])              

@bot.component("g_last_button")
async def g_last_response(ctx:CPC):
    data = g_pager_reg[str(ctx.author.user.username)] 
    chosen_page = len(data[2]) - 1
    g_pager_reg[str(ctx.author.user.username)][0] = chosen_page
    count = data[1]
    cur_embed = data[2][chosen_page]
    main_embed = data[3]
    g_n_pager = pagerMaker(chosen_page,count,'g_pager_menu')
    g_m_row = ActionRow(components=[g_n_pager])
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[g_m_row,g_b_row])

@bot.component("g_backward_button")
async def g_backward_response(ctx:CPC):                  
    data = g_pager_reg[str(ctx.author.user.username)] 
    if data[0]>0:
        chosen_page = data[0]-1
    elif data[0] == 0:
        chosen_page = 0
    g_pager_reg[str(ctx.author.user.username)][0] = chosen_page
    count = data[1]
    cur_embed = data[2][chosen_page]
    main_embed = data[3]
    g_n_pager = pagerMaker(chosen_page,count,'g_pager_menu')
    g_m_row = ActionRow(components=[g_n_pager])
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[g_m_row,g_b_row])

@bot.component("g_forward_button")
async def g_forward_response(ctx:CPC):
    data = g_pager_reg[str(ctx.author.user.username)] 
    if data[0]<len(data[2])-1:
        chosen_page = data[0] + 1
    elif data[0] == len(data[2]) - 1:
        chosen_page = len(data[2]) - 1
    g_pager_reg[str(ctx.author.user.username)][0] = chosen_page
    count = data[1]
    cur_embed = data[2][chosen_page]
    main_embed = data[3]
    g_n_pager = pagerMaker(chosen_page,count,'g_pager_menu')
    g_m_row = ActionRow(components=[g_n_pager])
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[g_m_row,g_b_row])

@bot.component("g_stop_button")
async def g_stop_response(ctx:CPC):
    data = g_pager_reg[str(ctx.author.user.username)]
    cur_pos = data[0]
    cur_embed = data[2][cur_pos]
    main_embed = data[3]
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[])

###############guild leaderboard in skills########################

@bot.command(name="guildlb",
            description="Show Guild's Leaderboard In Total Xp Or Specific Skill",
            options=[
                    it.Option(
                            name="skill",
                            description="The Leaderboard Skill",
             		        type=it.OptionType.STRING,
             		        required=True,
             		        choices=[
             			        it.Choice(name="Total",value="total"),
                	                it.Choice(name="Melee",value="melee"),
                                    it.Choice(name="Magic",value="magic"),
            	                    it.Choice(name="Mining",value="mining"),
           	                        it.Choice(name="Smithing",value="smithing"),
             	                    it.Choice(name="Woodcutting",value="woodcutting"),
           	                        it.Choice(name="Crafting",value="crafting"),              
             	                    it.Choice(name="Fishing",value="fishing"),
           	                        it.Choice(name="Cooking",value="cooking"),
                                    it.Choice(name="Tailoring",value="tailoring"),
             	                    ],
              	              	),
              	    it.Option(
              	       	    name="tag",
              	       	    description="Guild Tag To Look For",
              	       	    type=it.OptionType.STRING,
              	       	    required=True,
              	       	    ),   
                    ],		
            )        
async def guildlb(ctx:CC,skill:str,tag:str):
    await ctx.defer()
    g_tag = tag.upper()
    if len(g_tag) > 5 or len(g_tag) < 2:
        ctx.send("Invalid tag.\nValid tags length is between 2-5")
    else :
        await ctx.send("Fetching Data ...")
        if skill.lower() == "total":
            result = asyncio.run(searchtagtotal(g_tag)) 
            embeds = makeEmbeds(result,g_tag,"Total Xp")
            ranking_embeds = embeds[1]
            main_embed = embeds[0]
        else :
            skill_order = skills.index(skill.lower())
            result = asyncio.run(searchtag(skill_afx[skill_order],g_tag))
            embeds = makeEmbeds(result,g_tag,skill.capitalize())
            ranking_embeds = embeds[1]
            main_embed = embeds[0]
        user = ctx.author.user.username
        m_count = len(result[0])
        pager_reg[str(user)]=[0,m_count,ranking_embeds,main_embed]
        pager_m = pagerMaker(0,m_count,"pager_menu")
        m_row = ActionRow(components=[pager_m])
        await ctx.edit("Finished !",embeds=[main_embed,ranking_embeds[0]],components=[m_row,b_row])

@bot.component("pager_menu")
async def pager_response(ctx:CPC,blah):
    chosen_page = int(ctx.data.values[0])
    data = pager_reg[str(ctx.author.user.username)] 
    count = data[1]
    cur_embed = data[2][chosen_page]
    main_embed = data[3]
    pager_reg[str(ctx.author.user.username)][0]=chosen_page
    n_pager = pagerMaker(chosen_page,count,"pager_menu")
    m_row = ActionRow(components=[n_pager])
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,b_row])

@bot.component("first_button")
async def first_response(ctx:CPC):
    data = pager_reg[str(ctx.author.user.username)] 
    pager_reg[str(ctx.author.user.username)][0] = 0
    count = data[1]
    cur_embed = data[2][0]
    main_embed = data[3]
    n_pager = pagerMaker(0,count,"pager_menu")
    m_row = ActionRow(components=[n_pager])
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,b_row])              

@bot.component("last_button")
async def last_response(ctx:CPC):
    data = pager_reg[str(ctx.author.user.username)] 
    chosen_page = len(data[2]) - 1
    pager_reg[str(ctx.author.user.username)][0] = chosen_page
    count = data[1]
    cur_embed = data[2][chosen_page]
    main_embed = data[3]
    n_pager = pagerMaker(chosen_page,count,"pager_menu")
    m_row = ActionRow(components=[n_pager])
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,b_row])

@bot.component("backward_button")
async def backward_response(ctx:CPC):                  
    data = pager_reg[str(ctx.author.user.username)] 
    if data[0]>0:
        chosen_page = data[0]-1
    elif data[0] == 0:
        chosen_page = 0
    pager_reg[str(ctx.author.user.username)][0] = chosen_page
    count = data[1]
    cur_embed = data[2][chosen_page]
    main_embed = data[3]
    n_pager = pagerMaker(chosen_page,count,"pager_menu")
    m_row = ActionRow(components=[n_pager])
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,b_row])

@bot.component("forward_button")
async def forward_response(ctx:CPC):
    data = pager_reg[str(ctx.author.user.username)] 
    if data[0]<len(data[2])-1:
        chosen_page = data[0] + 1
    elif data[0] == len(data[2]) - 1:
        chosen_page = len(data[2]) - 1
    pager_reg[str(ctx.author.user.username)][0] = chosen_page
    count = data[1]
    cur_embed = data[2][chosen_page]
    main_embed = data[3]
    n_pager = pagerMaker(chosen_page,count,"pager_menu")
    m_row = ActionRow(components=[n_pager])
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[m_row,b_row])

@bot.component("stop_button")
async def stop_response(ctx:CPC):
    data = pager_reg[str(ctx.author.user.username)]
    cur_pos = data[0]
    cur_embed = data[2][cur_pos]
    main_embed = data[3]
    await ctx.edit("Finished !",embeds=[main_embed,cur_embed],components=[])

bot.start()









