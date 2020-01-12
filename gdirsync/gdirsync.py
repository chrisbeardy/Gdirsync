import PySimpleGUI as sg
import multiprocessing
import dirsync
import sys


class ExcProcess(multiprocessing.Process):
    """Class to extend the python processing module."""

    def exc_run(self):
        """Overwrite this method in implementation."""
        pass

    def run(self):
        self.exc = None
        try:
            self.exc_run()
        except Exception as e:
            self.exc = sys.exc_info()
            # Save details of the exception thrown but don't rethrow


class GSync(ExcProcess):
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
    """Entry point for gdirsync.

    Sets up main window so user can start sync jobs.
    If sync jobs are still running when user closes window,
    waits for syncing to end then alerts user.

    """
    # PySimpleGUI Layout
    layout = [
        [
            sg.Text("Source Directory", size=(20, 1)),
            sg.InputText(),
            sg.FolderBrowse(key="sourceDirBrowse"),
        ],
        [
            sg.Text("Target Directory", size=(20, 1)),
            sg.InputText(),
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
    ]
    window = sg.Window("Gdirsync", layout)
    source_dir_browse = window["sourceDirBrowse"]
    target_dir_browse = window["targetDirBrowse"]
    sync_button = window["syncButton"]

    def disable_inputs():
        """Internal function to disable inputs"""
        source_dir_browse.update(disabled=True)
        target_dir_browse.update(disabled=True)
        sync_button.update(disabled=True)

    def reset_main_window():
        """Internal function to reset main window elements."""
        source_dir_browse.update(disabled=False)
        target_dir_browse.update(disabled=False)
        sync_button.update(disabled=False)

    # App Logic - Main persistent window
    sync_jobs = []
    source_dirs = []
    target_dirs = []
    completed_jobs = []

    while True:
        event, values = window.read(timeout=500)
        if event is None:
            break
        elif event == "syncButton":
            source_dir = values[0]
            target_dir = values[1]
            if source_dir is "" or target_dir is "":
                disable_inputs()
                sg.PopupAutoClose("Please complete all fields", title="Gdirsync")
                reset_main_window()
            else:
                p = GSync(
                    source_dir, target_dir, "sync", purge=values[2], create=values[3]
                )
                sync_jobs.append(p)
                source_dirs.append(source_dir)
                target_dirs.append(target_dir)
                completed_jobs.append(False)
                p.start()
                disable_inputs()
                sg.PopupAutoClose(
                    "Syncing " + source_dir + " to " + target_dir, title="Syncing..."
                )
                reset_main_window()

        for i in range(len(sync_jobs)):
            if not sync_jobs[i].is_alive() and not completed_jobs[i]:
                sg.PopupNonBlocking(
                    "Sync from "
                    + source_dirs[i]
                    + " to "
                    + target_dirs[i]
                    + " complete ",
                    title="Gdirsync - Sync Complete",
                )
                completed_jobs[i] = True

    # main window closed
    # check for and complete current running sync jobs in the background
    for job in sync_jobs:
        if job.is_alive():
            sg.PopupAutoClose(
                "Existing sync jobs will continue in the background",
                title="Gdirsync - Syncing...",
            )
            break

    while True:
        for i in range(len(sync_jobs)):
            if not sync_jobs[i].is_alive() and not completed_jobs[i]:
                # blocking popup here otherwise program will exit causing windows to close
                sg.Popup(
                    "Sync from "
                    + source_dirs[i]
                    + " to "
                    + target_dirs[i]
                    + " complete ",
                    title="Gdirsync - Sync Complete",
                )
                completed_jobs[i] = True

        all_jobs_complete = True
        for i in range(len(sync_jobs)):
            if not completed_jobs[i]:
                all_jobs_complete = False
                break

        if all_jobs_complete:
            break

    for job in sync_jobs:
        job.join()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
