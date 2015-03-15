import time
import re
import inflect

p = inflect.engine()

def format_message(message):
	#pattern = r'^:.*\!~(.*)@.* (.*) (.*) :(.*)'
	pattern = r'^:.*\!(.*)@.* (.*) (.*) :(.*)'
	now = int(time.time())
	matches = re.match(pattern, message)
	if not matches:
		return ''

	nick    = matches.group(1).strip()
        command = matches.group(2).strip()
        channel = matches.group(3).strip()
	message = matches.group(4).strip()

	return "%s\t%s\t%s\t%s\t%s" % (now, nick, command, channel, message)

def prettyTime(time):
    m, s = divmod(time, 60)
    if m > 0:
        h, m = divmod(m, 60)
        if h > 0:
            return p.no("hour", h) + ", "+ p.no("minute", m) + " and " + p.no("second", s)
        else:
            return p.no("minute", m) + " and " + p.no("second", s)
    else:
        return p.no("second", s)
