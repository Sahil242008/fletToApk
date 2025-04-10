import flet as ft
import random

class Player:
    def __init__(self):
        self.name = "Necromancer"
        self.level = 1
        self.hp = 100
        self.mp = 100
        self.exp = 0
        self.morality = 0
        self.gold = 50
        self.reputation = 0
        self.skill_points = 0
        self.skills = {"Raise Dead": 1, "Bone Shield": 1, "Soul Blast": 1}
        self.inventory = {"bones": 0, "scrolls": 0, "soul_shards": 0, "equipment": []}
        self.companions = []

player = Player()

story_text = ft.Text(value="Welcome to Necromancer's Rise!", selectable=True, expand=True)
info_text = ft.Text(value="", size=12)
btns = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)


def update_info():
    info_text.value = f"HP: {player.hp} | MP: {player.mp} | Lvl: {player.level} | EXP: {player.exp}/100\n" \
                     f"Gold: {player.gold} | Rep: {player.reputation} | Skill Pts: {player.skill_points}\n" \
                     f"Inventory: {player.inventory} | Companions: {[c for c in player.companions]}"

def set_story(text, options):
    story_text.value = text
    btns.controls.clear()
    for opt in options:
        btn = ft.ElevatedButton(text=opt[0], on_click=opt[1])
        btns.controls.append(btn)
    update_info()


def gain_exp(amount):
    player.exp += amount
    if player.exp >= 100:
        player.exp -= 100
        player.level += 1
        player.hp += 20
        player.mp += 20
        player.skill_points += 1
        for skill in player.skills:
            player.skills[skill] += 1
        set_story(f"You leveled up to {player.level}!", [("Continue", main_town)])
    else:
        main_town(None)


# Feature: Dungeon Exploration
def explore_dungeon(e):
    encounters = ["skeletal knight", "haunted armor", "ghost"]
    encounter = random.choice(encounters)
    reward = random.randint(30, 70)
    player.gold += reward // 2
    set_story(f"You encounter a {encounter}! You defeat it and earn {reward} EXP and {reward // 2} gold.",
              [("Continue", lambda e: gain_exp(reward))])


# Feature: Skill Tree Upgrade
def skill_tree(e):
    if player.skill_points <= 0:
        set_story("You don't have any skill points.", [("Back", main_town)])
        return

    options = []
    for skill, lvl in player.skills.items():
        def make_upgrader(s=skill):
            def upgrade(ev):
                player.skills[s] += 1
                player.skill_points -= 1
                set_story(f"{s} upgraded to level {player.skills[s]}", [("Back", main_town)])
            return upgrade
        options.append((f"Upgrade {skill} (lvl {lvl})", make_upgrader()))
    options.append(("Back", main_town))
    set_story("Choose a skill to upgrade:", options)


# Feature: Reputation & Companions
def rumor_board(e):
    choices = [
        ("Help villagers (gain rep, lose gold)", lambda e: rep_action(True)),
        ("Extort villagers (lose rep, gain gold)", lambda e: rep_action(False)),
        ("Back", main_town)
    ]
    set_story("You hear rumors around town. What do you do?", choices)

def rep_action(kind):
    if kind:
        player.reputation += 3
        player.gold = max(0, player.gold - 10)
        player.companions.append("Grateful Villager")
        set_story("You helped a villager. They've joined your cause.", [("Back", main_town)])
    else:
        player.reputation -= 3
        player.gold += 15
        set_story("You demanded gold through fear.", [("Back", main_town)])


# Feature: Equipment

def equipment_shop(e):
    items = [("Bone Wand (+5 MP) - 20g", "Bone Wand"),
             ("Skull Amulet (+5 HP) - 25g", "Skull Amulet")]

    def buy_item(item, cost):
        def buy(e):
            if player.gold >= cost:
                player.gold -= cost
                player.inventory['equipment'].append(item)
                set_story(f"You bought {item}.", [("Back", main_town)])
            else:
                set_story("You don't have enough gold.", [("Back", main_town)])
        return buy

    choices = [(label, buy_item(item, int(label.split('-')[-1].strip('g')))) for label, item in items]
    choices.append(("Back", main_town))
    set_story("Welcome to the Equipment Shop:", choices)


# Main town hub

def main_town(e):
    set_story("You arrive at Brimvale, a haven for your kind. Where to?", [
        ("Explore Dungeon", explore_dungeon),
        ("Upgrade Skills", skill_tree),
        ("Rumor Board (Reputation)", rumor_board),
        ("Equipment Shop", equipment_shop),
        ("Rest (10g)", rest_at_inn),
        ("Continue Journey (Exit)", lambda e: set_story("[To be continued...]", []))
    ])


# Rest

def rest_at_inn(e):
    if player.gold >= 10:
        player.gold -= 10
        player.hp = 100 + (player.level - 1) * 20
        player.mp = 100 + (player.level - 1) * 20
        set_story("You feel rested.", [("Back", main_town)])
    else:
        set_story("Not enough gold.", [("Back", main_town)])


# App entry point
def main(page: ft.Page):
    page.title = "Necromancer's Rise"
    page.scroll = ft.ScrollMode.ALWAYS
    page.add(story_text, btns, info_text)
    main_town(None)

ft.app(target=main)


