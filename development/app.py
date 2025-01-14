from grim.character import Character
from grim.character.layers import classes, races
from grim.character.stats import Attributes, Saves
from textual import events, on
from textual.app import App as BaseApp
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Footer, Header, Label, ListItem, ListView, Select

RACES = (races.Human, races.Elf)
CLASSES = (classes.Fighter, classes.Cleric)

char: Character = Character.roll()


class CharacterChoices(Container):  # type: ignore
    def compose(
        self,
    ) -> ComposeResult:
        yield Select(
            prompt="Race",
            options=[(race.name, race) for race in RACES],
        )
        yield Select(
            prompt="Class",
            options=[(class_.name, class_) for class_ in CLASSES],
        )


class AttributeLabel(Label):  # type: ignore
    av = reactive("-")
    is_main = reactive(False)

    def watch_av(
        self,
        value: int,
    ) -> None:
        self.update(f"{self.name}{'*' if self.is_main else ''}: {str(self.av)}")


class SaveLabel(Label):  # type: ignore
    sv = reactive("-")

    def watch_sv(
        self,
        value: int,
    ) -> None:
        self.update(f"{self.name}: {str(self.sv)}")


class AttributesSheet(Container):  # type: ignore
    def compose(
        self,
    ) -> ComposeResult:
        attribute_labels = [ListItem(AttributeLabel(name=a.name, id=f"attr_{a.name.lower()}")) for a in Attributes]
        yield Label(
            "Attributes",
            classes="head_label",
        )
        yield ListView(*attribute_labels)


class SavesSheet(Container):  # type: ignore
    def compose(
        self,
    ) -> ComposeResult:
        sl = [ListItem(SaveLabel(name=s.name, id=f"save_{s.name.lower()}")) for s in Saves]
        save_labels = sl[0:3]
        save_labels.append(ListItem(Label("")))
        save_labels.append(sl[-1])
        yield Label(
            "Saves",
            classes="head_label",
        )
        yield ListView(*save_labels)


class App(BaseApp):  # type: ignore
    CSS_PATH = "app.tcss"
    BINDINGS = [
        ("c", "create_char", "Roll a new playing character"),
    ]
    TITLE = "GRIM"

    def compose(
        self,
    ) -> ComposeResult:
        yield Header()
        yield Footer()

    async def action_create_char(
        self,
    ) -> None:
        global char
        char = Character.roll()
        cc = CharacterChoices(id="char_choices")
        atts = AttributesSheet(id="attrs_sheet")
        savs = SavesSheet(id="saves_sheet")
        self.current_widgets = [
            cc,
            atts,
            savs,
        ]
        await self.mount(cc)
        await self.mount(atts)
        await self.mount(savs)
        self.sub_title = "Create a new character"
        await self.update_stats()

    @on(Select.Changed)  # type: ignore
    async def select_changed(
        self,
        event: Select.Changed,
    ) -> None:
        global char
        if event.value == Select.BLANK:
            if event.control.prompt == "Class":
                char.remove(classes.Class)
            else:
                char.remove(races.Race)
            return

        char.remove(event.value)

        if issubclass(event.value, classes.Class):
            char.lay(event.value)
            if char.class_ and char.class_.has_pending_choices:
                for choice in char.class_.pending_choices:
                    cc = self.query_one(CharacterChoices)
                    cc.mount(
                        Select(prompt=choice, options=[(a.name, v) for (a, v) in char.class_.pending_choices[choice]])
                    )

        if issubclass(event.value, races.Race):
            char.lay(event.value)
            if char.race and char.race.has_pending_choices:
                for choice in char.race.pending_choices:
                    pass

        await self.update_stats()

    async def update_stats(self) -> None:
        for a in Attributes:
            w = self.query_one(f"#attr_{a.name.lower()}")
            w.av = getattr(char.attributes, a.name)

        for s in Saves:
            w = self.query_one(f"#save_{s.name.lower()}")
            w.sv = getattr(char.saves, s.name)

    async def on_key(
        self,
        event: events.Key,
    ) -> None:
        if event.key == "q" and len(self.current_widgets):
            for widget in self.current_widgets:
                await widget.remove()  # type: ignore
            self.current_widgets = []
            self.sub_title = ""


if __name__ == "__main__":
    app = App()
    app.run()
