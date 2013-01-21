import sys
# checking conf file on startup
try:
    import conf
except SyntaxError as e:
    print "Conf Error!"
    print str(e)
    sys.exit(1)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    # lalala...
    for a in argv: print a
    print("yay")
    # return exit code
    
if __name__ == "__main__":
    sys.exit(main())
