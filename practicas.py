import json
import webbrowser
import os

class Token:
    def __init__(self, id, lexema):
        self.id = id
        self.lexema = lexema

lista_personas = []

def lexico(comando):
    estado = 0
    char = '' #caracter actual
    next_char = '' #caracter siguiente
    lexema = ""
    cont_comillas = 0
    lista_tokens = []
    for i in range(len(comando)):
        char = comando[i]
        #print(estado, ":", char,":\tLexema: ", lexema)
        try:
            next_char = comando[i+1]
        except:
            next_char = " "

        if(estado == 0): #ESTADO -------------------------------------------------------------- 0
            if (char.isalpha()):
                if (next_char.isalpha() or next_char.isdigit() or next_char == "_"): #RECONOCE PALABRAS RESERVADAS E IDENTIFICADORES
                    estado = 1
                    lexema = lexema + char       
                else:
                    estado = 0
                    lexema = lexema + char
                    lista_tokens.append(Token("identificador", lexema))
                    lexema = ""
            elif (char == '"'):
                estado = 2
                cont_comillas = 1 
            elif (char == ','):
                estado = 0
                lexema = lexema + char
                lista_tokens.append(Token("coma", lexema))
                lexema = ""
            elif (char == '*'):
                estado = 0
                lexema = lexema + char
                lista_tokens.append(Token("asterisco", lexema))
                lexema = ""
            elif (char == '='):
                estado = 0
                lexema = lexema + char
                lista_tokens.append(Token("igual", lexema))
                lexema = ""
            elif (char.isdigit()): # RECONOCE LOS NÃšMEROS
                if (next_char.isdigit() or next_char == "."):
                    estado = 3
                    lexema = lexema + char
                else:
                    estado = 0
                    lexema = lexema + char
                    lista_tokens.append(Token("numero", lexema))
                    lexema = ""
            elif (char.isspace()): # IGNORAR LOC ESPACIOS
                estado = 0  
        elif (estado == 1): #ESTADO --------------------------------------------------------- 1
            if (next_char.isalpha() or  next_char.isdigit() or next_char == "_"):
                lexema = lexema + char
                estado = 1
            else:
                #AGREGARLOS
                #nombre, edad, promedio, arctivo
                lexema = lexema + char                
                if (lexema.lower() == "cargar"):
                    estado = 0
                    lista_tokens.append(Token("pr_cargar", lexema))
                    lexema = ""
                elif (lexema.lower() == "seleccionar"):
                    estado = 0
                    lista_tokens.append(Token("pr_seleccionar", lexema))
                    lexema = ""
                elif (lexema.lower() == "donde"):
                    estado = 0
                    lista_tokens.append(Token("pr_donde", lexema))
                    lexema = ""
                elif (lexema.lower() == "maximo"):
                    estado = 0
                    lista_tokens.append(Token("pr_maximo", lexema))
                    lexema = ""
                elif (lexema.lower() == "minimo"):
                    estado = 0
                    lista_tokens.append(Token("pr_minimo", lexema))
                    lexema = ""
                elif (lexema.lower() == "suma"):
                    estado = 0
                    lista_tokens.append(Token("pr_suma", lexema))
                    lexema = ""
                elif (lexema.lower() == "cuenta"):
                    estado = 0
                    lista_tokens.append(Token("pr_cuenta", lexema))
                    lexema = ""
                elif (lexema.lower() == "reportar"):
                    estado = 0
                    lista_tokens.append(Token("pr_reportar", lexema))
                    lexema = ""
                elif (lexema.lower() == "nombre"):
                    estado = 0
                    lista_tokens.append(Token("pr_nombre", lexema))
                    lexema = ""
                elif (lexema.lower() == "edad"):
                    estado = 0
                    lista_tokens.append(Token("pr_edad", lexema))
                    lexema = ""
                elif (lexema.lower() == "promedio"):
                    estado = 0
                    lista_tokens.append(Token("pr_promedio", lexema))
                    lexema = ""
                elif (lexema.lower() == "activo"):
                    estado = 0
                    lista_tokens.append(Token("pr_activo", lexema))
                    lexema = ""
                else: 
                    estado = 0
                    lista_tokens.append(Token("identificador", lexema))
                    lexema = ""
        elif (estado == 2):#ESTADO -----------------------------------------------------------2
            if(cont_comillas == 1 and char == '"'):
                estado = 0                
                lista_tokens.append(Token("cadena", lexema))
                lexema = ""
                cont_commillas = 0
            else:
                lexema = lexema + char
                estado = 2
        elif (estado == 3):
            if (next_char.isdigit() or next_char == "."):
                estado = 3
                lexema = lexema + char
            else:
                estado = 0
                lexema = lexema + char
                lista_tokens.append(Token("numero", lexema))
                lexema = ""
    #for i in range(len(lista_tokens)): 
    #    print(lista_tokens[i].id, "\t:\t", lista_tokens[i].lexema)
    #lista_tokens = []
    return lista_tokens
    
def seleccionador(lista):
    if(lista[0].id == "pr_cargar"):
        lista.pop(0)
        ejecutar_cargar(lista)

    if(lista[0].id == "pr_seleccionar"):
        lista.pop(0)
        ejecutar_seleccionar(lista)

    if(lista[0].id == "pr_maximo"):
        ejecutar_maximo(lista[1].id)

    if(lista[0].id == "pr_minimo"):
        ejecutar_minimo(lista[1].id)

    if(lista[0].id == "pr_suma"):
        ejecutar_suma(lista[1].id)

    if(lista[0].id == "pr_cuenta"):
        ejecutar_cuenta()
    
    if(lista[0].id == "pr_reportar"):
        ejecutar_report(int(lista[1].lexema))

def ejecutar_report(n):    
    global lista_personas
    tabla = ""    
    for i in range(0,n):
        tabla += "<tr>"
        tabla += "<td>" + lista_personas[i]['nombre'] +"</td>"
        tabla += "<td>" + str(lista_personas[i]['edad']) +"</td>"
        tabla += "<td>" + str(lista_personas[i]['activo']) +"</td>"
        tabla += "<td>" + str(lista_personas[i]['promedio']) +"</td>"
        tabla += "</tr>"
    html = '<html><head><title>Reporte de Registros</title><head><body style = "padding:50px;background-color:#ECE0F8;"><h1 align="center">Reporte de Personas</h1><center><table border= "1"><tr><td>Nombre</td><td>Edad</td>'
    html += '<td>Activo</td><td>Promedio</td><tr>'+tabla+'</table></center></body></html>'
    f = open("reporte.html", "w")
    f.write(html)    
    f.close()
    os.system("start reporte.html")


def ejecutar_cuenta():
    global lista_personas
    print("Cantidad de Resistros: ", len(lista_personas))

def ejecutar_suma(atributo):
    global lista_personas
    if(atributo == "pr_edad"):
        suma = 0
        for persona in lista_personas:
            suma += persona['edad']
        print("Suma de edad es: ", suma)
    else:
        suma = 0
        for persona in lista_personas:
            suma += persona['promedio']
        print("Suma de promedio es: ", suma)

def ejecutar_maximo(atributo):
    global lista_personas
    if(atributo == "pr_edad"):
        array = [] # La Edad de Todos los Registros Se gurdan aquí 
        for persona in lista_personas:
            array.append(persona['edad'])
        array.sort()
        array.reverse()
        print("Máxima edad es: ", array[0])
    else:
        array = [] 
        for persona in lista_personas:
            array.append(persona['promedio'])
        array.sort()
        array.reverse()
        print("Máximo promedio es: ", array[0])

def ejecutar_minimo(atributo):
    global lista_personas
    if(atributo == "pr_edad"):
        array = [] # La Edad de Todos los Registros Se gurdan aquí 
        for persona in lista_personas:
            array.append(persona['edad'])
        array.sort()        
        print("Mínimo edad es: ", array[0])
    else:
        array = [] 
        for persona in lista_personas:
            array.append(persona['promedio'])
        array.sort()       
        print("Mínimo promedio es: ", array[0])

def  ejecutar_seleccionar(lista):
    global lista_personas
    atributos = []
    condicion = []
    estado = 0
    for token in lista:
        if(token.id != "coma" and token.id != "igual"):
            if(token.id == "pr_donde"):
                estado = 1
            elif(estado != 1):
                atributos.append(token)
            if(estado == 1 and token.id != "pr_donde"):
                condicion.append(token)
    if(len(atributos) == 1 and atributos[0].id == "asterisco"):
        for persona in lista_personas:
            if(str(persona[condicion[0].lexema.lower()]) == condicion[1].lexema):                  
                print("Resultado: ", persona)
    else:
        resultado = ""
        for persona in lista_personas:
            if(str(persona[condicion[0].lexema.lower()]) == condicion[1].lexema):                 
                for token in atributos:
                    resultado += token.lexema.lower() + " : " + str(persona[token.lexema.lower()]) + ", "
        print("Resultado: {", resultado, " }")

def ejecutar_cargar(lista):
    global lista_personas # Usar Variable Global 
    lista_archivos = []
    for i in range(0, len(lista)):
        if(lista[i].id == "identificador"):
            lista_archivos.append(lista[i].lexema)
    for i in range(0, len(lista_archivos)):
        csv_file = open(lista_archivos[i]+".json", "r") #Leer
        texto = csv_file.read()
        arr_json = json.loads(texto)
        unir_personas(arr_json)
        csv_file.close()
    for i in range(0, len(lista_personas)):
        print(lista_personas[i])

def unir_personas(lista):
    global lista_personas
    for i in range(0, len(lista)):
        lista_personas.append(lista[i])

def main():
    comando = ""
    while(True):
        comando = input("Eliga comando a utilizar: ")        
        seleccionador(lexico(comando))
        if(comando == "salir"):
            exit()
    #analizador("CARGAR archivo1, archivo_2, archivo3")

if __name__ == "__main__":
    main()

