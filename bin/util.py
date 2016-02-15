#!/usr/bin/python

import random
import json
import inflect

p = inflect.engine()

def genID(digits=5):
    # makes a string of digits

    id = ""
    x  = 0
    while x < digits:
        id += str(random.randint(0,9))
        x += 1

    return id

def sum_res(res):
    # takes a dict of str res and int quantities, returns int sum

    total = 0
    for x in res:
        total += res.get(x)

    return total

def pretty_dict(indict):
    print(json.dumps(indict, sort_keys=True, indent=2, separators=(",", ":")))

def pretty_time(time):
    m, s = divmod(time, 60)
    if m > 0:
        h, m = divmod(m, 60)
        if h > 0:
            d, h = divmod(h, 24)
            if d > 0:
                w, d = divmod(d, 7)
                if w > 0:
                    mo, w = divmod(w, 4)
                    if mo > 0:
                        return p.no("month", mo) + ", " + p.no("week", w) +", " + p.no("day", d) + ", " + p.no("hour", h) + ", "+ p.no("minute", m) + " and " + p.no("second", s)
                    else:
                        return p.no("week", w) +", " + p.no("day", d) + ", " + p.no("hour", h) + ", "+ p.no("minute", m) + " and " + p.no("second", s)
                else:
                    return p.no("day", d) + ", " + p.no("hour", h) + ", "+ p.no("minute", m) + " and " + p.no("second", s)
            else:
                return p.no("hour", h) + ", "+ p.no("minute", m) + " and " + p.no("second", s)
        else:
            return p.no("minute", m) + " and " + p.no("second", s)
    else:
        return p.no("second", s)
