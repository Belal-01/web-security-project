import paramiko
import sys

def run_command(host, user, password, command):
    print(f"Connecting to {host}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(hostname=host, username=user, password=password)
        print(f"Connected! Executing: {command}\n" + "-"*40)
        
        stdin, stdout, stderr = client.exec_command(command)
        
        # Read outputs
        out = stdout.read().decode('utf-8')
        err = stderr.read().decode('utf-8')
        
        if out:
            print(out)
        if err:
            print("ERROR:\n", err)
            
        print("-" * 40)
        print(f"Exit status: {stdout.channel.recv_exit_status()}")
        
    except Exception as e:
        print(f"Connection or execution failed: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_on_vm.py '<command>'")
        sys.exit(1)
        
    cmd = sys.argv[1]
    run_command('192.168.117.130', 'bilal', 'm8498069', cmd)
