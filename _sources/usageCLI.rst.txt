This is a command line script so you will need a terminal window open to use it.

Validate a package
------------------
To run validation on a package, type "hathivalidate" followed by path to the package. If the path has spaces in it, you must
surround the path by quotes.


    :command:`hathivalidate "Y:\\DCC Unprocessed Files\\20170523_CavagnaCollectionRBML_rj"`




The Help Screen
---------------
This documentation should be up to date. However, you can always type :command:`hathivalidate -h` or
:command:`hathivalidate --help` into a command prompt to display the script usage instructions along with any
additional the options.


:command:`hathivalidate -h`

.. code-block:: console

    C:\Users\hborcher.UOFI>hathivalidate -h

    usage: hathivalidate [-h] [--debug] [--log-debug LOG_DEBUG] path

    positional arguments:
      path                  Path to the hathipackages

    optional arguments:
      -h, --help            show this help message and exit

    Debug:
      --debug               Run script in debug mode
      --log-debug LOG_DEBUG
                            Save debug information to a file




It's that simple!