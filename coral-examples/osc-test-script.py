import click
from time import sleep
from oscpy.client import OSCClient

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


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
    osc = OSCClient(ip_address, int(port), encoding="utf8")
    while(True):
        osc.send_message(path, "hello")
        print("Sent message!\n\n")
        sleep(1)


if __name__ == '__main__':
    main()
