import datetime
import random
import sys
import time

LOG_PATH = "./batch.log"
log = open(LOG_PATH, "wa")

start = time.time()
progress = time.time()
count = 0

while progress - start < 180:
    log = open(LOG_PATH, "ab")
    progress = time.time()
#    time.sleep(0.1)
    timestamp = datetime.datetime.now()
    timestamp = timestamp.isoformat()
    value = random.randint(0,100)
#    print type(timestamp), type(value), type(sys.argv[1])
#    print "[%s][Random]: Application-id: %s: #%i\n" % (timestamp, sys.argv[1], value)
    if count % 60000 == 0:
        log.write("[%s][Random]: Application-id: %s: #%i\n" % (timestamp, sys.argv[1], value))
    log.close()
    count += 1

log = open(LOG_PATH, "ab")
log.write("[END]")
