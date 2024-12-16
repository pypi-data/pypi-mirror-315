
# import ctypes
#
# # Load the shared object file
# lib_path = './autograde.cpython-310-x86_64-linux-gnu.so'  # Update with the correct path if needed
# autograde = ctypes.CDLL(lib_path)

# Call the init_log function
# import autograde
# autograde.init_log()

from main import init_log, validate
init_log()