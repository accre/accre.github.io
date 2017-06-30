from feedgen.feed import FeedGenerator
from datetime import datetime
from dateutil.tz import tzlocal
import csv
import json
import subprocess
import re
from collections import OrderedDict
import dill as pickle


def check_gpfs():
  """ Launch system calls to check the status of GPFS """

  calls = {
    '/data':    ['stat', '/gpfs21'],
    '/home':    ['stat', '/gpfs22'],
    '/scratch': ['stat', '/gpfs23'],
    '/dors':    ['stat', '/dors']
  }

  status = dict()
  for k, call in calls.items():
    status.update({k: subprocess.call(call)})
  return status

def probe_slurm():
  """ Return a status from a a server """
  with open('SlurmStatus.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    goods, bads, unks = [], [], []
    for row in reader:
      if row['status'] == 'GOOD':
        goods.append(row)
      elif row['status'] == 'BAD':
        bads.append(row)
      else:
        unks.append(row)

    return {'GOOD': len(goods), 'BAD': len(bads), 'UNKNOWN': len(unks)}


def create_fg():
  # Create the feed
  fg = FeedGenerator()
  fg.id("http://www.accre.vanderbilt.edu")
  fg.title("ACCRE's Status Feed")
  fg.author(dict(name="Josh Arnold", email="arnoldjr@accre.vanderbilt.edu"))
  fg.link(href="http://www.accre.vanderbilt.edu", rel="alternate")
  fg.logo("http://www.accre.vanderbilt.edu/"
          "wp-content/themes/ashford/favicon.ico")
  fg.subtitle("ACCRE's Status Feed")
  fg.language('en')
  return fg


def pickle_fg(fg):
  with open("fg.dpkl", "wb") as file:
    pickle.dump(fg, file)


def unpickle_fg():
  with open("fg.dpkl", "rb") as file:
    return pickle.load(file)


def main():

  services = OrderedDict([
    ('GPFS', '\"red\"'),
    ('SLURM', '\"green\"'),
    ('Login', '\"yellow\"'),
  ])

  # Check GPFS
  check_gpfs()

  # Probe SLURM
  status = probe_slurm()
  status_string = json.dumps(status)

  with open('status_lights.html', 'r') as f:
    light_string = re.sub('\s+', ' ', f.read())

  if False:
    fg = create_fg()
    pickle_fg(fg)
  else:
    # Read the feed from file
    fg = unpickle_fg()

  # Add feed entry
  fe = fg.add_entry()
  fe.id("some id")
  fe.title('Status')

  content_rows = " "
  for service, color in services.items():
    content_rows += light_string.format(service=service, color=color)

  fe.content('<table>' + content_rows + '</table>')
  fe.pubdate(datetime.now(tzlocal()))

  # Evict oldest entry if too long
  orig_entries = fg.entry()
  entries = [ (e.pubdate(), e) for e in orig_entries]

  for _ in range(len(orig_entries)):
    fg.remove_entry(0)

  entries.sort(reverse=True, key=lambda x: x[0])

  for i, t in enumerate(entries[:5]):
    pubdate, e = t
    print(pubdate)
    fg.add_entry(e)

  # Save the feed to file
  pickle_fg(fg)

  # Write the rss XML file
  fg.rss_file('../accre.github.io/feed.xml', pretty=True)
  fg.rss_file('feed.xml', pretty=True)



if __name__ == "__main__":

  main()
