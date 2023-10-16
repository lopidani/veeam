# -*- coding: utf-8 -*-

"""Implement a program that synchronizes two folders: source and replica.
The program should maintain a full, identical copy of source folder at replica folder
1. Synchronization must be one-way: after the synchronization, content of the
   replica folder should be modified to exactly match content of the source
   folder
2. Synchronization should be performed periodically
3. File creation/copying/removal operations should be logged to a file and to the
   console output
4. Folder paths, synchronization interval and log file path should be provided
   using the command line arguments
Requirements:
1. Do not use third-party libraries that implement folder synchronization
2. It is allowed (and recommended) to use external libraries implementing other
   well-known algorithms. For example, there is no point in implementing yet
   another function that calculates MD5 if you need it for the task - it is perfectly
   acceptable to use a third-party (or built-in) library
"""

import os
import shutil
import filecmp
import logging
import sys
import threading

SOURCE = str(sys.argv[1])
REPLICA = str(sys.argv[2])
LOG =str(sys.argv[3])
INTERVAL = int(sys.argv[4])

class Sync():
    """Class to syncronize content of two folders - source folder.
    and replica folder
    """
    def __init__(self, source: str, replica: str):
        """Initialises the Sync class.
        Args: source: source folder path
              replica: replica folder path
        """
        self.source = source
        self.replica = replica
        if not os.path.isdir(self.source):
            raise FileNotFoundError(f"Source directory {self.source} does not exist")
        if not os.path.isdir(self.replica):
            raise FileNotFoundError(f"Replica directory {self.replica} does not exist")
        if len(os.listdir(self.source)) == 0:
            raise NothingToSync(f"Source folder {self.source} is empty. There is nothing to sync")

    def sync(self):
        """Method to syncronize content of replica folder with source folder."""
        print(f"Sync {self.source} folder with {self.replica} folder")
        logging.basicConfig(filename=f"{LOG}", level=logging.INFO,\
                            format='%(asctime)s %(message)s',\
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        # If replica folder is empty copy entire source folder to replica folder
        if len(os.listdir(self.replica)) == 0:
            print(f"Copy entire source folder {self.source} to replica folder {self.replica}")
            logging.info("Copy entire source folder %s to replica folder %s", self.source,\
                         self.replica)
            shutil.copytree(self.source, self.replica, dirs_exist_ok=True)
        else:
            dcmp = filecmp.dircmp(self.source, self.replica)
            if dcmp.right_only:
                for rep in dcmp.right_only:
                    print(f"Remove file {rep} from folder {self.replica}")
                    os.remove(os.path.join(self.replica, rep))
            if dcmp.left_only + dcmp.diff_files:
                for item in dcmp.left_only + dcmp.diff_files:
                    print(f"Copy file {os.path.join(self.source, item)} to folder {self.replica}")
                    logging.info("Copy file %s to folder %s", os.path.join(self.source, item),\
                                 self.replica)
                    shutil.copyfile(f"{os.path.join(self.source, item)}",\
                                    f"{os.path.join(self.replica, item)}")
        threading.Timer(INTERVAL, self.sync).start()


class NothingToSync(Exception):
    """NothingToSync class exception with own message."""
    def __init__(self, message):
        super().__init__(message)

Sync(SOURCE, REPLICA).sync()
