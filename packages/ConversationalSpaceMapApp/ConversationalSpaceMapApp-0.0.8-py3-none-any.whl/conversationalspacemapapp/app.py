"""
Generate conversational space maps for interview data.
"""

import toga
from toga.style import Pack
from toga.constants import COLUMN
import toga_chart
import pathlib
import platform

import conversationalspacemapapp.Parser.TranscriptParser as TranscriptParser
import conversationalspacemapapp.Plotter.PlotMap as PlotMap


class ConversationalSpaceMapApp(toga.App):

    @property
    def is_empty_selection(self):
        return len(self.path_input.items) > 0

    def startup(self):
        self.parser: TranscriptParser.AbstractParser = None
        self.map = None
        self.plot_title = ""

        box = toga.Box()

        self.path_input = toga.Selection(
            items=self._get_file_history(),
            on_change=self._set_file
        )
        self.path_input.style.padding = 5
        self.path_input.readonly = True
        self.path_input.style.flex = 10

        self.button = toga.Button("File", on_press=self.button_handler)
        self.button.style.padding = 5
        self.button.style.flex = 1

        self.flip = toga.Switch("Flip", on_change=self.plot_handler)
        self.flip.enabled = self.is_empty_selection
        self.flip.style.padding = 5
        self.flip.style.flex = 0.1

        self.plot = toga.Button("Plot", on_press=self.plot_handler)
        self.plot.enabled = self.is_empty_selection
        self.plot.style.padding = 5
        self.plot.style.flex = 1

        self.selection = toga.Selection(
            items=[
                {"name": "PDF", "format": ".pdf"},
                {"name": "PNG", "format": ".png"},
                {"name": "SVG", "format": ".svg"},
            ],
            accessor="name",
        )
        self.selection.style.padding = 5
        self.selection.style.flex = 1

        self.save = toga.Button("Save", on_press=self.save_handler)
        self.save.enabled = False
        self.save.style.padding = 5
        self.save.style.flex = 1

        self.label = toga.Label("")
        self.label.style.padding = 5

        self.chart = toga_chart.Chart(style=Pack(flex=1), on_draw=self.draw_chart)
        self.chart.style.padding = 5
        self.chart.style.flex = 1

        box.add(self.path_input)
        box.add(self.button)
        box.add(self.flip)
        box.add(self.plot)
        box.add(self.selection)
        box.add(self.save)

        main = toga.Box(
            children=[
                box,
                self.label,
                self.chart
            ],
            style=Pack(direction=COLUMN),
        )
        description = toga.WebView()
        description.set_content(
            root_url="",
            content=self._load_about_content()
        )
        description.style.padding = 5
        description.style.flex = 1

        if "macOS" in platform.platform():
            description.style.background_color = "transparent"

        about = toga.Box(
            children=[description],
            style=Pack(direction=COLUMN),
        )

        container = toga.OptionContainer(
            content=[("Home", main), ("About", about)]
        )
        container.style.padding = 5
        if "macOS" in platform.platform():
            container.style.background_color = "transparent"

        self.main_window = toga.MainWindow()
        self.main_window.content = container
        self.main_window.size = toga.Size(width=1300, height=1000)
        self.main_window.show()

    def draw_chart(self, chart, figure, *args, **kwargs):
        if self.parser is not None:
            figure.clf()
            # Add a subplot that is a histogram of the data, using the normal matplotlib API
            ax = figure.add_subplot(1, 1, 1)

            self.map = PlotMap.MapBarPlot(
                parser=self.parser,
                ax=ax,
                fig=figure
            )
            self.map.plot(title=self.plot_title, flip_roles=self.flip.value)
            figure.tight_layout()
        else:
            return

    async def button_handler(self, widget):
        file = await self.main_window.open_file_dialog("Open file")
        path = pathlib.Path(file)
        try:
            self.path_input.value = path
        except ValueError:
            self.path_input.items.append(path)
            self.path_input.value = path
            self._write_file_history()
        self._set_file(widget)

    def _set_file(self, widget):
        if self.path_input.value.is_file():
            self.plot_title = self.path_input.value.stem
            self.plot.enabled = True
            self.flip.enabled = True
        else:
            Exception("File not valid: " + self.path_input.value.as_posix())

    def _write_file_history(self):
        history = pathlib.Path(__file__).parent / "resources" / "history.txt"
        content = str(self.path_input.value)
        if history.is_file() and len(content.strip()) != 0:
            with open(history, "a") as f:
                f.write(content + "\n")

    def plot_handler(self, widget):
        self.parser = TranscriptParser.TimestampCleanParser(self.path_input.value)
        self.chart.redraw()
        self.save.enabled = True
        self._set_label(widget)

    def save_handler(self, widget):
        if self.path_input.value is not None:
            path = pathlib.Path(self.path_input.value).parent.resolve() / (
                    str(pathlib.Path(self.path_input.value).stem) + '_csm' + self.selection.value.format)
            self.map.save(path)
        else:
            return

    def _set_label(self, widget):
        if self.flip.value:
            number_of_words = self.parser.number_of_words_by_speaker[::-1]
        else:
            number_of_words = self.parser.number_of_words_by_speaker
        total_words = sum(number_of_words)
        speaker1_words = number_of_words[0]
        speaker2_words = number_of_words[1]
        self.label.text = (
            f"Total words: {total_words} / "
            f"Words interviewer: {speaker1_words} ({round(100 * speaker1_words / total_words, ndigits=1)}%) / "
            f"Words interviewee: {speaker2_words} ({round(100 * speaker2_words / total_words, ndigits=1)}%) / "
            f"Total utterances: {len(self.parser.map_list)}"
        )
        self.label.refresh()

    def _get_file_history(self) -> [pathlib.Path]:
        history = pathlib.Path(__file__).parent / "resources" / "history.txt"
        if history.is_file():
            with open(history, "r") as f:
                output = []
                files = sorted(f.readlines())
                for file in files:
                    file = file.strip("\n")
                    file = pathlib.Path(file)
                    if file.is_file():
                        output.append(file)
                return output
        else:
            return []

    def _load_about_content(self):
        file_path = pathlib.Path(__file__).parent / "resources" / "about.html"
        if file_path.is_file():
            return file_path.read_text()
        else:
            return "No about page available"


def main():
    return ConversationalSpaceMapApp(
        "Conversational Space Map App",
        "ch.manuelbieri.conversationalspacemapapp",
        icon="resources/icon.png",
    )
