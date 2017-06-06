import asyncio


async def ping(target):
    create =  asyncio.create_subprocess_exec('ping', '-c', '10', target,
                                          stdout=asyncio.subprocess.PIPE)
    proc = await create
    lines = []
    while True:
        line = await proc.stdout.readline()
        if line == b'':
            break
        l = line.decode('utf8').rstrip()
        lines.append(l)
    transmited, received = [int(a.split(' ')[0]) for a
                            in lines[-2].split(', ')[:2]]
    stats, unit = lines[-1].split(' = ')[-1].split(' ')
    min_, avg, max_, stddev = [float(a) for a in stats.split('/')]
    return transmited, received, unit, min_, avg, max_, stddev


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    ping = loop.run_until_complete(ping('free.fr'))
    print(ping)

    loop.close()