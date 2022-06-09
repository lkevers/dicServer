import socket
import sys

#
# dicServer - a multithreaded socket server allowing to query word lists
#
# Author :  Laurent Kevers - University of Corsica
#           kevers_l@univ-corse.fr
#
# This script is intended to test if a dicServer is up and running.
#

# 
# Copyright University of Corsica -- Laurent Kevers (2022)
# 
# kevers_l@univ-corse.fr
# 
# This software is a computer program whose purpose is the querying of word lists.
# 
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software. You can use, 
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info". 
# 
# As a counterpart to the access to the source code and rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty and the software's author, the holder of the
# economic rights, and the successive licensors have only limited
# liability.
# 
# In this respect, the user's attention is drawn to the risks associated
# with loading, using, modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean that it is complicated to manipulate, and that also
# therefore means that it is reserved for developers and experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or 
# data to be ensured and, more generally, to use and operate it in the 
# same conditions as regards security. 
# 
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
#



#HOST, PORT = "localhost", 1112
HOST, PORT = "", 1112
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(("%s\n"%data).encode(encoding='utf-8'))

    # Receive data from the server and shut down
    received = sock.recv(1024)
finally:
    sock.close()

print ("Sent:     {}".format(data))
print ("Received: {}".format(received.decode()))

