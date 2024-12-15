import os,threading
def main():
    if os.name == 'nt':
        from . import fluent
        fluent.main()
        
thread = threading.Thread(target=main , daemon=True)
thread.start()