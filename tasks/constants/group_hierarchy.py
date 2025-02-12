# Definição da hierarquia dos grupos
GROUP_HIERARCHY = {
    "User": 1,      # Nível mais baixo
    "Manager": 2,   # Pode ver todas as tarefas, mas só edita/deleta as suas
    "Admin": 3      # Pode fazer tudo
}


STATUS_PROFILE = {
    "user_green": 10,
    "user_yellow": 20,
    "user_red": 30,
    "consultor": 40,
    "admin": 50,
}

STATUS_PROFILE_ENUM ={
    "user_green": "Usuário - Verde",
    "user_yellow": "Usuário - Amarelo",
    "user_red": "Usuário - Vermelho",
    "consultor": "Consultor",
    "admin": "Administrador",
}