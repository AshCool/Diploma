from projectD import *


def main():
    # main() method of project
    # creates main window via TheD() class from projectD.py

    root = Tk()
    TheD(root).pack(side="top", fill="both", expand=True)
    root.mainloop()


# launching the thing
if __name__ == "__main__":

    main()
