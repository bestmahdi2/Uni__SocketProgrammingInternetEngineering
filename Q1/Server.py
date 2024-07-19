import os
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM


class Server:
    """
        Class to represent a Server
    """

    FILE_NAME = './film_final.mkv'  # The file name
    KEEP_TEMP_FILE = True
    HOST = 'localhost'  # The host address
    PORT = 12345  # The port number
    FILE_PART = 8  # Split file into this number

    def __init__(self):
        print(f'------------- File Transfer App -------------\n')

    @staticmethod
    def receive_file(index: int, connection: socket) -> None:

        """The method to receive a part file from client,

            Parameters:
                index (int): The index of file's part should be received from client.
                connection (socket) : The connection !"""

        # open the file
        with open(f'{index}.temp', 'wb') as f:
            while True:
                # receive the data
                data = connection.recv(1024)
                if not data:
                    break
                # write the data to file
                f.write(data)

        print(f"> Part {index} received !")

        # close the connection
        connection.close()

    def merge_file(self):
        # accept the connection
        connection, address = sock.accept()

        # get the data
        data = connection.recv(1024)

        # a dictionary to keep files
        keeper = {}

        # get the command to merge the file
        if data == bytes("end", encoding='utf-8'):
            # open and order the received files
            for i in range(8):
                with open(f"{i}.temp", 'rb') as file:
                    # get the order number
                    number = int(file.read(1).decode('utf-8'))
                    # throw away the ")"
                    file.read(1)
                    # get the original data
                    data = file.read()
                    # save the data
                    keeper[number] = data

                # delete temp files or keep them
                if not self.KEEP_TEMP_FILE:
                    os.remove(f"./{i}.temp")

            # merge and append each part to the main file
            with open(self.FILE_NAME, 'ab+') as file:
                for i in range(self.FILE_PART):
                    file.write(keeper[i])

            print(f"> Done merging !")


# Driver Code
if __name__ == '__main__':
    S = Server()

    # create or empty the saving file
    with open(S.FILE_NAME, 'wb') as file:
        pass

    # open TCP, listen for any connection
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((S.HOST, S.PORT))
    sock.listen(S.FILE_PART)

    # a list to keep all threads
    threads = []

    for part in range(S.FILE_PART):
        # accept the connection
        connection, address = sock.accept()

        # create a thread and append it to threads
        t = Thread(target=S.receive_file, args=(part, connection))
        threads.append(t)
        t.start()

    # join all threads together
    for t in threads:
        t.join()

    # merge the received parts into one file
    S.merge_file()
