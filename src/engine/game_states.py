import tcod.event
import tcod.sdl.render


class InventoryBox:
    def __init__(self, x, y, width, height, item=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.item = item

    def render(self, x, y, window):
        window.console.print_box(
            x=x,
            y=y,
            width=self.width,
            height=self.height,
            string=self.item.type,
        )


def inventory_state(engine, window):
    box_width = 14
    box_height = 20
    player_items = engine.player.inventory.items
    num_pages = len(player_items) // 15
    all_page_items = [[] for _ in range(num_pages + 1)]
    i = 0
    for item in player_items:
        all_page_items[i].append(item)
        if len(all_page_items[i]) == 15:
            i += 1
    current_page = 0
    while True:
        window.console.clear()

        window.console.draw_frame(
            0,
            0,
            window.width,
            window.height,
            title="Inventory",
            fg=(255, 255, 255),
            bg=(0, 0, 0),
            clear=True,
        )

        x_offset = 3
        y_offset = 4
        if len(player_items) == 0:
            window.console.print(
                window.width // 2,
                window.height // 2,
                "Inventory is empty",
                fg=(255, 255, 255),
                alignment=tcod.CENTER,
            )
        else:
            for item in all_page_items[current_page]:
                if x_offset + 5 > window.width:
                    x_offset = 3
                    y_offset += box_height + 1
                window.console.print_box(
                    x=x_offset,
                    y=y_offset,
                    width=box_width,
                    height=box_height,
                    string=item.type,
                )
                x_offset += box_width + 1

        window.console.print(
            window.width // 2,
            window.height,
            "Press the number next to the item to use it",
        )

        window.context.present(window.console)

        events = tcod.event.wait()

        event = engine.handle_inventory_events(events)

        if event == "close":
            engine.inventory_open = False
            break
        elif event == "next_page":
            if current_page < num_pages:
                current_page += 1
        elif event == "previous_page":
            if current_page > 0:
                current_page -= 1


def main_menu(engine, window):
    while True:
        events = tcod.event.wait()
        if engine.handle_main_menu_events(events) == "new_game":
            return "playing"
        window.console.clear(bg=(0, 0, 0))

        window.console.draw_frame(
            0,
            0,
            window.width,
            window.height,
            title="Main menu",
            fg=(255, 255, 255),
            bg=(0, 0, 0),
            clear=True,
        )

        window.console.print(
            x=window.width // 2,
            y=window.height // 2 - 4,
            string="Press enter to start",
            fg=(255, 255, 255),
            alignment=tcod.CENTER,
        )

        window.context.present(window.console)


def level_up_state(engine, window):
    available_points = engine.player.intelligence // 2 + 5
    temp_stats = (
        engine.player.max_hp,
        engine.player.strength,
        engine.player.perception,
        engine.player.dexterity,
        engine.player.intelligence,
    )

    while available_points > 0:
        events = tcod.event.wait()
        stat = engine.handle_level_up_events(events)
        if stat is not None and stat != "reset":
            if stat == "max_hp":
                engine.player.max_hp += 1
            elif stat == "strength":
                engine.player.strength += 1
            elif stat == "perception":
                engine.player.perception += 1
            elif stat == "dexterity":
                engine.player.dexterity += 1
            elif stat == "intelligence":
                engine.player.intelligence += 1
            available_points -= 1
        elif stat == "reset":
            engine.player.max_hp = temp_stats[0]
            engine.player.strength = temp_stats[1]
            engine.player.perception = temp_stats[2]
            engine.player.dexterity = temp_stats[3]
            engine.player.intelligence = temp_stats[4]
            available_points = engine.player.intelligence // 2 + 5
        window.console.clear(bg=(0, 0, 0))
        window.console.draw_frame(
            window.width // 2 - 20,
            10,
            window.width - 40,
            window.height - 20,
            "Level Up !",
            clear=False,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        window.console.print(
            window.width // 2 - 10,
            12,
            "Available points: " + str(available_points),
            fg=(0, 255, 0),
        )

        window.console.print(
            window.width // 2 - 18,
            24,
            f"Max HP: {engine.player.max_hp} (1)",
            fg=(255, 255, 255),
        )

        window.console.print(
            window.width // 2 - 18,
            40,
            f"Strength: {engine.player.strength} (3)",
            fg=(255, 255, 255),
        )

        window.console.print(
            window.width // 2 - 18,
            54,
            f"Dexterity: {engine.player.dexterity} (5)",
            fg=(255, 255, 255),
        )

        window.console.print(
            window.width // 2,
            24,
            f"Perception: {engine.player.perception} (2)",
            fg=(255, 255, 255),
        )

        window.console.print(
            window.width // 2,
            40,
            f"Intelligence: {engine.player.intelligence} (4)",
            fg=(255, 255, 255),
        )

        window.console.print(
            window.width // 2,
            45,
            f"Press the number\n\n of the stat you\n\n want to increase",
            fg=(0, 255, 255),
        )

        window.console.print(
            window.width // 2,
            56,
            f"Reset (R)",
            fg=(255, 0, 0),
        )

        window.context.present(window.console)
        engine.update_fov()


def death_state(engine, window):
    window.console.clear(bg=(0, 0, 0))
    while True:
        events = tcod.event.wait()
        engine.handle_death_events(events)
        window.console.print_box(
            window.width // 2 - 5,
            window.height // 2,
            100,
            200,
            "You died!",
            fg=(255, 0, 0),
        )
        window.console.print_box(
            window.width // 2 - 10,
            window.height - 5,
            20,
            5,
            "Press esc to to quit",
            fg=(255, 255, 255),
        )
        window.context.present(window.console)
