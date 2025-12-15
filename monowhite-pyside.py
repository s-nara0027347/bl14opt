# pip install PySide6 pyserial requests beautifulsoup4

import sys
import time
import datetime
import requests
import serial
from bs4 import BeautifulSoup

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QMessageBox
)
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont


# ==============================
# PM16C TCP Client（完全踏襲＋堅牢化）
# ==============================
class PM16CClient:
    def __init__(self, host="192.168.67.150", port=10001):
        self.ser = serial.serial_for_url(
            f"socket://{host}:{port}",
            timeout=1,
            write_timeout=1
        )
        self.last_value = {}

        # 初期化（元コード完全踏襲）
        self.write("S1R")
        for _ in range(2):
            self.write("S111")
            self.write("S124")
            time.sleep(0.2)

    def write(self, cmd: str):
        self.ser.write((cmd + "\r\n").encode())

    def query(self, cmd: str) -> str:
        self.write(cmd)
        return self.ser.readline().decode().strip()

    def get_value(self, ch: int) -> int:
        try:
            hexch = hex(ch).lstrip("0x").upper().zfill(1)
            value = self.query("S4" + hexch + "0").lstrip("R")

            # 16進数チェック（移動中のゴミ対策）
            if not value or any(c not in "0123456789ABCDEFabcdef" for c in value):
                raise ValueError

            v = int.from_bytes(
                bytes.fromhex(value.zfill(6)),
                byteorder="big",
                signed=True
            )
            self.last_value[ch] = v
            return v

        except Exception:
            return self.last_value.get(ch, 0)

    def amove(self, ch: str, chn: int, pulse: int):
        if ch == "A":
            com = "2"
            self.write("S11" + hex(chn).lstrip("0x").upper().zfill(1))
        elif ch == "B":
            com = "3"
            self.write("S12" + hex(chn).lstrip("0x").upper().zfill(1))
        else:
            return

        if pulse == self.get_value(chn):
            raise RuntimeError("there is no need")

        put_pulse = pulse.to_bytes(3, "big", signed=True).hex().upper()
        self.write("S1303")
        self.write("S3" + com + put_pulse + "11")


# ==============================
# HTML 状態取得
# ==============================
def htmlget(diname, time_str):
    url = (
        "http://srweb-dmz-03.spring8.or.jp/cgi-bin/MDAQ/"
        f"mdaq_arcdisp.py?signalname={diname}%2Fstatus&time={time_str}"
    )
    return requests.get(url).content


# ==============================
# Main Window
# ==============================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.pmch = {'mono': 1, 'gamma': 4}
        self.posdic = {
            'monoZ_W': -135000,
            'monoZ_M': 6000,
            'gamma_W': -90000,
            'gamma_M': 0
        }
        self.change = None

        self.pm = PM16CClient()

        self.init_ui()
        self.init_timer()

    # ==========================
    def init_ui(self):
        self.setWindowTitle("M_W Move")

        mono_font = QFont("Courier New", 24)

        self.mbs = QLabel("unacquired")
        self.dss = QLabel("unacquired")
        self.opt = QLabel("unacquired")
        self.opt2 = QLabel("unacquired")
        self.exp = QLabel("unacquired")
        self.monoz = QLabel("----")
        self.gamma = QLabel("----")

        self.monoz.setFont(mono_font)
        self.gamma.setFont(mono_font)

        self.update_btn = QPushButton("update")
        self.mono_btn = QPushButton("Mono Mode")
        self.white_btn = QPushButton("White Mode")

        self.update_btn.clicked.connect(self.update_status)
        self.mono_btn.clicked.connect(self.to_mono)
        self.white_btn.clicked.connect(self.to_white)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Mono-White Switch Program"))
        layout.addWidget(self.update_btn)

        layout.addWidget(QLabel("▼Component Status"))
        for name, lbl in [
            ("MBS Status", self.mbs),
            ("DSS Status", self.dss),
            ("Opt Hatch Status", self.opt),
            ("Opt2 Hatch Status", self.opt2),
            ("Exp Hatch Status", self.exp),
        ]:
            row = QHBoxLayout()
            row.addWidget(QLabel(name))
            row.addWidget(lbl)
            layout.addLayout(row)

        layout.addWidget(QLabel("▼Axis Position"))
        for name, lbl in [
            ("MonoZZ Position", self.monoz),
            ("γStopper Position", self.gamma),
        ]:
            row = QHBoxLayout()
            row.addWidget(QLabel(name))
            row.addWidget(lbl)
            layout.addLayout(row)

        btns = QHBoxLayout()
        btns.addWidget(self.mono_btn)
        btns.addWidget(self.white_btn)
        layout.addLayout(btns)

        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

    # ==========================
    def init_timer(self):
        self.pos_timer = QTimer(self)
        self.pos_timer.setInterval(300)
        self.pos_timer.timeout.connect(self.update_position)

    # ==========================
    def set_buttons(self, enable: bool):
        self.mono_btn.setEnabled(enable)
        self.white_btn.setEnabled(enable)
        self.update_btn.setEnabled(enable)

    # ==========================
    def set_state_label(self, label: QLabel, text: str, open_: bool):
        label.setText(text)
        if open_:
            label.setStyleSheet("color: green; font-weight: bold;")
        else:
            label.setStyleSheet("color: red; font-weight: bold;")

    # ==========================
    def update_status(self):
        dt = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        soup_hatch = BeautifulSoup(htmlget('bl_plc_14b1_di_25', dt), "html.parser")
        soup_shut = BeautifulSoup(htmlget('bl_plc_14b1_di_9', dt), "html.parser")

        shut = list(format(int(soup_shut.find_all("td")[2].string, 16), '030b'))[::-1]
        hatch = list(format(int(soup_hatch.find_all("td")[2].string, 16), '030b'))[::-1]

        self.change = (
            int(shut[23]) + int(shut[26]) +
            int(hatch[19]) + int(hatch[20]) + int(hatch[21])
        )

        self.set_state_label(self.mbs, "Open" if shut[23] == '1' else "Close", shut[23] == '1')
        self.set_state_label(self.dss, "Open" if shut[26] == '1' else "Close", shut[26] == '1')
        self.set_state_label(self.opt, "Open" if hatch[19] == '0' else "Normal Close", hatch[19] == '0')
        self.set_state_label(self.opt2, "Open" if hatch[20] == '0' else "Normal Close", hatch[20] == '0')
        self.set_state_label(self.exp, "Open" if hatch[21] == '0' else "Normal Close", hatch[21] == '0')

        self.update_position()

    # ==========================
    def update_position(self):
        self.monoz.setText(str(self.pm.get_value(self.pmch['mono'])))
        self.gamma.setText(str(self.pm.get_value(self.pmch['gamma'])))

        if self.pm.query("S14") == "R00":
            self.pos_timer.stop()
            self.set_buttons(True)

    # ==========================
    def start_move(self, mono_p, gamma_p):
        try:
            self.set_buttons(False)
            self.pos_timer.start()
            self.pm.amove("A", 1, mono_p)
            self.pm.amove("B", 4, gamma_p)
        except Exception as e:
            self.pos_timer.stop()
            self.set_buttons(True)
            QMessageBox.warning(self, "Error", str(e))

    def to_mono(self):
        if QMessageBox.question(self, "Confirm", "Switch White to Mono Ok?") == QMessageBox.Yes and self.change == 0:
            self.start_move(self.posdic['monoZ_M'], self.posdic['gamma_M'])

    def to_white(self):
        if QMessageBox.question(self, "Confirm", "Switch Mono to White Ok?") == QMessageBox.Yes and self.change == 0:
            self.start_move(self.posdic['monoZ_W'], self.posdic['gamma_W'])


# ==============================
# main
# ==============================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QLabel {
            font-size: 24px;
        }
        QPushButton {
            font-size: 32px;
            min-height: 50px;
            padding: 10px 20px;
        }
    """)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
