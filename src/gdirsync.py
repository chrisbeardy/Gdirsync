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
            # Possibly throws an exception
            self.exc_run()
        except Exception as e:
            self.exc = sys.exc_info()
            # Save details of the exception thrown but don't rethrow,
            # just complete the function


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
    ]
    window = sg.Window("Gdirsync", layout)
    source_dir_browse = window["sourceDirBrowse"]
    target_dir_browse = window["targetDirBrowse"]
    sync_button = window["syncButton"]

    def reset_main_window():
        """Internal function to reset main window elements."""
        source_dir_browse.update(disabled=False)
        target_dir_browse.update(disabled=False)
        sync_button.update("Sync")
        sync_button.update(disabled=False)

    # App Logic
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
                source_dir_browse.update(disabled=True)
                target_dir_browse.update(disabled=True)
                sync_button.update(disabled=True)
                sg.Popup("Please complete all fields")
                reset_main_window()
            else:
                p = GSync(
                        source_dir,
                        target_dir,
                        "sync",
                        purge=values[2],
                        create=values[3],
                    )
                sync_jobs.append(p)
                source_dirs.append(source_dir)
                target_dirs.append(target_dir)
                completed_jobs.append(False)
                p.start()
                sg.Popup("Syncing " + source_dir + " to " + target_dir, title="Syncing...", auto_close=True, auto_close_duration=2, non_blocking=True)

        for i in range(len(sync_jobs)):
            if not sync_jobs[i].is_alive() and not completed_jobs[i]:
                sg.Popup("Sync from " + source_dirs[i] + " to " + target_dirs[i] + " complete ", title="Gdirsync - Sync Complete", non_blocking=True)
                completed_jobs[i] = True

    window.close()

    for job in sync_jobs:
        if job.is_alive():
            jobs_running_layout = [[sg.Text("Existing sync jobs will continue in the background")]]
            jobs_running_window = sg.Window("Syncing...", jobs_running_layout, disable_close=True)
            jobs_running_window.read(timeout=2000)
            jobs_running_window.hide()
            jobs_running_window.close()
            break

    while True:
        for i in range(len(sync_jobs)):
            if not sync_jobs[i].is_alive() and not completed_jobs[i]:
                sg.Popup("Sync from " + source_dirs[i] + " to " + target_dirs[i] + " complete ", title="Gdirsync - Sync Complete")
                completed_jobs[i] = True

        all_jobs_complete = True  # TODO remove iteration
        for i in range(len(sync_jobs)):
            if not completed_jobs[i]:
                all_jobs_complete = False
                break

        if all_jobs_complete:
            break

    for job in sync_jobs:
        job.join()


if __name__ == "__main__":
    main()
