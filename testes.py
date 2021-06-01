import os
import unittest

from main import Balance, Usuario, Server
class TestBalance(unittest.TestCase):

    def setUp(self):
        writer_input = open('teste_in.txt', 'w')
        writer_input.write('4\n')
        writer_input.write('2\n')
        writer_input.write('1\n')
        writer_input.write('3\n')
        writer_input.write('0\n')
        writer_input.write('1\n')
        writer_input.write('0\n')
        writer_input.write('1')
        writer_input.close()

        self.reader = open('teste_in.txt', 'r')
        self.balanceamento_carga = Balance(self.reader, open('teste_out.txt', 'w'), )

        Usuario.ttask = int(self.reader.readline())  # Ler e define ttask
        Server.umax = int(self.reader.readline())  # Ler e define umax

    def tearDown(self):
        self.balanceamento_carga.reader.close()
        self.balanceamento_carga.writer.close()
        os.remove('teste_in.txt')
        os.remove('teste_out.txt')

    def test_le_linhas(self):
        tick = self.balanceamento_carga.le_linhas()
        self.assertEqual(tick, 1)

    def test_w_resultado(self):
        self.balanceamento_carga.novos_usuarios(1)
        self.assertEqual(self.balanceamento_carga.w_resultado(), '1\n')

    def test_existe_vaga(self):
        self.balanceamento_carga.novos_usuarios(1)
        self.balanceamento_carga.custo_Server = len(self.balanceamento_carga.servers)
        self.assertEqual(self.balanceamento_carga.conta_us_ativo(), 1)
        self.assertEqual(self.balanceamento_carga.servers[0].existe_vaga(), True)
        self.assertEqual(self.balanceamento_carga.custo_Server, 1)
        self.balanceamento_carga.novos_usuarios(1)
        self.balanceamento_carga.custo_Server = len(self.balanceamento_carga.servers)
        self.assertEqual(self.balanceamento_carga.servers[0].existe_vaga(), False)
        self.assertEqual(self.balanceamento_carga.conta_us_ativo(), 2)
        self.assertEqual(self.balanceamento_carga.custo_Server, 1)
        self.balanceamento_carga.novos_usuarios(1)
        self.balanceamento_carga.custo_Server = len(self.balanceamento_carga.servers)
        self.assertEqual(self.balanceamento_carga.custo_Server, 2)

    def test_exclui_tick_us_serv(self):
        self.balanceamento_carga.novos_usuarios(1)
        self.balanceamento_carga.exclui_tick_us_serv()
        self.assertEqual(self.balanceamento_carga.servers[0].usuarios[0].faltam_ttask, 3)

        for i in range(Usuario.ttask - 1):
            self.balanceamento_carga.exclui_tick_us_serv()

        self.assertEqual(self.balanceamento_carga.conta_us_ativo(), 0)
        self.assertEqual(len(self.balanceamento_carga.servers), 0)

    def test_cria_balance_saida(self):
        self.balanceamento_carga.cria_balance()

        self.assertEqual(self.balanceamento_carga.qtd_usuario, 0)
        self.assertEqual(self.balanceamento_carga.custo, 15)

        self.balanceamento_carga.writer.close()
        self.balanceamento_carga.writer = open('teste_out.txt', 'r')
        read_output = self.balanceamento_carga.writer.read()
        self.assertEqual(read_output, '1\n2,2\n2,2\n2,2,1\n1,2,1\n2\n2\n1\n1\n0\n15')


if __name__ == '__main__':
    unittest.main()
