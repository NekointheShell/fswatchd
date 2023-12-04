import argparse
import yaml
import threading
import inotify.adapters
import logging
import systemd.journal


def parseargs():
    parser = argparse.ArgumentParser(prog = 'fswatchd', description = 'Watches for FS events.')

    parser.add_argument('-c', '--config', default = '/etc/fswatchd.yaml', help = 'Path to configuration file.')
    return parser.parse_args()


def readconfig(config_file_path):
    config_file = open(config_file_path, 'r')
    config = yaml.safe_load(config_file)
    config_file.close()

    return config


def watch(path, logger):
    notify = inotify.adapters.InotifyTree(path['path'])
    for event in notify.event_gen():
        if event != None:
            tolog = False
            for operation in path['operations']:
                if operation in event[1] or operation == 'all': tolog = True

            if tolog == True:
                logger.info('{}: {}/{}'.format(event[1], event[2], event[3]))


def main():
    args = parseargs()
    config = readconfig(args.config)

    logger = logging.getLogger(__name__)
    logger.addHandler(systemd.journal.JournalHandler())
    logger.setLevel(logging.INFO)

    threads = []
    for path in config:
        watch_thread = threading.Thread(target = watch, args = [path, logger])
        watch_thread.start()

        threads.append(watch_thread)


if __name__ == '__main__': main()
