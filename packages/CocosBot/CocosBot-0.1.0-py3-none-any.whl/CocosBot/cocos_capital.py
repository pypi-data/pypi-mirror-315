from playrightbrowser import PlaywrightBrowser
from exctract_2fa_from_gmail import obtener_codigo_2FA
import logging
from urls import WEB_APP_URLS, API_URLS


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CocosCapital(PlaywrightBrowser):

    def __init__(self, username, password, gmail_user, gmail_app_pass, headless=False):
        super().__init__(headless)
        self.username = username
        self.password = password
        self.gmail_user = gmail_user
        self.gmail_app_pass = gmail_app_pass

    def login(self):
        """Realiza el login en Cocos Capital."""
        try:
            self.go_to(WEB_APP_URLS["login"], "Navegando al login...")
            self.fill_input('input[type="email"]', self.username, "Llenando el email...")
            self.fill_input('input[type="password"]', self.password, "Llenando la contraseña...")
            self.click_element('button[type="submit"]', "Enviando formulario de login...")
            self.handle_two_factor_authentication()
            self.handle_save_device_prompt()
            logger.info("Login exitoso.")
        except Exception as e:
            logger.error("Error durante el proceso de login: %s", e)
            self.close_browser()
            raise

    def handle_two_factor_authentication(self):
        """Maneja la autenticación de dos factores."""
        self.wait_for_element('div._inputs_cxnwh_23',
                              log_message="Esperando pantalla de autenticación de dos factores.")

        code = obtener_codigo_2FA(self.gmail_user, self.gmail_app_pass, 'no-reply@cocos.capital')
        if not code or len(code) != 6:
            logger.error("No se pudo obtener un código 2FA válido.")
            raise ValueError("No se pudo obtener un código 2FA válido.")

        logger.info("Código 2FA obtenido: %s", code)

        for i, digit in enumerate(code):
            self.fill_input(f'input#input{i}', digit, f"Ingresando dígito {i+1} del código 2FA...")

        logger.info("Código 2FA ingresado automáticamente.")

    def handle_save_device_prompt(self):
        """Maneja la pantalla de guardar el dispositivo como seguro."""
        try:
            self.click_element(
                'button:has-text("Sí, guardar como dispositivo seguro")',
                log_message="Guardando dispositivo como seguro...",
                timeout=5000
            )
        except Exception:
            logger.warning("No apareció la pantalla de guardar dispositivo.")

    def fetch_data(self, request_url, navigation_url, process_response=None, timeout=10000):
        """
        Intercepta un request específico y procesa su respuesta.
        """
        try:
            self.go_to(navigation_url, f"Navegando a {navigation_url} para obtener datos...")

            with self.page.expect_response(request_url) as response_info:
                logger.info(f"Esperando la respuesta de {request_url}...")
                response = response_info.value

            logger.info("Respuesta interceptada: URL=%s, Estado=%s", response.url, response.status)
            if response.status == 200:
                try:
                    data = response.json()
                    logger.debug("Contenido de la respuesta (JSON): %s", data)
                    if process_response:
                        return process_response(data)
                    else:
                        return data
                except Exception as e:
                    logger.error("No se pudo decodificar el JSON de la respuesta: %s", e)
            else:
                logger.warning("No se pudo capturar la respuesta del request específico.")
                return None
        except Exception as e:
            logger.error("Error general en fetch_data: %s", e)
            return None

    def fetch_portfolio_balance(self):
        """
        Obtiene el total balance desde el endpoint de portafolio.

        Returns:
            float: Valor de 'totalBalance' o None si no se encuentra.
        """

        def process_response(response):
            """Procesa la respuesta del balance y extrae 'totalBalance'."""
            total_balance = response.get('totalBalance')
            if total_balance is not None:
                logger.info("Total Balance obtenido con éxito: %s", total_balance)
            else:
                logger.warning("El campo 'totalBalance' no está presente en la respuesta.")
            return total_balance

        return self.fetch_data(API_URLS["portfolio_balance"], WEB_APP_URLS["portfolio"], process_response)

    def get_mep_value(self):
        """
        Obtiene el valor MEP desde el endpoint correspondiente.

        Returns:
            dict: Respuesta completa del endpoint MEP.
        """
        return self.fetch_data(API_URLS["mep_prices"], WEB_APP_URLS["portfolio"])

    def get_user_data(self):
        """
        Obtiene los datos del usuario desde el endpoint /api/v1/users/me.

        Returns:
            dict: Diccionario con los datos del usuario o None si falla.
        """

        def process_response(response):
            """Procesa la respuesta y extrae los datos del usuario."""
            logger.info("Datos del usuario obtenidos con éxito.")
            return response

        return self.fetch_data(API_URLS["user_data"], WEB_APP_URLS["dashboard"], process_response)

    def logout(self):
        """
        Realiza el logout de la aplicación de Cocos Capital.

        Returns:
            bool: True si el logout fue exitoso, False en caso contrario.
        """
        try:
            # Navegar a la página principal
            self.go_to(WEB_APP_URLS["dashboard"], "Navegando al dashboard para cerrar sesión...")

            # Seleccionar el ícono de logout
            logout_selector = 'svg.lucide-log-out'
            self.click_element(logout_selector, "Haciendo clic en el botón de logout...")

            # Confirmar que se redirigió a la página de inicio de sesión
            self.wait_for_element('input[type="email"]', log_message="Confirmando logout exitoso...")
            logger.info("Logout realizado con éxito.")
            return True
        except Exception as e:
            logger.error(f"Error durante el proceso de logout: {e}")
            return False

