from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.entidades.cliente import Cliente
from pynfe.entidades.emitente import Emitente
from pynfe.entidades.notafiscal import NotaFiscal
from pynfe.entidades.fonte_dados import _fonte_dados
from pynfe.processamento.serializacao import SerializacaoXML
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.utils.flags import CODIGO_BRASIL
from decimal import Decimal
import datetime

certificado = "KESCK COURO LTDA_12790431000188.pfx"
senha = 'Jesiel1401'
uf = 'sc'
homologacao = False

# emitente
emitente = Emitente(
    razao_social='KESCK COURO LTDA',
    nome_fantasia='KESCK',
    cnpj='12790431000188',           # cnpj apenas números
    codigo_de_regime_tributario='1', # 1 para simples nacional ou 3 para normal
    inscricao_estadual='260674664', # numero de IE da empresa
    #inscricao_municipal='12345',
    cnae_fiscal='4772500',           # cnae apenas números
    endereco_logradouro='Rua Candeias',
    endereco_numero='28',
    endereco_bairro='Floresta',
    endereco_municipio='Joinville',
    endereco_uf='SC',
    endereco_cep='89212406',
    endereco_pais=CODIGO_BRASIL
)

# cliente

cliente = Cliente(
    razao_social='Flavia Carvalho Rodrigues',
    tipo_documento='CPF',           #CPF ou CNPJ
    #email='email@email.com',
    numero_documento='39597908808', # numero do cpf ou cnpj
    indicador_ie=9,                 # 9=Não contribuinte 
    endereco_logradouro='rua eliseu visconte',
    endereco_numero='113',
    #endereco_complemento='Ao lado de lugar nenhum',
    endereco_bairro='Loteamento Villa Branca',
    endereco_municipio='Jacarei',
    endereco_uf='SP',
    endereco_cep='12301605',
    endereco_pais=CODIGO_BRASIL,
    #endereco_telefone='11912341234',
)

# Nota Fiscal
nota_fiscal = NotaFiscal(
   emitente=emitente,
   cliente=cliente,
   uf=uf.upper(),
   natureza_operacao='VENDA', # venda, compra, transferência, devolução, etc
   forma_pagamento=0,         # 0=Pagamento à vista; 1=Pagamento a prazo; 2=Outros.
   tipo_pagamento=1,
   modelo=55,                 # 55=NF-e; 65=NFC-e
             # Número do Documento Fiscal.
   data_emissao=datetime.datetime.now(),
   data_saida_entrada=datetime.datetime.now(),
   tipo_documento=1,          # 0=entrada; 1=saida
   municipio='4209102',       # Código IBGE do Município 
   tipo_impressao_danfe=1,    # 0=Sem geração de DANFE;1=DANFE normal, Retrato;2=DANFE normal Paisagem;3=DANFE Simplificado;4=DANFE NFC-e;
   forma_emissao='1',         # 1=Emissão normal (não em contingência);
              # 0=Normal;1=Consumidor final;
   indicador_intermediador=0,
   finalidade_emissao='1',    # 1=NF-e normal;2=NF-e complementar;3=NF-e de ajuste;4=Devolução de mercadoria.
   processo_emissao='0',      #0=Emissão de NF-e com aplicativo do contribuinte;
   transporte_modalidade_frete=1,
   informacoes_adicionais_interesse_fisco='',
   totais_tributos_aproximado=Decimal(0.04*347.65),
   indicador_presencial=2,


   serie='1',
   numero_nf='5000', 
   indicador_destino=2,
   cliente_final=1,
)

# Produto
nota_fiscal.adicionar_produto_servico(
    codigo='Amber Rouge',                           # id do produto
    descricao='Orientica Luxury Collection Amber Rouge Edp 80ml',
    ncm='33030020',
    #cest='0100100',                            # NT2015/003
    cfop='6102',
    unidade_comercial='UN',
    ean='SEM GTIN',
    ean_tributavel='SEM GTIN',
    quantidade_comercial=Decimal('1'),        # 12 unidades
    valor_unitario_comercial=Decimal('347.65'),  # preço unitário
    valor_total_bruto=Decimal('347.65'),       # preço total
    unidade_tributavel='UN',
    quantidade_tributavel=Decimal('1'),
    valor_unitario_tributavel=Decimal('347.65'),
    ind_total=1,
    # numero_pedido='12345',                   # xPed
    # numero_item='123456',                    # nItemPed
    icms_modalidade='102',
    icms_origem=0,
    icms_csosn='400',
    pis_modalidade='07',
    cofins_modalidade='07',
    valor_tributos_aprox=str(round(0.04*347.65,2))
    )

# responsável técnico
nota_fiscal.adicionar_responsavel_tecnico(
    cnpj='12790431000188',
    contato='Kesck',
    email='kesckword@gmail.com',
    fone='11944588170'
  )

# exemplo de nota fiscal referenciada (devolução/garantia)
# nfRef = NotaFiscalReferenciada(
#     chave_acesso='99999999999999999999999999999999999999999999')
# nota_fiscal.notas_fiscais_referenciadas.append(nfRef)

# exemplo de grupo de pessoas autorizadas a baixar xml
# autxml_lista = ['99999999000199', '00000000040']
# for index, item in enumerate(autxml_lista, 1):
#    nota_fiscal.adicionar_autorizados_baixar_xml(CPFCNPJ=item)

# serialização
serializador = SerializacaoXML(_fonte_dados, homologacao=homologacao)
nfe = serializador.exportar()

# assinatura
a1 = AssinaturaA1(certificado, senha)
xml = a1.assinar(nfe)

# envio
con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
envio = con.autorizacao(modelo='nfe', nota_fiscal=xml)

# em caso de sucesso o retorno será o xml autorizado
# Ps: no modo sincrono, o retorno será o xml completo (<nfeProc> = <NFe> + <protNFe>)
# no modo async é preciso montar o nfeProc, juntando o retorno com a NFe  
from lxml import etree
if envio[0] == 0:
  print('Sucesso!')
  print(etree.tostring(envio[1], encoding="unicode").replace('\n','').replace('ns0:','').replace(':ns0', ''))
# em caso de erro o retorno será o xml de resposta da SEFAZ + NF-e enviada
else:
  print('Erro:')
  print(envio[1].text) # resposta
  print('Nota:')
  print(etree.tostring(envio[2], encoding="unicode")) # nfe