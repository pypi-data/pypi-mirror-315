import sys
from typing import Optional

from PyQt6.QtWidgets import QApplication, QStyle, QStyleFactory
from fmtransfer.FmTransferWindow import FmTransferWindow


def _main() -> int:
    try:
        app = QApplication(sys.argv)
        style: Optional[QStyle] = app.style()
        if style is not None and style.name() == "windows11":
            app.setStyle(QStyleFactory.create('Fusion'))
        fm_transfer = FmTransferWindow()
        fm_transfer.show()
        return app.exec()
    except KeyboardInterrupt as e:
        print("ERROR: ", str(e))
        return 1
    except Exception as e:
        print("ERROR: ", str(e))
        return 1


if __name__ == '__main__':
    sys.exit(_main())
