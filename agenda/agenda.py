from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import mysql.connector
from reportlab.pdfgen import canvas

# Conexão com o banco de dados
banco = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="agenda"
)

# Função para cadastrar contatos
def cadastrarContatos():
    campoNome = agenda.lineEdit_2.text()
    campoEmail = agenda.lineEdit_3.text()
    campoTelefone = agenda.lineEdit_4.text()

    if agenda.radioButton.isChecked():
        tipoTelefone = "Residencial"
    elif agenda.radioButton_2.isChecked():
        tipoTelefone = "Celular"
    else:
        tipoTelefone = "Não informado"

    try:
        cursor = banco.cursor()
        comando_sql = "INSERT INTO contatos (nome, email, telefone, tipoTelefone) VALUES (%s, %s, %s, %s)"
        dados = (campoNome, campoEmail, campoTelefone, tipoTelefone)
        cursor.execute(comando_sql, dados)
        banco.commit()
        QMessageBox.information(None, 'Cadastro', 'Contato cadastrado com sucesso!')
    except Exception as e:
        QMessageBox.critical(None, 'Erro', f'Erro ao cadastrar contato: {e}') #Alert


# CONSULTAR CONTATOS
def consultarContatos():
    listarContatos.show()

    cursor = banco.cursor()
    comando_sql = "SELECT * FROM contatos"
    cursor.execute(comando_sql)
    contatosLidos = cursor.fetchall()

    listarContatos.tabelaContatos.setRowCount(len(contatosLidos))
    listarContatos.tabelaContatos.setColumnCount(5)

    for i in range (0, len(contatosLidos)):
        for f in range (0, 5):
            listarContatos.tabelaContatos.setItem(i, f, QtWidgets.QTableWidgetItem(str(contatosLidos[i] [f])))


# GERAR PDF
def gerarPdf():
    cursor = banco.cursor()
    comando_SQL = 'SELECT * FROM contatos'
    cursor.execute(comando_SQL)
    contatos_lidos = cursor.fetchall()
    
    y = 0
    pdf = canvas.Canvas("lista_contatos.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200, 800, "Lista de contatos")
    
    pdf.setFont("Times-Bold", 18)
    pdf.drawString(10, 750, "ID")
    pdf.drawString(110, 750, "NOME")
    pdf.drawString(210, 750, "EMAIL")
    pdf.drawString(410, 750, "TELEFONE")
    pdf.drawString(510, 750, "TIPO DE CONTATO")
    
    for i in range (0, len(contatos_lidos)):
        y = y + 50
        pdf.drawString(10, 750 - y, str(contatos_lidos[i][0]))
        pdf.drawString(110, 750 - y, str(contatos_lidos[i][1]))
        pdf.drawString(210, 750 - y, str(contatos_lidos[i][2]))
        pdf.drawString(410, 750 - y, str(contatos_lidos[i][3]))
        pdf.drawString(510, 750 - y, str(contatos_lidos[i][4]))
        
        pdf.save()
        print("PDF gerado com sucesso!")
        
        
# EXCLUIR CONTATO
def excluirContato():
    linhaContato = listarContatos.tabelaContatos.currentRow()
    listarContatos.tabelaContatos.removeRow(linhaContato)
    
    cursor = banco.cursor()
    comando_SQL = "SELECT id FROM contatos"
    cursor.execute(comando_SQL)
    contatos_lidos = cursor.fetchall()
    valorId = contatos_lidos[linhaContato][0]
    cursor.execute("DELETE FROM contatos WHERE id=" + str(valorId))
    banco.commit()
    
    
# ALTERAR CONTATO
def alterarContato():
    linhaContato = listarContatos.tabelaContatos.currentRow()

    # listarContatos.tabelaContatos.removeRow(linhaContato)
    
    cursor = banco.cursor()
    comando_SQL = "SELECT id FROM contatos"
    cursor.execute(comando_SQL)
    contatos_lidos = cursor.fetchall()
    valorId = contatos_lidos[linhaContato][0]

    nome = listarContatos.tabelaContatos.item(linhaContato, 1).text()
    email = listarContatos.tabelaContatos.item(linhaContato, 2).text()
    telefone = listarContatos.tabelaContatos.item(linhaContato, 3).text()
    tipoTelefone = listarContatos.tabelaContatos.item(linhaContato, 4).text()

    cursor.execute("UPDATE contatos SET nome=%s, email=%s, telefone=%s, tipoTelefone=%s WHERE id=%s",
                   (nome, email, telefone, tipoTelefone, valorId))
    banco.commit()
    
    # alterarContato.save()
    print("Contato alterado com sucesso!")


# VOLTAR
def voltar():
    listarContatos.hide()
    agenda.show()
    
    # cursor = banco.cursor()
    # comando_sql = "SELECT * FROM contatos"
    # cursor.execute(comando_sql)
    # contatosLidos = cursor.fetchall()

    # agenda.formLayout
    # listarContatos.tabelaContatos(agenda)
    # listarContatos.formLayout(agenda)

    print("De volta a tela inicial!")

    
    
# Configuração da aplicação PyQt
app = QtWidgets.QApplication([])
agenda = uic.loadUi("agenda.ui")
listarContatos = uic.loadUi("listarContatos.ui")

agenda.btnRegister.clicked.connect(cadastrarContatos)
agenda.btnConsultar.clicked.connect(consultarContatos)
listarContatos.btnAlterarContato.clicked.connect(alterarContato)
listarContatos.btnExcluir.clicked.connect(excluirContato)
listarContatos.btnGerarPdf.clicked.connect(gerarPdf)
listarContatos.btnVoltar.clicked.connect(voltar)
# listarContatos.btnVoltar.clicked.connect()

agenda.show()
# listarContatos.show()
app.exec_()
