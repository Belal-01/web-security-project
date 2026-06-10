import pty
import os
import sys

if len(sys.argv) < 3:
    print("Usage: python3 wsl_sshpass.py <password> <command...>")
    sys.exit(1)

password = sys.argv[1]
command = sys.argv[2:]

pid, fd = pty.fork()

if pid == 0:
    # Child process
    os.execvp(command[0], command)
else:
    # Parent process
    buffer = b""
    sent_password = False
    while True:
        try:
            data = os.read(fd, 1024)
            if not data:
                break
            
            # Print output from ssh
            sys.stdout.buffer.write(data)
            sys.stdout.flush()
            
            # Check for password prompt
            if not sent_password:
                buffer += data
                if b"password:" in buffer.lower():
                    os.write(fd, password.encode() + b"\n")
                    sent_password = True
                    buffer = b""
        except OSError:
            break
    os.waitpid(pid, 0)
