"""
Documentacion del pipe
"""


class pipe():
    """
    Esta clase crea al pipe
    """

    def hablar(self, tema):
        """
        Con esto habla el pipe

        Parameters:
        tema (str): este es un string que define el que del cual va a hablar el pipe

        Returns:
        devuelve 1 si habla bien del tema, de lo contrario devuelve 0
        """

        print(f'Hola soy el pipenv, y vamos a hablar del tema: {tema}')

    def seAburre(self, tema):
        """

        """

        print(f"Me aburri de hablar del tema: {tema}")
