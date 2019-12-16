import PySimpleGUI as sg
import threading
import dirsync
import sys


class ExcThread(threading.Thread):
    """Class to extend the python threading module."""

    def exc_run(self):
        """Overwrite this method in implementation.
        """
        pass

    def run(self):
        self.exc = None
        try:
            # Possibly throws an exception
            self.exc_run()
        except Exception as e:
            self.exc = sys.exc_info()
            # Save details of the exception thrown but don't rethrow,
            # just complete the function

    def join(self):
        threading.Thread.join(self)
        if self.exc:
            msg = "Thread '%s' threw an exception: %s" % (self.getName(), self.exc[1])
            new_exc = Exception(msg)
            raise new_exc.with_traceback(self.exc[2])


class GSync(ExcThread):
    """Performs the sync action using dirsync.

    :param source_dir: source directory to sync from
    :type source_dir: str
    :param target_dir: target directory to sync to
    :type target_dir: str
    :param action: action to perform, e.g. 'sync'
    :type action: str
    :param options: additional options to pass to dirsync, e.g. purge = True

    """

    def __init__(self, source_dir, target_dir, action, **options):
        super(GSync, self).__init__()
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.action = action
        self.options = options

    def exc_run(self):
        dirsync.sync(self.source_dir, self.target_dir, self.action, **self.options)


def main():
    """Entry point for gdirsync."""
    # PySimpleGUI Layout
    progress_bar_len = 1000
    layout = [
        [
            sg.Text("Source Directory", size=(20, 1)),
            sg.InputText(do_not_clear=True),
            sg.FolderBrowse(key="sourceDirBrowse"),
        ],
        [
            sg.Text("Target Directory", size=(20, 1)),
            sg.InputText(do_not_clear=True),
            sg.FolderBrowse(key="targetDirBrowse"),
        ],
        [sg.Text("Options")],
        [
            sg.Checkbox(
                "Purge",
                tooltip="Removes files from target directory if not in source directory",
                default=True,
            ),
            sg.Checkbox(
                "Create",
                tooltip="Creates target directory if it does not exist",
                default=True,
            ),
        ],
        [sg.Button("Sync", key="syncButton")],
        [
            sg.ProgressBar(
                progress_bar_len, orientation="h", size=(50, 20), key="progressBar"
            )
        ],
    ]
    window = sg.Window("Gdirsync").Layout(layout)
    source_dir_browse = window["sourceDirBrowse"]
    target_dir_browse = window["targetDirBrowse"]
    sync_button = window["syncButton"]
    progress_bar = window["progressBar"]
    syncing = False

    def reset_main_window(syncing, progress_loop):
        """Internal function to reset main window elements."""
        source_dir_browse.update(disabled=False)
        target_dir_browse.update(disabled=False)
        sync_button.update("Sync")
        sync_button.update(disabled=False)
        syncing = False
        progress_loop = 0
        progress_bar.UpdateBar(progress_loop)
        return syncing, progress_loop

    # App Logic
    progress_loop = 0
    while True:
        event, values = window.read(timeout=100)
        if event is None:
            break
        elif not syncing and event == "syncButton":
            source_dir = values[0]
            target_dir = values[1]
            if source_dir is "" or target_dir is "":
                source_dir_browse.update(disabled=True)
                target_dir_browse.update(disabled=True)
                sync_button.update(disabled=True)
                sg.Popup("Please complete all fields")
                syncing, progress_loop = reset_main_window(syncing, progress_loop)
            else:
                t1 = GSync(
                    source_dir, target_dir, "sync", purge=values[2], create=values[3]
                )
                t1.start()
                syncing = True
                source_dir_browse.update(disabled=True)
                target_dir_browse.update(disabled=True)
                sync_button.update(disabled=True)
        elif syncing and not t1.is_alive():
            t1.join()
            sg.Popup("Sync Complete")
            syncing, progress_loop = reset_main_window(syncing, progress_loop)
        elif syncing and event == sg.TIMEOUT_KEY:
            progress_bar.UpdateBar(progress_loop)
            progress_loop += 1
            if progress_loop >= progress_bar_len:
                progress_loop = 1
    if syncing:
        t1.join()


if __name__ == "__main__":
    main()
