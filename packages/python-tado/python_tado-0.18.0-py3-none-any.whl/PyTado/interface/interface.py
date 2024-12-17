"""
PyTado interface abstraction to use app.tado.com or hops.tado.com
"""

from PyTado.http import Http
import PyTado.interface.api as API


class Tado:
    """Interacts with a Tado thermostat via public API.

    Example usage: t = Tado('me@somewhere.com', 'mypasswd')
                   t.get_climate(1) # Get climate, zone 1.
    """

    def __init__(
        self,
        username: str,
        password: str,
        http_session=None,
        debug: bool = False,
    ):
        """Class Constructor"""

        self._http = Http(
            username=username,
            password=password,
            http_session=http_session,
            debug=debug,
        )

        if self._http.is_x_line:
            self._api = API.TadoX(http=self._http, debug=debug)
        else:
            self._api = API.Tado(http=self._http, debug=debug)

    def __getattr__(self, name):
        """Delegiert den Aufruf von Methoden an die richtige API-Client-Implementierung."""
        return getattr(self.client, name)
