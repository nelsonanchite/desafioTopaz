class Usuario:
    ttask = 0
    def __init__(self, ):
        self.faltam_ttask = Usuario.ttask

    def exclui_tick(self):
        self.faltam_ttask -=1
        return self.faltam_ttask

class Server:
    umax = 0
    def __init__(self,usuarios):
        self.usuarios = usuarios

    def exclui_tick_usuario(self):
        self.usuarios[:] = [usuario for usuario in self.usuarios if usuario.exclui_tick()]
        return self.usuarios

    def existe_vaga(self):
        if len(self.usuarios) < Server.umax:
            return True
        else:
            return False

class Balance:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.custo = 0
        self.servers = []
        self.qtd_usuario = 0

    def exclui_tick_us_serv(self):
        self.servers[:] = [servidor for servidor in self.servers if servidor.exclui_tick_usuario()]

    def conta_us_ativo(self):
        count = 0
        for servidor in self.servers:
            count += len(servidor.usuarios)
        return count

    def novos_usuarios(self,quantidade_usuarios):
        for i in range(quantidade_usuarios):
            no_lugar = False
            for servidor in self.servers:
                if servidor.existe_vaga():
                    servidor.usuarios.append(Usuario())
                    no_lugar = True
            if no_lugar is False:
                self.servers.append(Server([Usuario()]))

    def cria_balance(self):
        lido = False
        while self.servers or not lido:
            novos = self.le_linhas()
            if novos is False and lido is False:
                lido = True

            if novos is not False:
                self.novos_usuarios(novos)

            self.w_resultado()
            self.custo += len(self.servers)
            self.exclui_tick_us_serv()

        self.w_resultado_final()

    def le_linhas(self):
        linha = self.reader.readline()
        if linha:
            return int(linha)
        else:
            return False

    def w_resultado(self):
        result = []
        for i, servidor in enumerate(self.servers):
            result.append(str(len(servidor.usuarios)))
        result = ','.join(result) +'\n'
        self.writer.write(result)
        return result

    def w_resultado_final(self):
        self.writer.write('\n'.join(str(self.conta_us_ativo())) + '\n')
        self.writer.write(str(self.custo))

def main():
    with open('input.txt', 'r') as reader, open('output.txt', 'w') as writer:
        balance = Balance(reader, writer)
        Usuario.ttask = int(reader.readline())
        Server.umax = int(reader.readline())
        balance.cria_balance()

if __name__ == '__main__':
    main()


