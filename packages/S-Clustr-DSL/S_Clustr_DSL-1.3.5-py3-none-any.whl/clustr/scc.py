#!/usr/bin/python3
# @Мартин.
import sys
import re
import os
import random
import string
from collections import Counter, deque
import json
import base64
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton,
    QWidget, QLabel, QComboBox, QCheckBox, QLineEdit, QMessageBox,
    QAction, QFileDialog, QMenuBar
)
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt5.QtCore import QRegularExpression, Qt
from clustr_lib.aes import S_Clustr_AES_CBC
import datetime
from collections import deque

class Compile:
    def __init__(self):
        self.map = {'RUN': 'RUN', 'STOP': 'STOP', 'TIME': 'TIME','FOR':'FOR'}
        self.code = {}

    def run(self, code):
        self.code = self.__check_json(code)
        if not self.code:
            return "Payload malformed"

        return self.__EIP_MAIN()

    def __call_function(self, function_name, args):
        if function_name not in self.code:
            return f"Function call failed, function '{function_name}' does not exist"

        func_info = self.code[function_name]
        
        if len(args) != len(func_info['args']):
            return "Incorrect number of arguments"
        
        if any(isinstance(arg, str) and arg.isdigit() for arg in func_info['args']):
            return "Argument names cannot be numeric"
        
        var = dict(zip(func_info['args'], args))

        queue = deque(func_info['eip'])
        while queue:
            eip = queue.popleft()
            if len(eip.split(':')) != 2:
                return "Incorrect assignment operation"

            k, v = eip.split(':')
            v = v.split(',')

            if 'CALL' in k:
                called_function = k.replace('CALL-', '')
                if called_function in self.code:
                    if called_function == 'MAIN':
                        return "Main function cannot be called within other functions"
                    result = self.__call_function(called_function, v)
                    if result is not True:
                        return result
                else:
                    return f"Function call failed, function '{called_function}' does not exist"
            elif k in self.map:
                continue
            else:
                return f"Severe warning: illegal function '{k}'"

        return True

    def __check_json(self, data):
        try:
            result = json.loads(data)
            if isinstance(result, dict):
                return result
            else:
                return False
        except json.JSONDecodeError:
            return False

    def __EIP_MAIN(self):
        if 'MAIN' not in self.code:
            return "Main function does not exist"

        queue = deque(self.code['MAIN']['eip'])
        while queue:
            eip = queue.popleft()
            if len(eip.split(':')) != 2:
                return "Incorrect assignment operation"

            k, v = eip.split(':')
            v = v.split(',')

            if 'CALL' in k:
                function_name = k.replace('CALL-', '')
                if function_name in self.code:
                    if function_name == 'MAIN':
                        return "Main function cannot be called within other functions"
                    result = self.__call_function(function_name, v)
                    if result is not True:
                        return result
                else:
                    return f"Function call failed, function '{function_name}' does not exist"
            elif k in self.map:
                continue
            else:
                return f"Severe warning: illegal function '{k}'"

        return True


class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("green"))

        self.comment_rules = [
            (QRegularExpression('//.*'), self.comment_format),
            (QRegularExpression('/\*.*?\*/'), self.comment_format)
        ]

    def highlightBlock(self, text):
        for pattern, format in self.comment_rules:
            index = pattern.match(text).capturedStart()
            while index >= 0:
                length = pattern.match(text).capturedLength()
                self.setFormat(index, length, format)
                index = pattern.match(text, index + length).capturedStart()


class CompilerInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.aes = S_Clustr_AES_CBC()
        self.compiler = Compile()  

        self.setWindowTitle("S-Clustr(Simple) @ Maptnh.")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.fontSizeComboBox = QComboBox(self)
        font_sizes = ['8', '10', '12', '14', '16', '18', '20']
        self.fontSizeComboBox.addItems(font_sizes)
        self.fontSizeComboBox.setCurrentText('18') 
        self.fontSizeComboBox.currentTextChanged.connect(self.change_font_size)
        layout.addWidget(self.fontSizeComboBox)

        self.randomKeyCheckBox = QCheckBox("Generate Random Key", self)
        self.randomKeyCheckBox.stateChanged.connect(self.toggle_key_input)
        layout.addWidget(self.randomKeyCheckBox)

        self.keyInput = QLineEdit(self)
        self.keyInput.setPlaceholderText("Enter a key (must be > 6 characters)")
        layout.addWidget(self.keyInput)

        self.toggle_key_input(Qt.Unchecked)

        self.codeEditor = QTextEdit(self)
        self.codeEditor.setPlaceholderText("Enter your code here...")
        layout.addWidget(self.codeEditor)

        self.outputLabel = QLabel("Output:", self)
        layout.addWidget(self.outputLabel)
        self.outputArea = QTextEdit(self)
        self.outputArea.setReadOnly(True)
        layout.addWidget(self.outputArea)

        self.compileButton = QPushButton("Compile", self)
        self.compileButton.clicked.connect(self.compile_code)
        layout.addWidget(self.compileButton)

        self.formatButton = QPushButton("Format Code", self)
        self.formatButton.clicked.connect(self.format_code)
        layout.addWidget(self.formatButton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.set_default_font_size(18)

        template_code = """ 
DEF MAIN:
    RUN:1-1
    TIME:1000
    STOP:1-1
END"""
        self.codeEditor.setText(template_code)

        self.highlighter = SyntaxHighlighter(self.codeEditor.document())

        # Create File menu
        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")

        open_action = QAction("&Open", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("&Save", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save &As", self)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "SCC Files (*.scc);;All Files (*)")
        if file_name:
            with open(file_name, 'r') as file:
                self.codeEditor.setText(file.read())

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "SCC Files (*.scc);;All Files (*)")
        if file_name:
            if not file_name.endswith('.scc'):
                file_name += '.scc'
            with open(file_name, 'w') as file:
                file.write(self.codeEditor.toPlainText())

    def save_file_as(self):
        self.save_file()

    def set_default_font_size(self, size):
        font_code = self.codeEditor.font()
        font_code.setPointSize(size)
        self.codeEditor.setFont(font_code)

        font_output = self.outputArea.font()
        font_output.setPointSize(size)
        self.outputArea.setFont(font_output)

    def compile_code(self):
        self.format_code()

        code = self.codeEditor.toPlainText().strip()

        if self.randomKeyCheckBox.isChecked():
            key = self.generate_random_key()
        else:
            key = self.keyInput.text().strip()
            if len(key) <= 6:
                self.outputArea.setText("Error: Key must be greater than 6 characters.")
                return
        result = self.convert_to_json(code)
        if result:
            validation_result = self.compiler.run(result)
            if validation_result is not True:
                self.outputArea.setText(f"Error in code format: {validation_result}")
                return
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            output_path = f'./sccopt/{timestamp}.clustr'
            self.outputArea.setText(f"Compilation successful!\nOutput Path: {output_path}\nKey: {key}")
            print(result)
            with open(output_path, 'wb') as f:
                f.write(self.aes.aes_cbc_encode(key, result).encode('utf-8'))

            QMessageBox.information(self, "Compilation Successful", "Your code has been successfully compiled!")
        else:
            self.outputArea.setText("Error in code format.")

    def convert_to_json(self,code):
        lines = code.strip().split('\n')
        result = {}
        current_function = None
        for_loop_args = None
        for_loop_body = []

        def process_for_loop_body(body):
            # Join the body list into a single string and encode it as Base64
            body_str = ''.join(body)
            encoded_body = base64.b64encode(body_str.encode('utf-8')).decode('utf-8')
            return encoded_body

        # Regex pattern to extract parts of FOR loop
        for_loop_pattern = r'\(\s*\[([^\]]+)\]\s*,\s*([^\],]+)\s*,\s*\[([^\]]*)\]\s*\)'

        for line in lines:
            line = line.strip()
            if line.startswith('DEF '):
                parts = line[4:].split(':')
                function_name = parts[0].strip()
                args = parts[1].strip().split(',')
                result[function_name] = {
                    'args': [arg.strip() for arg in args],
                    'eip': []
                }
                current_function = function_name
                for_loop_args = None  # Reset FOR loop variables when a new function starts
                for_loop_body = []
            elif line == 'END':
                if current_function:
                    if for_loop_body and for_loop_args is not None:
                        # Process FOR loop before ending function
                        for_loop_body_encoded = process_for_loop_body(for_loop_body)
                        result[current_function]['eip'].append(f'FOR:{",".join(for_loop_args)},{for_loop_body_encoded}')
                        for_loop_body = []
                        for_loop_args = None
                    current_function = None
                continue
            elif line.startswith('FOR:'):
                # Extract FOR loop arguments and start collecting body
                match = re.match(for_loop_pattern, line[len('FOR:'):].strip())
                if match:
                    for_payload='FOR:'+match.group(1).strip()+','+match.group(2).strip()+','+base64.b64encode(match.group(3).strip().encode('utf-8')).decode('utf-8')
                    result[current_function]['eip'].append(f'{for_payload}')
    
            else:
                # Handle other commands
                if current_function:
                    eip_parts = line.split(':', 1)  # Ensure split only on the first occurrence of ':'
                    if len(eip_parts) == 2:
                        eip_cmd = eip_parts[0].strip()
                        eip_values = eip_parts[1].strip().split(',')

                        if eip_cmd.startswith('CALL '):
                            eip_cmd = f'CALL-{eip_cmd[5:].strip()}'

                        result[current_function]['eip'].append(f'{eip_cmd}:{",".join(eip_values)}')

        return json.dumps(result, separators=(',', ':'))
    def format_code(self):
        code = self.codeEditor.toPlainText()

        lines = code.splitlines()
        formatted_lines = []
        indent_level = 0
        indent_size = 4 

        for line in lines:
            stripped_line = line.strip()
            
            if stripped_line.endswith('END'):
                indent_level -= 1
            
            formatted_line = ' ' * (indent_level * indent_size) + stripped_line
            formatted_lines.append(formatted_line)
            
            if stripped_line.startswith('DEF '):
                indent_level += 1

        formatted_code = '\n'.join(formatted_lines)
        self.codeEditor.setText(formatted_code)

    def change_font_size(self, size):
        try:
            size = int(size)
            self.set_default_font_size(size)
        except ValueError:
            pass 

    def generate_random_key(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    def toggle_key_input(self, state):
        if state == Qt.Checked:
            self.keyInput.setEnabled(False)
            self.keyInput.clear()
        else:
            self.keyInput.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CompilerInterface()
    window.show()
    sys.exit(app.exec_())