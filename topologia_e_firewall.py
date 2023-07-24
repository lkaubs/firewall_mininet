from mininet.topo import Topo
import time

# Mini código para descobrir o dia e a hora do sistema

lista = time.ctime().split()

hora = int(lista[3].split(':')[0])

class Topo(Topo):
    def build(self):
        # Adiciona switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        # Adiciona hosts
        h1 = self.addHost('h1', ip='10.0.0.1')
        h2 = self.addHost('h2', ip='10.0.0.2')
        h3 = self.addHost('h3', ip='10.0.0.3')
        h4 = self.addHost('h4', ip='10.0.0.4')
        h5 = self.addHost('h5', ip='10.0.0.5')
        h6 = self.addHost('h6', ip='10.0.0.6')
        h7 = self.addHost('h7', ip='10.0.0.7')
        h8 = self.addHost('h8', ip='10.0.0.8')
        h9 = self.addHost('h9', ip='10.0.0.9')
        h10 = self.addHost('h10', ip='10.0.0.10')
        
        #interfaces para os hosts
        #switch1

        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        self.addLink(h4, s1)

        #switch2
        
        self.addLink(h5, s2)
        self.addLink(h6, s2)
        self.addLink(h7, s2)
        self.addLink(h8, s2)
        #switch3
        
        self.addLink(h9, s3)
        
        #switch4
                
        self.addLink(h10, s4)
        self.addLink(s4, s1)
        self.addLink(s4, s2)
        self.addLink(s4, s3)

class RegrasOpenFlow(object):
    def __init__(self, net):
        self.net = net

    def set_rules(self):
        # Obtenha os switchs da rede
        s4 = self.net.get('s4')
        # Regras que vão estar no switch s4 durante os dias de trabalho
        if not (lista[0] == 'Sat' or lista[0]== 'Sun') and 8 < hora < 18:
            print('Dia de semana e horário de trabalho, acesso à rede social bloqueado')
            s4.cmd('ovs-ofctl add-flow s4 in_port=1,action=output:4')
        else:
            print('Não é horário nem dia de trabalho, acesso à rede social liberado')
        for c in range(4):
            s = self.net.get(f's{c+1}')
            s.cmd(f'ovs-ofctl add-flow s{c+1} action=normal')

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch

def cria_topologia():
    # Cria a instância do Mininet com um controlador OpenFlow padrão e switches OpenFlow
    net = Mininet(controller=RemoteController, switch=OVSSwitch, topo=Topo())

    # Inicia a rede
    net.start()

    # Instancia a classe para adicionar as regras de OpenFlow
    regras_openflow = RegrasOpenFlow(net)
    regras_openflow.set_rules()

    # Inicie a CLI do Mininet
    net.interact()

    # Encerre a rede
    net.stop()

if __name__ == '__main__':
    cria_topologia()
