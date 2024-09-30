class View:
    def show(self, data):
        user_inputs = {}
        
        print("Por favor, ingrese la siguiente información:")
        for field in data:
            user_input = input(f"Ingrese el {field}: ")
            user_inputs[field] = user_input  # Guardar la entrada del usuario en un diccionario

        return user_inputs
