class DomainException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class EmailAlreadyExistsException(DomainException):
    def __init__(self, email: str = ""):
        super().__init__("E-mail já cadastrado.", status_code=409)


class InvalidCredentialsException(DomainException):
    def __init__(self):
        super().__init__("Credenciais inválidas.", status_code=401)


class NoKnowledgeBaseException(DomainException):
    def __init__(self):
        super().__init__(
            "Nenhum texto base carregado. Envie um texto primeiro.", status_code=422
        )


class SessionNotFoundException(DomainException):
    def __init__(self):
        super().__init__("Sessão de chat não encontrada.", status_code=404)
