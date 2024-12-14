from .Back_End import Back
from .Front_End import Front

def main():
    print("GUI wird gestartet")
    back = Back()
    e = Front(back)
    
if __name__ == "__main__":
    main()
