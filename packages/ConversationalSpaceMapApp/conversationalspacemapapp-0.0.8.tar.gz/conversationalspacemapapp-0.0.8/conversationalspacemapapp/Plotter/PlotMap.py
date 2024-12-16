import matplotlib.pyplot as plt
import conversationalspacemapapp.Parser.TranscriptParser as TranscriptParser


class MapBarPlot:
    def __init__(self, parser: TranscriptParser.AbstractParser, fig: plt.figure, ax: plt.Axes):
        self.parser = parser
        self.ax = ax
        self.fig = fig

    def _flip(self, flip_roles=False):
        if flip_roles:
            return [ -i for i in self.parser.map_list]
        else:
            return self.parser.map_list

    def plot(self, title: str, flip_roles=False):
        words: list[int] = self._flip(flip_roles=flip_roles)
        index = [*range(1, len(words) + 1)]
        self.ax.barh(index, words, align='center', height=0.8)

        # Set x-axis
        xlim_num = max([abs(number) for number in words])*1.1
        self.ax.set_xlim([-xlim_num, xlim_num])
        self.ax.xaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.25)

        # Set y-axis
        self.ax.set_ylim([-2, max(index)+2])
        self.ax.set_yticks(index)

        # Set plot labels
        self.ax.set_title("Conversational Map Space " + title)
        self.ax.text(xlim_num/2, -1, "Participant's words per utterance", horizontalalignment='center')
        self.ax.text(-xlim_num/2, -1, "Interviewer's words per utterance", horizontalalignment='center')
        self.ax.set_ylabel("Utterance (bottom = start of interview)")
        self.fig.tight_layout()

    def save(self, filename: str):
        self.fig.savefig(filename, dpi=300)


