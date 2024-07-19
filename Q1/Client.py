import os
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM


class Client:
    """
        Class to represent a Client
    """

    FILE_NAME = './film.mkv'  # The file name
    HOST = 'localhost'  # The host address
    PORT = 12345  # The port number
    FILE_PART = 8  # Split file into this number

    def __init__(self):
        print(f'------------- File Transfer App -------------\n')

    def send_file(self, index: int, **kwargs) -> None:
        """The method to send a file to server in parts,

            Parameters:
                index (int): The index of file's part should be sent to server."""

        # read the file
        with open(self.FILE_NAME, 'rb') as f:
            # throw away the sent parts
            f.read(kwargs['start'])

            # keep the part should be sent
            data = f.read(kwargs['end'] - kwargs['start'])

        # open TCP, connect, and send data with an index and close the connection
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((self.HOST, self.PORT))
        sock.sendall(bytes(str(index) + ")", encoding='utf-8') + data)
        sock.close()

        print(f"> Sending part {index} !")

    def end_file(self) -> None:
        """The method to send ending file notification to server to merge file"""

        # open TCP, connect, and send notification and close the connection
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((self.HOST, self.PORT))
        sock.sendall(bytes("end", encoding='utf-8'))
        sock.close()


# Driver Code
if __name__ == '__main__':
    C = Client()

    # get file size
    file_size = os.path.getsize(C.FILE_NAME)

    # make the chunk size
    chunk_size = file_size // C.FILE_PART + 1

    # a list to keep all threads
    threads = []

    for i in range(C.FILE_PART):
        # find start and end byte the file's chunk
        start_byte = i * chunk_size
        end_byte = min((i + 1) * chunk_size, file_size)

        # create a thread and append it to threads
        t = Thread(target=C.send_file, args=(i,), kwargs={'start': start_byte, 'end': end_byte})
        threads.append(t)
        t.start()

    # join all threads together
    for t in threads:
        t.join()

    # send ending file notification to server to merge file
    C.end_file()
