#!/usr/bin/env python
import argparse, os, sys, time
from subprocess import PIPE, Popen
from threading  import Thread
from Queue import Queue, Empty


parser = argparse.ArgumentParser()
parser.add_argument("-m", "--match-anywhere", help="match anywhere in address", action="store_true")
parser.add_argument("wallet_name", help="file name for wallet binary")
parser.add_argument("wallet_pw", help="desired wallet password")
parser.add_argument("target", help="string to match in address")
args = parser.parse_args()

ON_POSIX = 'posix' in sys.builtin_module_names


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


def createWallet():
    """Method that will loop on itself in a single thread until match"""
    p = Popen(["./simplewallet", "--set_log", "0", "--generate-new-wallet",
                          args.wallet_name, "--password", args.wallet_pw],
                          stdout=PIPE,
                          stdin=PIPE,
                          bufsize=1,
                          close_fds=ON_POSIX)

    q = Queue()
    t = Thread(target=enqueue_output, args=(p.stdout, q))
    t.daemon = True  # thread dies with the program
    t.start()

    t_start = time.time()
    electrum = ''
    electrum_coming = False

    while time.time() - t_start < 10:
        try:
            line = q.get_nowait()
            if "new wallet:" in line:
                address = line.rstrip().split(': ')[1]
            if "view key:" in line:
                view_key = line.rstrip().split(': ')[1]
            if electrum_coming:
                electrum = line.rstrip()
            if "PLEASE NOTE:" in line:
                electrum_coming = line.rstrip()
        except Empty:
            pass
        else:
            pass
        if len(electrum) > 2:
            break

    p.kill()

    # print "Generated address: {0}".format(address)
    if not args.match_anywhere:
        print "Target: {0}, Address first chars: {1}".format(args.target, address[2:len(args.target)+2])
        if args.target in address[2:len(args.target)+2]:
            print "success1!"
            with open('./{0}_info.txt'.format(args.wallet_name), 'w') as f:
                f.write("Name:\n{0}\n\nAddress:\n{1}\n\nView key:\n{2}\n\nElectrum seed:\n{3}".format(
                    args.wallet_name, address, view_key, electrum))
            return 0
        else:
            os.remove('./{0}'.format(args.wallet_name))
            os.remove('./{0}.keys'.format(args.wallet_name))
            os.remove('./{0}.address.txt'.format(args.wallet_name))
            os.remove('./simplewallet.log')
            return 1
    elif args.match_anywhere:
        print "Target: {0}, Address: {1}".format(args.target, address)
        if args.target in address:
            print "success2!"
            with open('./{0}_info.txt'.format(args.wallet_name), 'w') as f:
                f.write("Name:\n{0}\n\nAddress:\n{1}\n\nView key:\n{2}\n\nElectrum seed:\n{3}".format(
                    args.wallet_name, address, view_key, electrum))
            return 0
        else:
            os.remove('./{0}'.format(args.wallet_name))
            os.remove('./{0}.keys'.format(args.wallet_name))
            os.remove('./{0}.address.txt'.format(args.wallet_name))
            os.remove('./simplewallet.log')
            return 1


if __name__ == "__main__":
    if not args.match_anywhere:
        print "You're target is {0} characters, expect to need {1} attempts to match at begininning of address".format(len(args.target), 62**len(args.target))
    elif args.match_anywhere:
        print "You're target is {0} characters, expect to need {1:.0f} attempts to match anywhere in the address".format(len(args.target), 1.0/((94.0-len(args.target))*(62.0**(94-len(args.target)))/(62.0**94)))
    print 'starting'
    time.sleep(1)
    print '...'
    time.sleep(1)
    n = 1
    t = time.time()
    while True:
        print "Attempt #{0}, total time = {1:.2f} seconds".format(n+1, time.time()-t)
        out = createWallet()
        if out == 0:
            break
        n += 1

