import sys
import cv2
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QComboBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QSlider,
    QSizePolicy, QMessageBox
)
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor, QFont,QIcon
from PyQt5.QtCore import Qt


class ClickableLabel(QLabel):
    """Custom QLabel to handle mouse press events."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.click_callback = None

    def mousePressEvent(self, event):
        if self.click_callback:
            self.click_callback(event)


class AnnotationTool(QMainWindow):
    def __init__(self):
        super().__init__()

        # Video variables
        self.video_path = None
        self.cap = None
        self.current_frame = 0
        self.total_frames = 0

        # Separate lists for action and posture annotations
        self.action_annotations = []  # List of action annotations
        self.posture_annotations = []  # List of posture annotations

        # Current ongoing annotations per pigeon
        self.current_actions = {pigeon: None for pigeon in ['P1', 'P2', 'P3', 'P4']}
        self.current_postures = {pigeon: None for pigeon in ['P1', 'P2', 'P3', 'P4']}

        # Undo stack
        self.undo_stack = []  # Stack to track annotations for undo

        # Pigeons for which we will create timeline bars
        self.pigeons = ['P1', 'P2', 'P3', 'P4']
        self.timeline_bars = {}

        # Dictionary to store bounding boxes and labels for each frame
        # self.frame_annotations[frame_id][pigeon_id] = {
        #   'x': float, 'y': float, 'width': float, 'height': float,
        #   'action_label': str or -1,
        #   'posture_label': str or -1
        # }
        self.frame_annotations = {}

        # Colors for each pigeon (RGB)
        self.pigeon_colors = {
            'P1': (255, 0, 0),    # Red in RGB
            'P2': (0, 255, 0),    # Green in RGB
            'P3': (0, 0, 255),    # Blue in RGB
            'P4': (255, 255, 0)   # Yellow in RGB
        }

        # GUI components
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Pigeon Behavior Annotation Tool')
        self.setFixedSize(1200, 1080)

        # Video display label
        self.video_label = QLabel(self)
        self.video_label.setScaledContents(True)
        self.video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_label.setStyleSheet("border: 1px solid black;")
        self.setWindowIcon(QIcon('icon.ico'))

        # Frame information label
        self.frame_info_label = QLabel("Frame: 0 / 0", self)
        font_info = QFont()
        font_info.setPointSize(12)
        self.frame_info_label.setFont(font_info)

        # Pigeon selection
        self.pigeon_selector = QComboBox(self)
        self.pigeon_selector.addItems(self.pigeons)

        # Behavior selection
        self.behavior_selector = QComboBox(self)
        self.behavior_selector.addItems([
            'Feeding', 'Drinking', 'Grit', 'Grooming', 'Incubation',
            'Feeding_young', 'Walking', 'Spread_wings', 'Kiss',
            'Mating', 'Fighting', 'Inflating_the_crop'
        ])
        self.behavior_selector.currentIndexChanged.connect(self.update_behavior_color)

        # Behavior color display
        self.behavior_color_display = QLabel(self)
        self.behavior_color_display.setFixedSize(50, 20)
        self.behavior_color_display.setStyleSheet("background-color: white; border: 1px solid black;")
        self.update_behavior_color()  # Initialize behavior color display

        # Posture selection
        self.posture_selector = QComboBox(self)
        self.posture_selector.addItems(['Standing', 'Lying_down', 'Tail_up', 'Motion'])
        self.posture_selector.currentIndexChanged.connect(self.update_posture_color)

        # Posture color display
        self.posture_color_display = QLabel(self)
        self.posture_color_display.setFixedSize(50, 20)
        self.posture_color_display.setStyleSheet("background-color: #e3e3e3; border: 1px solid black;")
        self.update_posture_color()  # Initialize posture color display

        # Control buttons
        self.load_button = QPushButton('Load Video', self)
        self.load_button.clicked.connect(self.load_video)

        self.import_annotation_button = QPushButton('Import Annotations', self)
        self.import_annotation_button.clicked.connect(self.import_annotations)

        self.prev_button = QPushButton('Previous Frame', self)
        self.prev_button.clicked.connect(self.prev_frame)

        self.next_button = QPushButton('Next Frame', self)
        self.next_button.clicked.connect(self.next_frame)

        self.start_action_button = QPushButton('Start Action', self)
        self.start_action_button.clicked.connect(self.start_action)

        self.end_action_button = QPushButton('End Action', self)
        self.end_action_button.clicked.connect(self.end_action)

        self.start_posture_button = QPushButton('Start Posture', self)
        self.start_posture_button.clicked.connect(self.start_posture)

        self.end_posture_button = QPushButton('End Posture', self)
        self.end_posture_button.clicked.connect(self.end_posture)

        self.export_button = QPushButton('Export Annotations', self)
        self.export_button.clicked.connect(self.export_annotations)

        self.export_sorted_button = QPushButton('Export Sorted Format', self)
        self.export_sorted_button.clicked.connect(self.export_sorted_annotations)

        # Undo button
        self.undo_button = QPushButton('Undo', self)
        self.undo_button.clicked.connect(self.undo_last_annotation)

        # Video progress bar
        self.progress_slider = QSlider(Qt.Horizontal, self)
        self.progress_slider.sliderMoved.connect(self.slider_moved)

        # Timeline layout for each pigeon
        timeline_layout = QVBoxLayout()
        for pigeon in self.pigeons:
            # Behavior timeline
            row_layout_behavior = QHBoxLayout()
            label_behavior = QLabel(f"{pigeon}_B", self)
            timeline_bar_behavior = ClickableLabel(self)
            timeline_bar_behavior.setFixedHeight(20)
            timeline_bar_behavior.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            timeline_bar_behavior.setStyleSheet("background-color: white; border: 1px solid black;")
            timeline_bar_behavior.click_callback = lambda event, pid=pigeon, bar="B": self.timeline_clicked(event, pid, bar)
            self.timeline_bars[f"{pigeon}_B"] = timeline_bar_behavior

            row_layout_behavior.addWidget(label_behavior)
            row_layout_behavior.addWidget(timeline_bar_behavior)
            timeline_layout.addLayout(row_layout_behavior)

            # Posture timeline
            row_layout_posture = QHBoxLayout()
            label_posture = QLabel(f"{pigeon}_S", self)
            timeline_bar_posture = ClickableLabel(self)
            timeline_bar_posture.setFixedHeight(20)
            timeline_bar_posture.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            timeline_bar_posture.setStyleSheet("background-color: #e3e3e3; border: 1px solid black;")
            timeline_bar_posture.click_callback = lambda event, pid=pigeon, bar="S": self.timeline_clicked(event, pid, bar)
            self.timeline_bars[f"{pigeon}_S"] = timeline_bar_posture

            row_layout_posture.addWidget(label_posture)
            row_layout_posture.addWidget(timeline_bar_posture)
            timeline_layout.addLayout(row_layout_posture)

            # Add a line separator
            line_separator = QLabel(self)
            line_separator.setFixedHeight(1)
            line_separator.setStyleSheet("background-color: black;")
            timeline_layout.addWidget(line_separator)

        # Layout for controls
        controls_layout1 = QHBoxLayout()
        controls_layout1.addWidget(self.load_button)
        controls_layout1.addWidget(self.import_annotation_button)
        controls_layout1.addWidget(QLabel("Select Pigeon:", self))
        controls_layout1.addWidget(self.pigeon_selector)
        controls_layout1.addWidget(self.prev_button)
        controls_layout1.addWidget(self.next_button)
        controls_layout1.addWidget(self.export_button)
        controls_layout1.addWidget(self.export_sorted_button)
        controls_layout1.addWidget(self.undo_button)

        controls_layout2 = QHBoxLayout()
        controls_layout2.addWidget(QLabel("Behavior:", self))
        controls_layout2.addWidget(self.behavior_selector)
        controls_layout2.addWidget(self.behavior_color_display)
        controls_layout2.addWidget(self.start_action_button)
        controls_layout2.addWidget(self.end_action_button)
        controls_layout2.addWidget(QLabel("Posture:", self))
        controls_layout2.addWidget(self.posture_selector)
        controls_layout2.addWidget(self.posture_color_display)
        controls_layout2.addWidget(self.start_posture_button)
        controls_layout2.addWidget(self.end_posture_button)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.video_label)
        main_layout.addWidget(self.frame_info_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.progress_slider)
        main_layout.addLayout(timeline_layout)
        main_layout.addLayout(controls_layout1)
        main_layout.addLayout(controls_layout2)

        # Set main layout
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def get_behavior_color(self, action_label):
        behavior_color_map = {
            'Feeding': (255, 0, 0),           # Red in RGB
            'Drinking': (0, 0, 255),          # Blue in RGB
            'Grit': (0, 255, 0),              # Green in RGB
            'Grooming': (0, 255, 255),        # Cyan in RGB
            'Incubation': (255, 0, 255),      # Magenta in RGB
            'Feeding_young': (255, 255, 0),   # Yellow in RGB
            'Walking': (255, 165, 0),         # Orange in RGB
            'Spread_wings': (238, 130, 238),  # Violet in RGB
            'Kiss': (139, 0, 0),              # Dark Red (Maroon) in RGB
            'Mating': (0, 0, 139),            # Dark Blue in RGB
            'Fighting': (0, 100, 0),          # Dark Green in RGB
            'Inflating_the_crop': (139, 0, 139)  # Dark Cyan (Magenta-like) in RGB
        }
        return behavior_color_map.get(action_label, (255, 255, 255))  # Default to white

    def get_posture_color(self, posture_label):
        posture_color_map = {
            'Standing': (128, 0, 128),  # Purple in RGB
            'Lying_down': (165, 42, 42),  # Brown in RGB
            'Tail_up': (255, 192, 203),   # Pink in RGB
            'Motion': (255, 165, 0)       # Orange in RGB
        }
        return posture_color_map.get(posture_label, (211, 211, 211))  # Default to Light Gray

    def update_behavior_color(self):
        behavior = self.behavior_selector.currentText()
        color_map = {
            'Feeding': "red",
            'Drinking': "blue",
            'Grit': "green",
            'Grooming': "cyan",
            'Incubation': "magenta",
            'Feeding_young': "yellow",
            'Walking': "orange",
            'Spread_wings': "violet",
            'Kiss': "darkred",
            'Mating': "darkblue",
            'Fighting': "darkgreen",
            'Inflating_the_crop': "darkcyan"
        }
        color = color_map.get(behavior, "white")
        self.behavior_color_display.setStyleSheet(f"background-color: {color}; border: 1px solid black;")

    def update_posture_color(self):
        posture = self.posture_selector.currentText()
        color_map = {
            'Standing': "purple",
            'Lying_down': "brown",
            'Tail_up': "pink",
            'Motion': "orange"
        }
        color = color_map.get(posture, "#e3e3e3")
        self.posture_color_display.setStyleSheet(f"background-color: {color}; border: 1px solid black;")

    def load_video(self):
        self.video_path, _ = QFileDialog.getOpenFileName(self, 'Open Video')
        if self.video_path:
            if self.cap:
                self.cap.release()
            self.cap = cv2.VideoCapture(self.video_path)
            if not self.cap.isOpened():
                QMessageBox.critical(self, "Error", "Cannot open video.")
                return

            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.progress_slider.setRange(0, self.total_frames - 1)
            self.current_frame = 0
            self.action_annotations.clear()
            self.posture_annotations.clear()
            self.undo_stack.clear()
            self.current_actions = {pigeon: None for pigeon in self.pigeons}
            self.current_postures = {pigeon: None for pigeon in self.pigeons}
            self.frame_annotations.clear()
            self.update_frame_info()
            self.show_frame()
            self.update_timeline()

    def show_frame(self):
        if not self.cap or not self.cap.isOpened():
            return
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        ret, frame = self.cap.read()
        if not ret:
            QMessageBox.critical(self, "Error", f"Cannot read frame {self.current_frame}.")
            return

        # Do not resize to maintain original aspect ratio and ensure accurate bounding box placement
        # If scaling is necessary, ensure coordinate transformations are handled accordingly
        h, w = frame.shape[:2]

        # Draw bounding boxes if present
        if self.current_frame in self.frame_annotations:
            for pigeon_id, data in self.frame_annotations[self.current_frame].items():
                # Assuming x, y, width, height are normalized left-top coordinates and sizes
                x1 = int(data['x'] * w)
                y1 = int(data['y'] * h)
                x2 = int((data['x'] + data['width']) * w)
                y2 = int((data['y'] + data['height']) * h)

                color_rgb = self.pigeon_colors.get(pigeon_id, (255, 255, 255))  # Get RGB color
                # Convert RGB to BGR for OpenCV
                color_bgr = (color_rgb[2], color_rgb[1], color_rgb[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), color_bgr, 2)

                # Retrieve labels
                action_label = data['action_label']
                posture_label = data['posture_label']

                # Determine text colors based on labels
                action_color_rgb = self.get_behavior_color(action_label) if action_label != -1 else color_rgb
                posture_color_rgb = self.get_posture_color(posture_label) if posture_label != -1 else color_rgb

                # Convert RGB to BGR for OpenCV
                action_color_bgr = (action_color_rgb[2], action_color_rgb[1], action_color_rgb[0]) if action_label != -1 else color_bgr
                posture_color_bgr = (posture_color_rgb[2], posture_color_rgb[1], posture_color_rgb[0]) if posture_label != -1 else color_bgr

                # Set font parameters
                font_scale = 1.0  # Increased from 0.5 to 1.0
                thickness = 2     # Increased from 1 to 2

                # Initialize offset for stacking text
                offset = 25  # Start higher to accommodate larger text

                # Posture label
                if posture_label != -1:
                    pos_text = f"Posture: {posture_label}"
                    (pos_w, pos_h), _ = cv2.getTextSize(pos_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
                    # Ensure text does not go above the frame
                    y_pos = max(y1 - offset, pos_h)
                    # Draw shadow
                    cv2.putText(frame, pos_text, (x1 + 2, y_pos + 2),
                                cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)
                    # Draw main text
                    cv2.putText(frame, pos_text, (x1, y_pos),
                                cv2.FONT_HERSHEY_SIMPLEX, font_scale, posture_color_bgr, thickness, cv2.LINE_AA)
                    offset += pos_h + 10  # Additional spacing

                # Action label
                if action_label != -1:
                    act_text = f"Behavior: {action_label}"
                    (act_w, act_h), _ = cv2.getTextSize(act_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
                    y_pos = max(y1 - offset, act_h)
                    # Draw shadow
                    cv2.putText(frame, act_text, (x1 + 2, y_pos + 2),
                                cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)
                    # Draw main text
                    cv2.putText(frame, act_text, (x1, y_pos),
                                cv2.FONT_HERSHEY_SIMPLEX, font_scale, action_color_bgr, thickness, cv2.LINE_AA)
                    offset += act_h + 10  # Additional spacing

                # ID text placed inside the top-left corner of the bounding box
                id_text = f"ID: {pigeon_id}"
                (id_w, id_h), _ = cv2.getTextSize(id_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
                # Ensure ID text stays within the frame
                x_id = x1 + 5
                y_id = y1 + id_h + 5
                # Draw shadow
                cv2.putText(frame, id_text, (x_id + 2, y_id + 2),
                            cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)
                # Draw main text
                cv2.putText(frame, id_text, (x_id, y_id),
                            cv2.FONT_HERSHEY_SIMPLEX, font_scale, color_bgr, thickness, cv2.LINE_AA)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        qimg = QImage(frame.data, w, h, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qimg))
        self.progress_slider.setValue(self.current_frame)
        self.update_frame_info()

    def update_frame_info(self):
        self.frame_info_label.setText(f"Frame: {self.current_frame} / {self.total_frames}")

    def prev_frame(self):
        if self.current_frame > 0:
            self.current_frame -= 1
            self.show_frame()

    def next_frame(self):
        if self.current_frame < self.total_frames - 1:
            self.current_frame += 1
            self.show_frame()

    def slider_moved(self, position):
        self.current_frame = position
        self.show_frame()
        self.update_timeline()

    def start_action(self):
        pigeon = self.pigeon_selector.currentText()
        behavior = self.behavior_selector.currentText()

        if self.current_actions[pigeon]:
            QMessageBox.warning(self, "Warning", f"Finish the current action annotation for {pigeon} before starting a new one.")
            return

        self.current_actions[pigeon] = {
            'pigeon_id': pigeon,
            'action_label': behavior,
            'start_frame': self.current_frame,
            'end_frame': None
        }
        self.update_timeline()

    def end_action(self):
        pigeon = self.pigeon_selector.currentText()

        if not self.current_actions[pigeon]:
            QMessageBox.warning(self, "Warning", f"No action is currently being annotated for {pigeon}.")
            return

        self.current_actions[pigeon]['end_frame'] = self.current_frame
        annotation = self.current_actions[pigeon].copy()
        annotation['posture_label'] = -1

        self.action_annotations.append(annotation)
        self.undo_stack.append(('action', annotation))

        self.current_actions[pigeon] = None
        self.update_timeline()

    def start_posture(self):
        pigeon = self.pigeon_selector.currentText()
        posture = self.posture_selector.currentText()

        if self.current_postures[pigeon]:
            QMessageBox.warning(self, "Warning", f"Finish the current posture annotation for {pigeon} before starting a new one.")
            return

        self.current_postures[pigeon] = {
            'pigeon_id': pigeon,
            'posture_label': posture,
            'start_frame': self.current_frame,
            'end_frame': None
        }
        self.update_timeline()

    def end_posture(self):
        pigeon = self.pigeon_selector.currentText()

        if not self.current_postures[pigeon]:
            QMessageBox.warning(self, "Warning", f"No posture is currently being annotated for {pigeon}.")
            return

        self.current_postures[pigeon]['end_frame'] = self.current_frame
        annotation = self.current_postures[pigeon].copy()
        annotation['action_label'] = -1

        self.posture_annotations.append(annotation)
        self.undo_stack.append(('posture', annotation))

        self.current_postures[pigeon] = None
        self.update_timeline()

    def import_annotations(self):
        if not self.cap or not self.cap.isOpened():
            QMessageBox.warning(self, "Error", "Please load a video before importing annotations.")
            return

        annotation_path, _ = QFileDialog.getOpenFileName(
            self, 'Open Annotation File', '', 'CSV Files (*.csv)'
        )
        if not annotation_path:
            return

        try:
            imported_annotations = pd.read_csv(annotation_path)
            # Required columns for bounding box visualization
            required_columns = {'frame_id', 'pigeon_id', 'x', 'y', 'width', 'height', 'action_label', 'posture_label'}
            if not required_columns.issubset(imported_annotations.columns):
                QMessageBox.critical(
                    self, "Error",
                    f"The CSV file is missing required columns: {required_columns}\nActual columns: {imported_annotations.columns.tolist()}"
                )
                return

            max_frame_id = imported_annotations['frame_id'].max()
            if max_frame_id >= self.total_frames:
                QMessageBox.critical(
                    self, "Error", "Annotation frame count exceeds the video frame count."
                )
                return

            # Clear existing annotations
            self.action_annotations.clear()
            self.posture_annotations.clear()
            self.undo_stack.clear()
            self.current_actions = {pigeon: None for pigeon in self.pigeons}
            self.current_postures = {pigeon: None for pigeon in self.pigeons}
            self.frame_annotations.clear()

            # Store bounding boxes and labels
            for _, row in imported_annotations.iterrows():
                f_id = int(row['frame_id'])
                pigeon_id = row['pigeon_id']
                a_label = row['action_label']
                p_label = row['posture_label']
                x = float(row['x'])
                y = float(row['y'])
                w = float(row['width'])
                h = float(row['height'])

                if f_id not in self.frame_annotations:
                    self.frame_annotations[f_id] = {}
                self.frame_annotations[f_id][pigeon_id] = {
                    'x': x,
                    'y': y,
                    'width': w,
                    'height': h,
                    'action_label': a_label,
                    'posture_label': p_label
                }

            # Merge consecutive annotations for timeline display
            for pigeon in self.pigeons:
                pigeon_data = imported_annotations[imported_annotations['pigeon_id'] == pigeon].sort_values('frame_id')
                # Merge actions
                pigeon_actions = pigeon_data[pigeon_data['action_label'] != -1]
                if not pigeon_actions.empty:
                    grouped_actions = self.merge_consecutive_annotations(pigeon_actions, 'action_label')
                    for group in grouped_actions:
                        annotation = {
                            'pigeon_id': pigeon,
                            'action_label': group['action_label'],
                            'start_frame': group['start_frame'],
                            'end_frame': group['end_frame'],
                            'posture_label': -1
                        }
                        self.action_annotations.append(annotation)
                        self.undo_stack.append(('action', annotation))

                # Merge postures
                pigeon_postures = pigeon_data[pigeon_data['posture_label'] != -1]
                if not pigeon_postures.empty:
                    grouped_postures = self.merge_consecutive_annotations(pigeon_postures, 'posture_label')
                    for group in grouped_postures:
                        annotation = {
                            'pigeon_id': pigeon,
                            'posture_label': group['posture_label'],
                            'start_frame': group['start_frame'],
                            'end_frame': group['end_frame'],
                            'action_label': -1
                        }
                        self.posture_annotations.append(annotation)
                        self.undo_stack.append(('posture', annotation))

            QMessageBox.information(self, "Success", "Annotations imported successfully.")
            self.update_timeline()
            self.show_frame()

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load annotations: {str(e)}')

    def merge_consecutive_annotations(self, df, label_column):
        grouped = []
        current_label = None
        start_frame = None
        end_frame = None

        for _, row in df.iterrows():
            label = row[label_column]
            frame = row['frame_id']
            if label != current_label:
                if current_label is not None:
                    grouped.append({
                        label_column: current_label,
                        'start_frame': start_frame,
                        'end_frame': end_frame
                    })
                current_label = label
                start_frame = frame
                end_frame = frame
            else:
                end_frame = frame

        if current_label is not None:
            grouped.append({
                label_column: current_label,
                'start_frame': start_frame,
                'end_frame': end_frame
            })
        return grouped

    def update_timeline(self):
        for pigeon in self.pigeons:
            timeline_bar_behavior = self.timeline_bars[f"{pigeon}_B"]
            timeline_bar_posture = self.timeline_bars[f"{pigeon}_S"]

            behavior_width = timeline_bar_behavior.width()
            behavior_height = timeline_bar_behavior.height()
            posture_width = timeline_bar_posture.width()
            posture_height = timeline_bar_posture.height()

            timeline_image_behavior = QImage(behavior_width, behavior_height, QImage.Format_RGB32)
            timeline_image_behavior.fill(Qt.white)

            timeline_image_posture = QImage(posture_width, posture_height, QImage.Format_RGB32)
            timeline_image_posture.fill(QColor(211, 211, 211))

            behavior_colors = [QColor(255, 255, 255)] * self.total_frames  # White
            posture_colors = [QColor(211, 211, 211)] * self.total_frames  # Light Gray

            # Apply action annotations
            for annotation in self.action_annotations:
                if annotation['pigeon_id'] != pigeon:
                    continue
                start = annotation['start_frame']
                end = annotation['end_frame']
                color_rgb = self.get_behavior_color(annotation['action_label'])
                color_qcolor = QColor(*color_rgb)  # Correct RGB order
                for frame in range(start, end + 1):
                    if 0 <= frame < self.total_frames:
                        behavior_colors[frame] = color_qcolor

            # Apply posture annotations
            for annotation in self.posture_annotations:
                if annotation['pigeon_id'] != pigeon:
                    continue
                start = annotation['start_frame']
                end = annotation['end_frame']
                color_rgb = self.get_posture_color(annotation['posture_label'])
                color_qcolor = QColor(*color_rgb)  # Correct RGB order
                for frame in range(start, end + 1):
                    if 0 <= frame < self.total_frames:
                        posture_colors[frame] = color_qcolor

            # Apply current ongoing action
            current_action = self.current_actions[pigeon]
            if current_action:
                start = current_action['start_frame']
                if 0 <= start < self.total_frames:
                    behavior_colors[start] = QColor("black")
                action_color_rgb = self.get_behavior_color(current_action['action_label'])
                action_color_qcolor = QColor(*action_color_rgb)
                for frame in range(start + 1, self.current_frame + 1):
                    if 0 <= frame < self.total_frames:
                        behavior_colors[frame] = action_color_qcolor

            # Apply current ongoing posture
            current_posture = self.current_postures[pigeon]
            if current_posture:
                start = current_posture['start_frame']
                if 0 <= start < self.total_frames:
                    posture_colors[start] = QColor("black")
                posture_color_rgb = self.get_posture_color(current_posture['posture_label'])
                posture_color_qcolor = QColor(*posture_color_rgb)
                for frame in range(start + 1, self.current_frame + 1):
                    if 0 <= frame < self.total_frames:
                        posture_colors[frame] = posture_color_qcolor

            # Draw behavior timeline
            painter_behavior = QPainter(timeline_image_behavior)
            for frame in range(self.total_frames):
                x = int(frame / self.total_frames * behavior_width)
                if x >= behavior_width:
                    x = behavior_width - 1
                painter_behavior.setPen(Qt.NoPen)
                painter_behavior.setBrush(behavior_colors[frame])
                painter_behavior.drawRect(x, 0, 1, behavior_height)
            painter_behavior.end()

            # Draw posture timeline
            painter_posture = QPainter(timeline_image_posture)
            for frame in range(self.total_frames):
                x = int(frame / self.total_frames * posture_width)
                if x >= posture_width:
                    x = posture_width - 1
                painter_posture.setPen(Qt.NoPen)
                painter_posture.setBrush(posture_colors[frame])
                painter_posture.drawRect(x, 0, 1, posture_height)
            painter_posture.end()

            # Update QLabel display
            timeline_bar_behavior.setPixmap(QPixmap.fromImage(timeline_image_behavior))
            timeline_bar_posture.setPixmap(QPixmap.fromImage(timeline_image_posture))

    def undo_last_annotation(self):
        if self.undo_stack:
            annotation_type, last_annotation = self.undo_stack.pop()
            pigeon_id = last_annotation['pigeon_id']
            if annotation_type == 'action':
                if last_annotation in self.action_annotations:
                    self.action_annotations.remove(last_annotation)
            elif annotation_type == 'posture':
                if last_annotation in self.posture_annotations:
                    self.posture_annotations.remove(last_annotation)
            QMessageBox.information(self, "Undo", "Last annotation removed.")
            self.update_timeline()
            self.show_frame()
        else:
            QMessageBox.warning(self, "Undo", "No annotation to undo.")

    def export_annotations(self):
        save_path, _ = QFileDialog.getSaveFileName(
            self, 'Save Annotations', '', 'CSV Files (*.csv)'
        )
        if save_path:
            try:
                combined_annotations = []
                for annotation in self.action_annotations:
                    combined_annotations.append({
                        'frame_id': annotation['start_frame'],
                        'pigeon_id': annotation['pigeon_id'],
                        'action_label': annotation['action_label'],
                        'posture_label': -1,
                        'x': -1,
                        'y': -1,
                        'width': -1,
                        'height': -1
                    })
                for annotation in self.posture_annotations:
                    combined_annotations.append({
                        'frame_id': annotation['start_frame'],
                        'pigeon_id': annotation['pigeon_id'],
                        'action_label': -1,
                        'posture_label': annotation['posture_label'],
                        'x': -1,
                        'y': -1,
                        'width': -1,
                        'height': -1
                    })
                df = pd.DataFrame(combined_annotations, columns=['frame_id', 'pigeon_id', 'action_label', 'posture_label', 'x', 'y', 'width', 'height'])
                df.to_csv(save_path, index=False)
                QMessageBox.information(self, 'Success', 'Annotations saved successfully.')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to save annotations: {str(e)}')

    def export_sorted_annotations(self):
        save_path, _ = QFileDialog.getSaveFileName(
            self, 'Save Sorted Annotations', '', 'CSV Files (*.csv)'
        )
        if save_path:
            try:
                sorted_annotations = []
                for frame_id in range(self.total_frames):
                    for pigeon in self.pigeons:
                        action_label = -1
                        posture_label = -1
                        for annotation in self.action_annotations:
                            if annotation['pigeon_id'] == pigeon and annotation['start_frame'] <= frame_id <= annotation['end_frame']:
                                action_label = annotation['action_label']
                                break
                        for annotation in self.posture_annotations:
                            if annotation['pigeon_id'] == pigeon and annotation['start_frame'] <= frame_id <= annotation['end_frame']:
                                posture_label = annotation['posture_label']
                                break
                        # If bounding boxes are needed, they should be included here.
                        # Currently, only action and posture labels are exported.
                        sorted_annotations.append({
                            'frame_id': frame_id,
                            'pigeon_id': pigeon,
                            'action_label': action_label,
                            'posture_label': posture_label,
                            'x': -1,
                            'y': -1,
                            'width': -1,
                            'height': -1
                        })
                df_sorted = pd.DataFrame(sorted_annotations, columns=['frame_id', 'pigeon_id', 'action_label', 'posture_label', 'x', 'y', 'width', 'height'])
                df_sorted.to_csv(save_path, index=False)
                QMessageBox.information(self, 'Success', 'Sorted annotations saved successfully.')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to save sorted annotations: {str(e)}')

    def timeline_clicked(self, event, pigeon_id, bar_type):
        timeline_label = self.timeline_bars[f"{pigeon_id}_{bar_type}"]
        click_x = event.pos().x()
        total_width = timeline_label.width()
        frame_clicked = int(click_x / total_width * self.total_frames)

        found_annotation = False

        if bar_type == "B":
            for annotation in self.action_annotations:
                if annotation['pigeon_id'] == pigeon_id:
                    if annotation['start_frame'] <= frame_clicked <= annotation['end_frame']:
                        QMessageBox.information(
                            self, "Annotation Info",
                            f"Pigeon: {pigeon_id}\n"
                            f"Type: Behavior\n"
                            f"Label: {annotation['action_label']}\n"
                            f"Start Frame: {annotation['start_frame']}\n"
                            f"End Frame: {annotation['end_frame']}"
                        )
                        found_annotation = True
                        break
            current_action = self.current_actions[pigeon_id]
            if not found_annotation and current_action:
                if current_action['start_frame'] <= frame_clicked <= self.current_frame:
                    QMessageBox.information(
                        self, "Annotation Info",
                        f"Pigeon: {pigeon_id}\n"
                        f"Type: Behavior (Ongoing)\n"
                        f"Label: {current_action['action_label']}\n"
                        f"Start Frame: {current_action['start_frame']}\n"
                        f"End Frame: {self.current_frame}"
                    )
                    found_annotation = True

        elif bar_type == "S":
            for annotation in self.posture_annotations:
                if annotation['pigeon_id'] == pigeon_id:
                    if annotation['start_frame'] <= frame_clicked <= annotation['end_frame']:
                        QMessageBox.information(
                            self, "Annotation Info",
                            f"Pigeon: {pigeon_id}\n"
                            f"Type: Posture\n"
                            f"Label: {annotation['posture_label']}\n"
                            f"Start Frame: {annotation['start_frame']}\n"
                            f"End Frame: {annotation['end_frame']}"
                        )
                        found_annotation = True
                        break
            current_posture = self.current_postures[pigeon_id]
            if not found_annotation and current_posture:
                if current_posture['start_frame'] <= frame_clicked <= self.current_frame:
                    QMessageBox.information(
                        self, "Annotation Info",
                        f"Pigeon: {pigeon_id}\n"
                        f"Type: Posture (Ongoing)\n"
                        f"Label: {current_posture['posture_label']}\n"
                        f"Start Frame: {current_posture['start_frame']}\n"
                        f"End Frame: {self.current_frame}"
                    )
                    found_annotation = True

        if not found_annotation:
            QMessageBox.information(self, "Annotation Info", "No annotation found for this position.")

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_D:
            self.next_frame()
        elif key == Qt.Key_S:
            self.prev_frame()
        elif key == Qt.Key_Z and event.modifiers() == Qt.ControlModifier:
            self.undo_last_annotation()
        elif key == Qt.Key_1:
            self.pigeon_selector.setCurrentIndex(0)
        elif key == Qt.Key_2:
            self.pigeon_selector.setCurrentIndex(1)
        elif key == Qt.Key_3:
            self.pigeon_selector.setCurrentIndex(2)
        elif key == Qt.Key_4:
            self.pigeon_selector.setCurrentIndex(3)


def main():
    app = QApplication(sys.argv)
    ex = AnnotationTool()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
