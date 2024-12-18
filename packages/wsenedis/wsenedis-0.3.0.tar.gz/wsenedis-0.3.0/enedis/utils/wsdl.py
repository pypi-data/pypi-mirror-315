from pathlib import Path

script_dir = Path(__file__).parent.parent.parent
ressources_path = script_dir / 'ressources'

SERVICES = {x.stem: x.resolve().as_posix() for x in ressources_path.glob("**/*.wsdl")}

def wsdl(service_name: str) -> str:
    """Return path to WSDL file for `service_name`."""
    try:
        return SERVICES[service_name]
    except KeyError:
        raise KeyError(
            "Unknown service name {!r}, available services are {}".format(
                service_name,
                ", ".join(sorted(SERVICES)),
            ),
        ) from None


