from stub_code import *
import sys
import queue
import mock_server
import json
import uuid
import time
import datetime
import os.path

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

msg_queue = queue.Queue()


class SkeletonRun(Ui_MainWindow):

    def __init__(self, window):

        self.setupUi(window)

        self.ip = ''
        self.port = ''
        self.payload = ''
        self.emu_time = ''
        self.reload_config()

        self.menu_bar.setNativeMenuBar(False)
        # Line not needed when working on Windows

        self.mquit.clicked.connect(self.close)
        self.mquit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.squit.clicked.connect(self.close)
        self.run.clicked.connect(self.run_func)
        self.clear_all.clicked.connect(self.clear_app_log)
        self.exp.clicked.connect(self.export)
        self.rel_con.clicked.connect(self.reload_config)

        self.action_quit.triggered.connect(self.close)
        self.action_clear_all.triggered.connect(self.clear_app_log)
        self.action_export.triggered.connect(self.export)
        self.action_rel_con.triggered.connect(self.reload_config)
        self.action_run.triggered.connect(self.run_func)
        self.action_about.triggered.connect(self.about)

        self.progress_bar.setValue(0)

    def run_func(self):
        # call run thread and receiver thread
        if self.ip == '' or self.port == '' or self.payload == '' or self.emu_time == '':
            QtWidgets.QMessageBox.warning(None, "Parameters", "Some or all of the parameters " +
                                                "do not have assigned values. Please assign them in the given fields."
                                                            , QtWidgets.QMessageBox.Ok)
            return
        self.Main.setCurrentIndex(1)

        self.app_log_text.append('Python 3.6.4, MacOS High Sierra 10.13.6')
        request_id = str(uuid.uuid4())
        self.app_log_text.append('uuid: ' + request_id)

        self.run.setEnabled(False)
        self.mquit.setEnabled(False)
        self.squit.setEnabled(False)

        self.run_thread = RunThread(self.ip, int(self.port), self.payload, int(self.emu_time), request_id)
        self.start = time.time()
        self.run_thread.start()

        self.reciever_thread = ReceiverThread()
        self.reciever_thread.start()

        self.reciever_thread.msg_sig.connect(self.update_status_log)
        self.reciever_thread.msg_sig.connect(self.update_progress)
        self.reciever_thread.msg_sig.connect(self.update_status_bar)

        if self.central_widget.isMinimized():
            print('Window is minimized')

    def close(self):
        sys.exit()

    def update_status_log(self, msg):
        self.app_log_text.append('Step ' + str(msg['current_step']) + ' / ' + str(msg['total_steps']))
        self.app_log_text.append(str(datetime.datetime.now()))
        if msg['current_step'] == msg['total_steps']:
            self.run.setEnabled(True)
            self.mquit.setEnabled(True)
            self.squit.setEnabled(True)
            self.end = time.time()
            self.timer = self.end - self.start
            self.app_log_text.append('Function call completed. Time elapsed: ' + str(self.timer) + ' seconds')
            self.app_log_text.append('\n')

    def file_save(self):
        name = QtWidgets.QFileDialog.getSaveFileName()
        if name[0] == '':
            return ''
        return name[0]

    def export(self):
        file_name = self.file_save()
        if file_name == '':
            return
        file = open(os.path.join(file_name), 'w+')
        file.truncate(0)
        file.write(self.app_log_text.toPlainText())
        file.close()

    def reload_config(self):
        self.ip = self.mip_text.text()
        self.port = self.mport_text.text()
        self.payload = self.mpayload_text.text()
        self.emu_time = self.mtimer_text.text()
        self.sip_text.setText(self.ip)
        self.sport_text.setText(self.port)
        self.spayload_text.setText(self.payload)
        self.slabel_text.setText(self.emu_time)

    def clear_app_log(self):
        self.app_log_text.clear()

    def update_progress(self, msg):
        current_step = float(msg['current_step'])
        total_steps = float(msg['total_steps'])
        self.progress_bar.setValue(100 * (current_step / total_steps))

    def update_status_bar(self, msg):
        self.status_bar.showMessage('  Step ' + str(msg['current_step']) + ' / ' + str(msg['total_steps'])
                                        + '    ' + str(datetime.datetime.now()))
        if msg['current_step'] == msg['total_steps']:
            self.status_bar.showMessage('Function call completed in ' + str(self.timer) + ' seconds')

    def clear_status(self):
        self.status_bar.clearMessage()

    def about(self):
        about_dialog = QtWidgets.QDialog()
        about_dialog.resize(300, 200)
        about_text = QtWidgets.QTextBrowser(about_dialog)
        about_text.resize(290, 190)
        about_text.move(5, 5)
        about_text.setText('Developed with PyQt5 on PyCharm CE 2019.1\nMac OS Sierra 10.13.6')
        about_dialog.setWindowTitle('About')

        about_dialog.exec_()


class ReceiverThread(QtCore.QThread):

    msg_sig = QtCore.pyqtSignal(dict)

    def __init__(self):
        super(ReceiverThread, self).__init__()

    def run(self):
        print('worker thread started')
        while True:
            item = msg_queue.get()
            msg = json.loads(item)
            self.msg_sig.emit(msg)
        print('worker thread ended')


class RunThread(QtCore.QThread):

    def __init__(self, ip, port, payload, emu_time, request_id):
        self.ip = ip
        self.port = port
        self.payload = payload
        self.emu_time = emu_time
        self.request_id = request_id
        super().__init__()

    def run(self):
        print('run thread started')
        mock_server.call_manor(self.request_id, self.ip, self.port, self.payload, msg_queue, self.emu_time)
        print('run thread finished, call completed')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = SkeletonRun(MainWindow)
    MainWindow.show()
    app.exec_()
