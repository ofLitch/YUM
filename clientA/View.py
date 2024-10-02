class View:
    def show(self, data):
        user_inputs = {}
        print("Response: ", data.get("answer"))
        isForm = data.get("add the data", False)

        if isForm != False:
            data = data["add the data"]
            print("Por favor, ingrese la siguiente información:")   
            for field in data:
                if field != ('answer', '200 OK'):
                    user_input = input(f"Ingrese el {field}: ")
                    user_inputs[field] = user_input  # Guardar la entrada del usuario en un diccionario
                else:
                    print(field)
        else:
            print("No hay formulario para mostrar")
        return user_inputs

    def show_menu(self, menu_data):
        print(menu_data.get("topic", "---Menu---"))
        
        # Iterar sobre las opciones del menú
        options = menu_data.get("options", [])
        if isinstance(options, list):
            for option in options:
                print(option)
        else:
            print(options)
        
        # Solicitar selección
        selection = input(menu_data.get("select", "Select an option: "))
        return selection
    
    def showMsg(self, msg):
        print(msg)
    
    def  showMsgToUser(self):
        msg = input("Write a msg: ")
        return msg
    
    def showInfo(self, info):
        for key, value in info.items():
            print(f"{key}: {value}")