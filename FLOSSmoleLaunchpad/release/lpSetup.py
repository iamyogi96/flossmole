from launchpadlib.launchpad import Launchpad

def lpObj():
  cachedir = "cache/"
  return Launchpad.login_anonymously('flossmole-dev', 'production', cachedir)
