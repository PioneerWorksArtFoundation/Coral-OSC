import click
from oscpy.server import OSCThreadServer
from time import sleep

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def onReceiveMessageCallback(*argv):
    print(argv)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    '-ip', '--ip-address', 'ip_address',
    default=None,
    required=True,
    help="Used to specify the port that's listening for request on the OSC server handling these OSC messages."
)
@click.option(
    '-p', '--port', 'port',
    default=None,
    required=True,
    help="Used to specify the port that's listening for request on the OSC server handling these OSC messages."
)
@click.option(
    '--path', 'path',
    default='/',
    required=True,
    help="Path (endpoint) at which the OSC server is listening for requests."
)
def main(ip_address, port, path):
    osc = OSCThreadServer(encoding="utf8")
    osc.listen(address=ip_address, port=int(port), default=True)
    osc.bind(path, onReceiveMessageCallback)
    sleep(1000)
    osc.stop()


if __name__ == '__main__':
    main()
