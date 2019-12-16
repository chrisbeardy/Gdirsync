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
        [sg.ProgressBar(1000, orientation="h", size=(50, 20), key="progressBar")],
    ]
    window = sg.Window("Gdirsync").Layout(layout)
    source_dir_browse = window["sourceDirBrowse"]
    target_dir_browse = window["targetDirBrowse"]
    sync_button = window["syncButton"]
    progress_bar = window["progressBar"]

    # App Logic
    while True:
        event, values = window.read(timeout=50)
        if event is None:
            sys.exit()
        elif event == "syncButton":
            source_dir = values[0]
            target_dir = values[1]
            if source_dir is "" or target_dir is "":
                sg.Popup("Please complete all fields")
            else:
                t1 = GSync(
                    source_dir, target_dir, "sync", purge=values[2], create=values[3]
                )
                t1.start()
                source_dir_browse.update(disabled=True)
                target_dir_browse.update(disabled=True)
                sync_button.update("Cancel")

                i = 0
                while True:
                    event, value = window.Read(timeout=100)
                    if not t1.is_alive():
                        t1.join()
                        i = 0
                        progress_bar.UpdateBar(i)
                        sync_button.update(disabled=True)
                        sg.Popup("Sync Complete")
                        source_dir_browse.update(disabled=False)
                        target_dir_browse.update(disabled=False)
                        sync_button.update("Sync")
                        sync_button.update(disabled=False)
                        break
                    if event is None:
                        sys.exit()  # TODO kill thread and popup warning
                    elif event == "syncButton":
                        source_dir_browse.update(disabled=False)
                        target_dir_browse.update(disabled=False)
                        sync_button.update("Sync")
                        # TODO cancel
                    elif event == sg.TIMEOUT_KEY:
                        progress_bar.UpdateBar(i)
                        i += 1
                        if i >= 1000:
                            i = 1


if __name__ == "__main__":
    main()
