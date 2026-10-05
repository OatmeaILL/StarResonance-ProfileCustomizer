# -*- coding: utf-8 -*-
"""图片裁剪编辑组件：选框拖拽、亮度/对比度/饱和度/色温调节、缩放平移"""

from PyQt5.QtWidgets import QLabel, QWidget, QSizePolicy
from PyQt5.QtCore import Qt, QRect, QPoint, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPixmap, QImage, QPainter, QPen
from PIL import Image, ImageEnhance

from .debug import debug_log

# 图片目标尺寸常量
CARD_WIDTH = 468
CARD_HEIGHT = 774
AVATAR_WIDTH = 468
AVATAR_HEIGHT = 468

# 缩略图尺寸范围
THUMB_MIN_SIZE = 120
THUMB_MAX_SIZE = 180

# 选框颜色
SELECTION_COLOR = QColor(0, 180, 255)
SELECTION_PEN_WIDTH = 2
CORNER_PEN_WIDTH = 3
CORNER_LENGTH = 12


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class ImageCropWidget(QWidget):
    """带遮罩和选择框的图片裁剪组件"""

    def __init__(self, target_w, target_h, parent=None):
        super().__init__(parent)
        self.target_w = target_w
        self.target_h = target_h
        self.aspect_ratio = target_w / target_h
        self._pixmap = None
        self._processed_pixmap = None
        self._img_rect = QRect()
        self._sel_rect = QRect()
        self._dragging = False
        self._drag_start = QPoint()
        self._panning = False
        self._pan_last = QPoint()
        self._img_offset = QPoint(0, 0)
        self._brightness = 0
        self._contrast = 0
        self._saturation = 0
        self._temperature = 0
        self._zoom = 1.0
        self._zoom_callback = None
        self._preview_callback = None
        self._dirty = True
        self.setMinimumSize(400, 300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)

    def set_image(self, pixmap):
        self._pixmap = pixmap
        self._dirty = True
        self._img_offset = QPoint(0, 0)
        self._update_layout()
        self._rebuild_processed()
        self.update()
        # 载入图片后立即刷新预览框，无需等待用户拖动
        self._emit_preview()

    def reset_position(self):
        self._zoom = 1.0
        self._img_offset = QPoint(0, 0)
        self._update_layout()
        self.update()
        self._emit_preview()

    def reset_adjustments(self):
        self._brightness = 0
        self._contrast = 0
        self._saturation = 0
        self._temperature = 0
        self._dirty = True
        self._rebuild_processed()
        self.update()
        self._emit_preview()

    def _set_adjustment(self, attr, val):
        """通用属性设置：检测变化后触发重绘和预览"""
        if getattr(self, attr) != val:
            setattr(self, attr, val)
            self._dirty = True
            self._rebuild_processed()
            self.update()
            self._emit_preview()

    def set_brightness(self, val):
        self._set_adjustment('_brightness', val)

    def set_contrast(self, val):
        self._set_adjustment('_contrast', val)

    def set_saturation(self, val):
        self._set_adjustment('_saturation', val)

    def set_temperature(self, val):
        self._set_adjustment('_temperature', val)

    def set_zoom(self, val):
        val = max(0.01, min(3.0, val))
        if abs(self._zoom - val) < 0.001:
            return
        sel_img_rx = None
        sel_img_ry = None
        if (not self._img_rect.isEmpty() and self._img_rect.width() > 0
                and self._img_rect.height() > 0 and not self._sel_rect.isEmpty()):
            sel_cx = self._sel_rect.center().x()
            sel_cy = self._sel_rect.center().y()
            sel_img_rx = (sel_cx - self._img_rect.x()) / self._img_rect.width()
            sel_img_ry = (sel_cy - self._img_rect.y()) / self._img_rect.height()
        self._zoom = val
        if sel_img_rx is not None:
            base_scaled = self._pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            zoom_w = int(base_scaled.width() * self._zoom)
            zoom_h = int(base_scaled.height() * self._zoom)
            default_x = (self.width() - zoom_w) // 2
            default_y = (self.height() - zoom_h) // 2
            sel_cx = self._sel_rect.center().x()
            sel_cy = self._sel_rect.center().y()
            point_x = default_x + sel_img_rx * zoom_w
            point_y = default_y + sel_img_ry * zoom_h
            self._img_offset.setX(int(sel_cx - point_x))
            self._img_offset.setY(int(sel_cy - point_y))
        self._update_img_rect()
        self.update()
        self._emit_preview()
        if self._zoom_callback:
            self._zoom_callback(self._zoom)

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        step = 0.01
        if delta > 0:
            new_zoom = min(self._zoom + step, 3.0)
        else:
            new_zoom = max(self._zoom - step, 0.01)
        self.set_zoom(new_zoom)
        event.accept()

    def _rebuild_processed(self):
        if not self._pixmap or not self._dirty:
            return
        self._dirty = False
        if self._brightness == 0 and self._contrast == 0 and self._saturation == 0 and self._temperature == 0:
            self._processed_pixmap = QPixmap(self._pixmap)
            return
        debug_log(f"_rebuild_processed: brightness={self._brightness}, contrast={self._contrast}, saturation={self._saturation}, temperature={self._temperature}")
        img = self._pixmap.toImage().convertToFormat(QImage.Format_RGBA8888)
        w, h = img.width(), img.height()
        buf = img.bits()
        buf.setsize(img.sizeInBytes())
        pil_img = Image.frombytes("RGBA", (w, h), bytes(buf))
        if self._brightness != 0:
            pil_img = ImageEnhance.Brightness(pil_img).enhance(1.0 + self._brightness / 100.0)
        if self._contrast != 0:
            pil_img = ImageEnhance.Contrast(pil_img).enhance(1.0 + self._contrast / 100.0)
        if self._saturation != 0:
            pil_img = ImageEnhance.Color(pil_img).enhance(1.0 + self._saturation / 100.0)
        if self._temperature != 0:
            r, g, b, a = pil_img.split()
            shift = self._temperature / 100.0 * 30
            r = r.point(lambda x: min(255, max(0, int(x + shift))))
            b = b.point(lambda x: min(255, max(0, int(x - shift))))
            pil_img = Image.merge("RGBA", (r, g, b, a))
        data = pil_img.tobytes()
        qimg = QImage(data, pil_img.width, pil_img.height, pil_img.width * 4, QImage.Format_RGBA8888)
        self._processed_pixmap = QPixmap.fromImage(qimg)

    def _update_img_rect(self):
        if not self._pixmap:
            return
        base_scaled = self._pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        zoom_w = int(base_scaled.width() * self._zoom)
        zoom_h = int(base_scaled.height() * self._zoom)
        x = (self.width() - zoom_w) // 2 + self._img_offset.x()
        y = (self.height() - zoom_h) // 2 + self._img_offset.y()
        self._img_rect = QRect(x, y, zoom_w, zoom_h)

    def _update_layout(self):
        if not self._pixmap:
            return
        self._update_img_rect()
        img_w = self._pixmap.width()
        img_h = self._pixmap.height()
        scale_x = self.target_w / img_w if img_w > 0 else 1.0
        scale_y = self.target_h / img_h if img_h > 0 else 1.0
        scale = min(scale_x, scale_y, 1.0)
        base_scaled = self._pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        sel_w = int(base_scaled.width() * scale)
        sel_h = int(sel_w / self.aspect_ratio)
        if sel_h > base_scaled.height():
            sel_h = base_scaled.height()
            sel_w = int(sel_h * self.aspect_ratio)
        sx = (self.width() - sel_w) // 2
        sy = (self.height() - sel_h) // 2
        self._sel_rect = QRect(sx, sy, sel_w, sel_h)

    def resizeEvent(self, event):
        self._update_layout()
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self._sel_rect.contains(event.pos()):
                self._dragging = True
                self._drag_start = event.pos() - self._sel_rect.topLeft()
                self.setCursor(Qt.SizeAllCursor)
            else:
                self._panning = True
                self._pan_last = event.pos()
                self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if self._dragging:
            new_top_left = event.pos() - self._drag_start
            new_top_left.setX(max(self._img_rect.x(), min(new_top_left.x(),
                self._img_rect.right() - self._sel_rect.width())))
            new_top_left.setY(max(self._img_rect.y(), min(new_top_left.y(),
                self._img_rect.bottom() - self._sel_rect.height())))
            self._sel_rect.moveTopLeft(new_top_left)
            self.update()
            self._emit_preview()
        elif self._panning:
            delta = event.pos() - self._pan_last
            self._img_offset += delta
            self._pan_last = event.pos()
            self._update_img_rect()
            self._clamp_offset()
            self.update()
            self._emit_preview()
        else:
            if self._sel_rect.contains(event.pos()):
                self.setCursor(Qt.SizeAllCursor)
            else:
                self.setCursor(Qt.OpenHandCursor)

    def mouseReleaseEvent(self, event):
        if self._dragging:
            self._dragging = False
            self.setCursor(Qt.SizeAllCursor if self._sel_rect.contains(event.pos()) else Qt.OpenHandCursor)
        if self._panning:
            self._panning = False
            self.setCursor(Qt.OpenHandCursor)

    def _clamp_offset(self):
        if not self._pixmap or self._sel_rect.isEmpty():
            return
        base_scaled = self._pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        zoom_w = int(base_scaled.width() * self._zoom)
        zoom_h = int(base_scaled.height() * self._zoom)
        default_x = (self.width() - zoom_w) // 2
        default_y = (self.height() - zoom_h) // 2
        sel_cx = self._sel_rect.center().x()
        sel_cy = self._sel_rect.center().y()
        margin = min(self._sel_rect.width(), self._sel_rect.height()) // 2
        min_ox = sel_cx - default_x - zoom_w + margin
        max_ox = sel_cx - default_x - margin
        min_oy = sel_cy - default_y - zoom_h + margin
        max_oy = sel_cy - default_y - margin
        ox = max(min_ox, min(max_ox, self._img_offset.x()))
        oy = max(min_oy, min(max_oy, self._img_offset.y()))
        self._img_offset = QPoint(int(ox), int(oy))
        self._update_img_rect()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(0x2D, 0x2D, 0x2D))
        if not self._processed_pixmap:
            painter.end()
            return
        scaled = self._processed_pixmap.scaled(self._img_rect.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        painter.drawPixmap(self._img_rect, scaled)
        overlay = QColor(0, 0, 0, 128)
        inter = self._sel_rect.intersected(self._img_rect)
        if inter.isEmpty():
            painter.fillRect(self._img_rect, overlay)
        else:
            top_h = inter.top() - self._img_rect.top()
            if top_h > 0:
                painter.fillRect(QRect(self._img_rect.x(), self._img_rect.y(),
                                       self._img_rect.width(), top_h), overlay)
            bottom_y = inter.bottom() + 1
            bottom_h = self._img_rect.bottom() - bottom_y + 1
            if bottom_h > 0:
                painter.fillRect(QRect(self._img_rect.x(), bottom_y,
                                       self._img_rect.width(), bottom_h), overlay)
            left_w = inter.left() - self._img_rect.left()
            if left_w > 0:
                painter.fillRect(QRect(self._img_rect.x(), inter.y(),
                                       left_w, inter.height()), overlay)
            right_x = inter.right() + 1
            right_w = self._img_rect.right() - right_x + 1
            if right_w > 0:
                painter.fillRect(QRect(right_x, inter.y(),
                                       right_w, inter.height()), overlay)
        pen = QPen(SELECTION_COLOR, SELECTION_PEN_WIDTH, Qt.DashLine)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(self._sel_rect)
        pen2 = QPen(SELECTION_COLOR, CORNER_PEN_WIDTH)
        painter.setPen(pen2)
        r = self._sel_rect
        painter.drawLine(r.topLeft(), r.topLeft() + QPoint(CORNER_LENGTH, 0))
        painter.drawLine(r.topLeft(), r.topLeft() + QPoint(0, CORNER_LENGTH))
        painter.drawLine(r.topRight(), r.topRight() + QPoint(-CORNER_LENGTH, 0))
        painter.drawLine(r.topRight(), r.topRight() + QPoint(0, CORNER_LENGTH))
        painter.drawLine(r.bottomLeft(), r.bottomLeft() + QPoint(CORNER_LENGTH, 0))
        painter.drawLine(r.bottomLeft(), r.bottomLeft() + QPoint(0, -CORNER_LENGTH))
        painter.drawLine(r.bottomRight(), r.bottomRight() + QPoint(-CORNER_LENGTH, 0))
        painter.drawLine(r.bottomRight(), r.bottomRight() + QPoint(0, -CORNER_LENGTH))
        painter.setPen(QColor(200, 200, 200))
        painter.setFont(QFont("Microsoft YaHei", 9))
        label = f"{self.target_w}x{self.target_h}"
        # 兼容旧版 PyQt5（< 5.11）：horizontalAdvance 不存在时回退到 width
        fm = painter.fontMetrics()
        try:
            label_w = fm.horizontalAdvance(label)
        except AttributeError:
            label_w = fm.width(label)
        painter.drawText(r.x() + (r.width() - label_w) // 2,
                         r.y() - 5, label)
        painter.end()

    def get_cropped_image(self):
        if not self._pixmap:
            return None
        inter = self._sel_rect.intersected(self._img_rect)
        if inter.isEmpty():
            debug_log("get_cropped_image: 选区与图片无交集")
            return None
        debug_log(f"get_cropped_image: sel_rect={self._sel_rect}, img_rect={self._img_rect}, inter={inter}, target={self.target_w}x{self.target_h}")
        img = self._pixmap.toImage().convertToFormat(QImage.Format_RGBA8888)
        w, h = img.width(), img.height()
        buf = img.bits()
        buf.setsize(img.sizeInBytes())
        pil_img = Image.frombytes("RGBA", (w, h), bytes(buf))
        if self._brightness != 0:
            pil_img = ImageEnhance.Brightness(pil_img).enhance(1.0 + self._brightness / 100.0)
        if self._contrast != 0:
            pil_img = ImageEnhance.Contrast(pil_img).enhance(1.0 + self._contrast / 100.0)
        if self._saturation != 0:
            pil_img = ImageEnhance.Color(pil_img).enhance(1.0 + self._saturation / 100.0)
        if self._temperature != 0:
            r, g, b, a = pil_img.split()
            shift = self._temperature / 100.0 * 30
            r = r.point(lambda x: min(255, max(0, int(x + shift))))
            b = b.point(lambda x: min(255, max(0, int(x - shift))))
            pil_img = Image.merge("RGBA", (r, g, b, a))
        scale_x = pil_img.width / self._img_rect.width()
        scale_y = pil_img.height / self._img_rect.height()
        crop_x = int((inter.x() - self._img_rect.x()) * scale_x)
        crop_y = int((inter.y() - self._img_rect.y()) * scale_y)
        crop_w = int(inter.width() * scale_x)
        crop_h = int(inter.height() * scale_y)
        crop_x = max(0, crop_x)
        crop_y = max(0, crop_y)
        crop_w = min(crop_w, pil_img.width - crop_x)
        crop_h = min(crop_h, pil_img.height - crop_y)
        if crop_w <= 0 or crop_h <= 0:
            return None
        cropped = pil_img.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_h))
        canvas = Image.new("RGBA", (self.target_w, self.target_h), (0, 0, 0, 0))
        paste_x = int((inter.x() - self._sel_rect.x()) / self._sel_rect.width() * self.target_w)
        paste_y = int((inter.y() - self._sel_rect.y()) / self._sel_rect.height() * self.target_h)
        paste_w = max(1, int(inter.width() / self._sel_rect.width() * self.target_w))
        paste_h = max(1, int(inter.height() / self._sel_rect.height() * self.target_h))
        resized_part = cropped.resize((paste_w, paste_h), Image.LANCZOS)
        canvas.paste(resized_part, (paste_x, paste_y))
        return canvas

    def has_image(self):
        """是否已载入图片"""
        return self._pixmap is not None and not self._pixmap.isNull()

    def _emit_preview(self):
        if self._preview_callback and self._pixmap:
            self._preview_callback(self.get_preview_pixmap())

    def get_preview_pixmap(self):
        if not self._processed_pixmap or self._img_rect.isEmpty():
            return None
        inter = self._sel_rect.intersected(self._img_rect)
        if inter.isEmpty():
            return None
        scale_x = self._processed_pixmap.width() / self._img_rect.width()
        scale_y = self._processed_pixmap.height() / self._img_rect.height()
        sx = int((inter.x() - self._img_rect.x()) * scale_x)
        sy = int((inter.y() - self._img_rect.y()) * scale_y)
        sw = int(inter.width() * scale_x)
        sh = int(inter.height() * scale_y)
        sx = max(0, sx)
        sy = max(0, sy)
        sw = min(sw, self._processed_pixmap.width() - sx)
        sh = min(sh, self._processed_pixmap.height() - sy)
        if sw <= 0 or sh <= 0:
            return None
        canvas = QPixmap(self.target_w, self.target_h)
        canvas.fill(Qt.transparent)
        painter = QPainter(canvas)
        paste_x = int((inter.x() - self._sel_rect.x()) / self._sel_rect.width() * self.target_w)
        paste_y = int((inter.y() - self._sel_rect.y()) / self._sel_rect.height() * self.target_h)
        paste_w = max(1, int(inter.width() / self._sel_rect.width() * self.target_w))
        paste_h = max(1, int(inter.height() / self._sel_rect.height() * self.target_h))
        cropped = self._processed_pixmap.copy(sx, sy, sw, sh)
        scaled = cropped.scaled(paste_w, paste_h, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        painter.drawPixmap(paste_x, paste_y, scaled)
        painter.end()
        return canvas


def draw_preview_border(pixmap):
    """在预览 pixmap 四周绘制与编辑窗口选框一致的蓝色虚线边框

    框住整个预览画布，即实际导出裁剪的区域（含无图片的透明部分）；
    仅用于显示，不写入导出的图片文件。
    """
    if pixmap is None or pixmap.isNull():
        return pixmap
    rect = pixmap.rect()
    # 内缩 1px 保证 2px 虚线不被 pixmap 边缘裁掉
    if rect.width() > 8 and rect.height() > 8:
        rect = rect.adjusted(1, 1, -1, -1)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    pen = QPen(SELECTION_COLOR, SELECTION_PEN_WIDTH, Qt.DashLine)
    painter.setPen(pen)
    painter.setBrush(Qt.NoBrush)
    painter.drawRect(rect)
    corner_len = max(1, min(CORNER_LENGTH, rect.width() // 3, rect.height() // 3))
    pen2 = QPen(SELECTION_COLOR, CORNER_PEN_WIDTH)
    painter.setPen(pen2)
    painter.drawLine(rect.topLeft(), rect.topLeft() + QPoint(corner_len, 0))
    painter.drawLine(rect.topLeft(), rect.topLeft() + QPoint(0, corner_len))
    painter.drawLine(rect.topRight(), rect.topRight() + QPoint(-corner_len, 0))
    painter.drawLine(rect.topRight(), rect.topRight() + QPoint(0, corner_len))
    painter.drawLine(rect.bottomLeft(), rect.bottomLeft() + QPoint(corner_len, 0))
    painter.drawLine(rect.bottomLeft(), rect.bottomLeft() + QPoint(0, -corner_len))
    painter.drawLine(rect.bottomRight(), rect.bottomRight() + QPoint(-corner_len, 0))
    painter.drawLine(rect.bottomRight(), rect.bottomRight() + QPoint(0, -corner_len))
    painter.end()
    return pixmap
