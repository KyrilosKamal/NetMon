"""
Styled charts for NetMon using pyqtgraph.
"""
import pyqtgraph as pg
from PySide6.QtGui import QColor, QLinearGradient, QBrush

class ModernChart(pg.PlotWidget):
    def __init__(self, title: str, color: str = "#00d9ff", parent=None):
        super().__init__(parent)
        self.setBackground('transparent')
        self.setTitle(title, color='#ffffff', size='12pt')
        self.showGrid(x=True, y=True, alpha=0.1)
        
        # Axis styling
        self.getAxis('left').setPen(pg.mkPen(color='#ffffff', width=1))
        self.getAxis('bottom').setPen(pg.mkPen(color='#ffffff', width=1))
        
        self.curve = self.plot(pen=pg.mkPen(color=color, width=2))
        
        # Fill under the curve with a gradient
        fill_color = QColor(color)
        fill_color.setAlpha(30)
        self.curve.setFillBrush(fill_color)
        self.curve.setFillLevel(0)

    def update_data(self, data):
        self.curve.setData(data)
