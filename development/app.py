from grim.character import Character, classes

# from grim.character.stats import Attribute, Save
from textual import events, on
from textual.app import App as BaseApp
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Footer, Header, Label, ListView, Select

char: Character | None = None


class CharacterChoices(Container):  # type: ignore
    def compose(self) -> ComposeResult:
        yield Select(
            prompt="Class",
            options=[("Fighter", classes.Fighter), ("Cleric", classes.Cleric)],
        )


class AttributeLabel(Label):  # type: ignore
    av = reactive("-")
    is_main = reactive(False)

    def watch_av(self, value: int) -> None:
        self.update(f"{self.name}{'*' if self.is_main else ''}: {str(self.av)}")


class SaveLabel(Label):  # type: ignore
    sv = reactive("-")

    def watch_sv(self, value: int) -> None:
        self.update(f"{self.name}: {str(self.sv)}")


class AttributesSheet(Container):  # type: ignore
    def compose(self) -> ComposeResult:
        # attribute_labels = [ListItem(AttributeLabel(name=a.name, id=f"attr_{a.name.lower()}")) for a in Attribute]
        attribute_labels: list[str] = []
        yield Label("Attributes", classes="head_label")
        yield ListView(*attribute_labels)


class SavesSheet(Container):  # type: ignore
    def compose(self) -> ComposeResult:
        # sl = [ListItem(SaveLabel(name=s.name, id=f"save_{s.name.lower()}")) for s in Save]
        # save_labels = sl[0:3]
        # save_labels.append(ListItem(Label("")))
        # save_labels.append(sl[-1])
        save_labels: list[str] = []
        yield Label("Saves", classes="head_label")
        yield ListView(*save_labels)


class App(BaseApp):  # type: ignore
    CSS_PATH = "app.tcss"
    BINDINGS = [
        ("c", "create_char", "Roll a new playing character"),
    ]
    TITLE = "GRIM"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    async def action_create_char(self) -> None:
        global char
        char = Character.roll()
        cc = CharacterChoices(id="char_choices")
        atts = AttributesSheet(id="attrs_sheet")
        savs = SavesSheet(id="saves_sheet")
        self.current_widgets = [cc, atts, savs]
        await self.mount(cc)
        await self.mount(atts)
        await self.mount(savs)
        self.sub_title = "Create a new character"

    @on(Select.Changed)  # type: ignore
    async def select_changed(self, event: Select.Changed) -> None:
        pass
        # char = Character.roll(class_=event.value)  # type: ignore
        # for a in Attribute:
        #    w = self.query_one(f"#attr_{a.name.lower()}")
        #    w.is_main = a.name == char.main_attribute.name
        #    w.av = char.attributes[a]
        # for s in Save:
        #    w = self.query_one(f"#save_{s.name.lower()}")
        #    w.sv = char.saves[s].val

    async def on_key(self, event: events.Key) -> None:
        if event.key == "q" and len(self.current_widgets):
            for widget in self.current_widgets:
                await widget.remove()  # type: ignore
            self.current_widgets = []
            self.sub_title = ""


if __name__ == "__main__":
    app = App()
    app.run()
