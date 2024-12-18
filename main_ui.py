
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QTimer, QPointF
import threading
import sys
import math
from logic import VoiceLogic


class VoiceUI(QMainWindow):
    def __init__(self, logic):
        super().__init__()
        self.setWindowTitle("Voice Assistant")
        self.setGeometry(100, 100, 400, 400)
        self.logic = logic

        self.base_radius = 120
        self.wave_points = 60
        self.phase_shift = 0
        self.phase_speed = 0.1

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(50)

        self.audio_thread = threading.Thread(target=self.logic.process_audio)
        self.audio_thread.start()

    def update_ui(self):
        if self.logic.state in ["waiting", "listening", "processing", "executing"]:
            self.phase_shift += self.phase_speed
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center_x, center_y = self.width() // 2, self.height() // 2
        color = self.get_state_color()

        painter.setPen(Qt.NoPen)
        painter.setBrush(color)

        path = self.create_wave_path(center_x, center_y)
        painter.drawPath(path)

    def create_wave_path(self, center_x, center_y):
        from PyQt5.QtGui import QPainterPath
        path = QPainterPath()
        path.moveTo(center_x + self.base_radius, center_y)

        for i in range(self.wave_points + 1):
            angle = 2 * math.pi * i / self.wave_points
            radius = self.base_radius + 10 * math.sin(angle * 3 + self.phase_shift)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            path.lineTo(QPointF(x, y))

        path.closeSubpath()
        return path

    def get_state_color(self):
        if self.logic.state == "waiting":
            return QColor(0, 122, 255, 150)
        elif self.logic.state == "listening":
            return QColor(0, 255, 100, 150)
        elif self.logic.state == "processing":
            return QColor(255, 200, 0, 150)
        elif self.logic.state == "executing":
            return QColor(255, 50, 200, 150)
        else:
            return QColor(0, 0, 0, 0)

    def closeEvent(self, event):
        self.logic.is_running = False
        self.audio_thread.join()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    api_key = "API_KEY_HERE"
    path_to_vosk = "vosk-model-small-ru-0.22"
    logic = VoiceLogic(path_to_vosk, api_key)
    ui = VoiceUI(logic)
    ui.show()
    sys.exit(app.exec_())
#Температура в Троицке, спой песню, открой блокнот, открой браузер, кто ты, ...
