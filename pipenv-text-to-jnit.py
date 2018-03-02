#!/usr/bin/env python3

import sys
import re
from pathlib import Path

# ensure argument exists
if len(sys.argv) < 2:
  print("Usage: %s [path_to_inputfile]" % sys.argv[0])
  sys.exit()


# ensure file exists
if not Path(sys.argv[1]).is_file():
  print("%s does not exists!" % sys.argv[1])
  exit()


# begin reading file
header_counter = 0
message = ""

input_file = open(sys.argv[1], 'r')
output_file = open('results.xml', 'w+')
output_file.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
output_file.write('<testsuites>\n\t<testsuite>\n')
for line in input_file:
  line = line.rstrip()

  # check for header
  matchObj = re.match(r'\d+: (.+)!', line, re.M)

  if matchObj:

    # print message for previous issue
    if header_counter > 0:
      output_file.write('\t\t\t<failure message="%s">\n\t\t\t</failure>\n\t\t</testcase>\n' % message)

    # print header for current issue
    output_file.write('\t\t<testcase name="%s">\n' % matchObj.group(1))
    message = ""
    header_counter += 1
  else:
    message = message + "\n" + line

# print message for last detected issue
if header_counter > 0:
  output_file.write('\t\t\t<failure message="%s">\n\t\t\t</failure>\n\t\t</testcase>\n' % message)

output_file.write('\t</testsuite>\n</testsuites>\n')

# close files
output_file.close()
input_file.close()
