#!/usr/bin/python

import os
import re
import shutil
import hashlib
from optparse import OptionParser

re_dot = re.compile(r'^\.[^\.]+$')

HOME = os.environ["HOME"]
IGNORE = ['.git', '.gitmodules']

def file_hash(f):
    return hashlib.md5(open(f).read()).hexdigest()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-l", "--link-only", dest="link_only",
        action="store_true", default=False,
        help="just link the .dotfiles")
    parser.add_option("-f", "--force", dest="force",
        action="store_true", default=False,
        help="don't back up")
    parser.add_option("-c", "--clean", dest="clean",
        action="store_true", default=False,
        help="cleanup backups")

    options, args = parser.parse_args()

    d = os.path.dirname(os.path.abspath(__file__))
    for f in os.listdir(d):
        if re_dot.match(f) and f not in IGNORE:
            new_f = os.path.join(d, f)
            old_f = os.path.join(HOME, f)
            print "[%s]" % old_f

            if os.path.exists(old_f):
                if options.force:
                    os.remove(old_f)
                else:
                    if file_hash(new_f) == file_hash(old_f):
                        print "    ...ignoring"
                        continue
                    else:
                        print "    ...backing up"
                        shutil.move(old_f, old_f+'.old')

            if options.clean and os.path.exists(old_f+'.old'):
                os.remove(old_f+'.old')

            print "    ...symlinking"
            os.symlink(new_f, old_f)


    if not options.link_only:
        print "Switching to zsh!"
        os.system("chsh -s /bin/zsh")




