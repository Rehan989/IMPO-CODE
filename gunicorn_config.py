import os

bind = "127.0.0.1:8080"  # Replace with your desired listening address and port
workers = 3  # Adjust the number of worker processes as needed
activate_env = "/www/wwwroot/admin.islamicaudiobooks.com/python-server/IMPO_T2S/venvbook/bin/activate"  # Replace with your virtual env path

def pre_fork(server, worker):
    # Activate the virtual environment before launching workers
    os.environ['PATH'] = os.path.join(os.getcwd(), activate_env) + ':' + os.environ['PATH']
    with open(os.path.join(os.getcwd(), 'venvbook/bin/activate'), 'r') as f:
        code = compile(f.read(), os.path.join(os.getcwd(), 'venvbook/bin/activate'), 'exec')
        exec(code, globals(), locals())

def post_fork(server, worker):
    # Ensure worker processes inherit the virtual environment
    os.environ['PATH'] = os.path.join(os.getcwd(), activate_env) + ':' + os.environ['PATH']