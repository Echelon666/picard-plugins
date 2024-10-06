PLUGIN_NAME = "Albums Statistics"
PLUGIN_AUTHOR = "Echelon"
PLUGIN_VERSION = '0.1'
PLUGIN_API_VERSIONS = ['2.2']
PLUGIN_LICENSE = "GPL-2.0-or-later"
PLUGIN_LICENSE_URL = "https://www.gnu.org/licenses/gpl-2.0.html"
PLUGIN_DESCRIPTION = '''Counts the quality or status of albums.

A - An integer variable counting albums Incomplete & unchanged,
B - An integer variable counting albums Incomplete & modified,
C - An integer variable counting albums Complete & unchanged,
D - An integer variable counting albums Complete & modified,
E - An integer variable counting albums Errored,
T - An integer variable summing up the above variables'''

from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget
from PyQt5.QtGui import QPixmap, QIcon

from picard.ui.itemviews import BaseAction, register_album_action

statwindow = QWidget()
grid = QGridLayout()

statwindow.setLayout(grid)
statwindow.setGeometry(100, 100, 400, 200)
statwindow.setWindowTitle("Albums Statistics")
statwindow.setWindowIcon(QIcon(":/images/16x16/org.musicbrainz.Picard.png"))
statwindow.setStyleSheet("font-size:12pt;")

class AlbumStats(BaseAction):
    NAME = "Statistics"

    def callback(self, objs):
        A = B = C = D = E = 0

        while grid.count():
            item = grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.clear()

        icon1 = QLabel()
        icon1.setPixmap(QPixmap(":/images/22x22/media-optical.png"))
        icon2 = QLabel()
        icon2.setPixmap(QPixmap(":/images/22x22/media-optical-modified.png"))
        icon3 = QLabel()
        icon3.setPixmap(QPixmap(":/images/22x22/media-optical-saved.png"))
        icon4 = QLabel()
        icon4.setPixmap(QPixmap(":/images/22x22/media-optical-saved-modified.png"))
        icon5 = QLabel()
        icon5.setPixmap(QPixmap(":/images/22x22/media-optical-error.png"))

        grid.addWidget(icon1, 1, 0)
        grid.addWidget(icon2, 2, 0)
        grid.addWidget(icon3, 3, 0)
        grid.addWidget(icon4, 4, 0)
        grid.addWidget(icon5, 5, 0)

        grid.addWidget(QLabel("The status of the selected Albums is as follows:"), 0, 0, 1, 3)
        grid.addWidget(QLabel("Incomplete & unchanged"), 1, 2)
        grid.addWidget(QLabel("Incomplete & modified"), 2, 2)
        grid.addWidget(QLabel("Complete & unchanged"), 3, 2)
        grid.addWidget(QLabel("Complete & modified"), 4, 2)
        grid.addWidget(QLabel("Errored"), 5, 2)
        grid.addWidget(QLabel("Total"), 6, 2)

        for album in objs:
            if album.errors:
                E = E + 1
            elif album.is_complete():
                if album.is_modified():
                    D = D + 1
                else:
                    C = C + 1
            else:
                if album.is_modified():
                    B = B + 1
                else:
                    A = A + 1

        T = A + B + C + D + E

        grid.addWidget(QLabel(str(A)), 1, 1)
        grid.addWidget(QLabel(str(B)), 2, 1)
        grid.addWidget(QLabel(str(C)), 3, 1)
        grid.addWidget(QLabel(str(D)), 4, 1)
        grid.addWidget(QLabel(str(E)), 5, 1)
        grid.addWidget(QLabel(str(T)), 6, 1)

        statwindow.show()

register_album_action(AlbumStats())