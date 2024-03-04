import subprocess

def importer(file_path):
   
    result = subprocess.run(
        [f"cat {file_path} | grep '^http' | grep -v '\.js' | uro "],
        stdout=subprocess.PIPE,  # Capture standard output
        stderr=subprocess.PIPE,  # Capture standard error
        text=True,               # Work with text data instead of binary
        shell=True               # Use shell to interpret the command
    )
    # result = subprocess.run(
    #     [f"cat {file_path} | grep '^http' | grep -v '\.js'"],
    #     stdout=subprocess.PIPE,  # Capture standard output
    #     stderr=subprocess.PIPE,  # Capture standard error
    #     text=True,               # Work with text data instead of binary
    #     shell=True               # Use shell to interpret the command
    # )
    if not result.stderr:
        requests = []
        for line in result.stdout.splitlines():
            requests.append(line)
        return requests

