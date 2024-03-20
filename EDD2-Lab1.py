
import matplotlib.pyplot as plt
import networkx as nx
import os

class avl_Node(object):
    def __init__(self, value, depth=0):  
        self.value = value
        self.left = None
        self.right = None
        self.height = 1
        self.depth = depth 
        
class AVLTree(object):
    def __init__(self):
       
        self.root = None
        self.nodes_by_type = {}    # Listas para almacenar nodos por tipo.

    # Método para insertar un nuevo nodo en el árbol AVL.
    def insert_node(self, root, value):
        
        if not root:
            root = avl_Node(value)  
        elif value < root.value:
            root.left = self.insert_node(root.left, value)
        else:
            root.right = self.insert_node(root.right, value)

        # Actualizar la altura del nodo actual
        root.height = 1 + max(self.avl_Height(root.left), self.avl_Height(root.right))

        # Rebalancear el árbol si es necesario
        balanceFactor = self.avl_BalanceFactor(root)
        if balanceFactor > 1:
            if value < root.left.value:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)

        if balanceFactor < -1:
            if value > root.right.value:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)

        return root   #La raíz del subárbol después de la inserción.

    def delete_node(self, root, value):
        if not root:
            return root

        # Realizar la eliminación del nodo 
        if value < root.value:
            root.left = self.delete_node(root.left, value)
        elif value > root.value:
            root.right = self.delete_node(root.right, value)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.avl_MinValue(root.right)
            root.value = temp.value
            root.right = self.delete_node(root.right, temp.value)

        # Actualizar la altura del nodo actual
        root.height = 1 + max(self.avl_Height(root.left), self.avl_Height(root.right))

        # Calcular el factor de equilibrio del nodo actual
        balanceFactor = self.avl_BalanceFactor(root)

        # Rebalancear el árbol si es necesario
        if balanceFactor > 1:
            if self.avl_BalanceFactor(root.left) >= 0:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)
        if balanceFactor < -1:
            if self.avl_BalanceFactor(root.right) <= 0:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)

        return root

    # Método para obtener la altura de un nodo en el árbol AVL.
    def avl_Height(self, root):
        if not root:
            return 0
        return root.height

    # Método para obtener el factor de balanceo de un nodo en el árbol AVL.    
    def avl_BalanceFactor(self, root):
        if not root:
            return 0
        return self.avl_Height(root.left) - self.avl_Height(root.right)
    
    # Método para encontrar el nodo con el valor mínimo en el árbol AVL.
    def avl_MinValue(self, root):
        if root is None or root.left is None:
            return root
        return self.avl_MinValue(root.left)

    def preOrder(self, root):
        if not root:
            return
        print("{0} ".format(root.value), end=" ")
        self.preOrder(root.left)
        self.preOrder(root.right)

    def inOrder(self, root):
        if root:
            self.inOrder(root.left)
            print("{0} ".format(root.value), end=" ")
            self.inOrder(root.right)

    def postOrder(self, root):
        if root:
            self.postOrder(root.left)
            self.postOrder(root.right)
            print("{0} ".format(root.value), end=" ")
        
    # Método para realizar un recorrido por niveles en el árbol AVL de manera recursiva.
    def level_order_recursive(self,root):
      height = self.avl_Height(root)
      for level in range(0, height + 1):
        self.print_level(root, level)

    
    # Método auxiliar para imprimir los nodos de un nivel específico en el árbol AVL de manera recursiva.
    def print_level(self,node, level):
      if node is None:
        return
      if level == 0:
        print(node.value)
      elif level > 0:
        self.print_level(node.left, level - 1)
        self.print_level(node.right, level - 1)    

    # Método para realizar una rotación hacia la izquierda en el árbol AVL.
    def leftRotate(self, b):
        a = b.right
        T2 = a.left
        a.left = b
        b.right = T2
        b.height = 1 + max(self.avl_Height(b.left), self.avl_Height(b.right))
        a.height = 1 + max(self.avl_Height(a.left), self.avl_Height(a.right))
        return a

   # Método para realizar una rotación hacia la derecha en el árbol AVL.
    def rightRotate(self, b):
        a = b.left
        T3 = a.right
        a.right = b
        b.left = T3
        b.height = 1 + max(self.avl_Height(b.left), self.avl_Height(b.right))
        a.height = 1 + max(self.avl_Height(a.left), self.avl_Height(a.right))
        return a

    # Método para visualizar el árbol binario AVL.
    def visualize_binary_tree(self, root):
        G = nx.DiGraph()
        self._build_graph(G, root)
        pos = self.draw_vertical_tree(G, root)

        for node in G.nodes:
            tipo = node.lower()  # Convertir el nombre del nodo a minúsculas para evitar errores de comparación
            if tipo.startswith('bike'):
                image_path = f'C:/ArchivosLab1/DataEDD2/data/bike/{node}.bmp'
            elif tipo.startswith('car'):
                image_path = f'C:/ArchivosLab1/DataEDD2/data/cars/{node}.bmp'
            elif tipo.startswith('cat'):
                image_path = f'C:/ArchivosLab1/DataEDD2/data/cats/{node}.jpg'
            elif tipo.startswith('dog'):
                image_path = f'C:/ArchivosLab1/DataEDD2/data/dogs/{node}.jpg'
            elif tipo.startswith('0'):
                image_path = f'C:/ArchivosLab1/DataEDD2/data/flowers/{node}.png'
            elif tipo.startswith('horse'):
                image_path = f'C:/ArchivosLab1/DataEDD2/data/horses/{node}.jpg'
            elif tipo.startswith('rider'):
                image_path = f'C:/ArchivosLab1/DataEDD2/data/human/{node}.jpg'
            else:
                print(f"Tipo de nodo no reconocido: {tipo}")
                continue

            G.nodes[node]['image_path'] = image_path  # Asignar la ruta a los nodos

        nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=11, font_weight="bold")

        # Manejar clics en los nodos
        plt.gcf().canvas.mpl_connect('button_press_event', lambda event: self._on_click(event, G))

        plt.show()

    # Método auxiliar para construir el grafo para la visualización del árbol.
    def _build_graph(self, G, root):
        if root is not None:
            if root.left:
                G.add_edge(root.value, root.left.value)
                self._build_graph(G, root.left)
            if root.right:
                G.add_edge(root.value, root.right.value)
                self._build_graph(G, root.right)

    def inOrderTraversal(self, root):
        if root:
            yield from self.inOrderTraversal(root.left)
            yield root
            yield from self.inOrderTraversal(root.right)

    def draw_vertical_tree(self, G, root, x=0, y=0, spacing=1):
        if root is not None:
            # Calcular la posición y para el nodo actual en función de su profundidad
            depth = self.get_max_depth(root)
            y_position = -depth * spacing

            # Asignar la posición x al nodo actual
            G.nodes[root.value]['pos'] = (x, y_position)

            # Calcular la posición x para los hijos del nodo actual
            if root.left:
                # La posición x para el hijo izquierdo se ajusta hacia la izquierda
                self.draw_vertical_tree(G, root.left, x - spacing, y, spacing / 2)
            if root.right:
                # La posición x para el hijo derecho se ajusta hacia la derecha
                self.draw_vertical_tree(G, root.right, x + spacing, y, spacing / 2)

            # Construir el grafo agregando aristas entre nodos
            self._build_graph(G, root)

            # Ajustar la separación entre nodos en el mismo nivel después de asignar las posiciones
            if root.left and root.right:
                sibling_spacing = abs(G.nodes[root.left.value]['pos'][0] - G.nodes[root.right.value]['pos'][0])
                spacing = sibling_spacing / 2

            # Calcular la posición x para los hijos del nodo actual después de ajustar la separación
            if root.left:
                self.draw_vertical_tree(G, root.left, x - spacing, y, spacing / 2)
            if root.right:
                self.draw_vertical_tree(G, root.right, x + spacing, y, spacing / 2)

        return nx.get_node_attributes(G, 'pos')




   # Método para obtener la máxima profundidad del árbol.
    def get_max_depth(self, root):
        if root is None:
            return 0
        else:
            left_depth = self.get_max_depth(root.left)
            right_depth = self.get_max_depth(root.right)
            return max(left_depth, right_depth) + 1

   # Método para manejar clics en los nodos del árbol.
    def _on_click(self, event, G):
        if event.inaxes is None:
            return
        for node in G.nodes:
            if G.nodes[node]['pos'][0] - 0.05 < event.xdata < G.nodes[node]['pos'][0] + 0.05 and G.nodes[node]['pos'][1] - 0.05 < event.ydata < G.nodes[node]['pos'][1] + 0.05:
                image_path = G.nodes[node].get('image_path')
                if image_path:
                    image = plt.imread(image_path)
                    fig, ax = plt.subplots()
                    ax.imshow(image)
                    plt.show()
                break
    
    def get_node_level(self, root, value):
        if root is None:
            print("El árbol está vacío.")
            return None  # Si el árbol está vacío, no hay niveles

        queue = [(root, 0)]  # Utilizamos una cola para recorrer el árbol nivel por nivel

        while queue:
            current_node, level = queue.pop(0)  # Sacamos el primer nodo de la cola

            if current_node.value == value:
                if level == 0:
                    print("El nodo con valor", value, "es la raíz del árbol.")
                else:
                    print("El nodo con valor", value, "está en el nivel", level, "del árbol.")
                return None  # Devolvemos el nivel del nodo si encontramos el valor

            if current_node.left:
                queue.append((current_node.left, level + 1))  # Agregamos el hijo izquierdo a la cola

            if current_node.right:
                queue.append((current_node.right, level + 1))  # Agregamos el hijo derecho a la cola

        print("El nodo con valor", value, "no existe en el árbol.")
        return None  # Devolvemos -1 si el valor no se encuentra en el árbol


    def avl_BalanceFactor_node(self, value):
        node = Tree.search_node(root, value)

        if not node:
            print(f"El nodo {value} no existe en el árbol.")
            return None

        height_left = self.avl_Height(node.left)
        height_right = self.avl_Height(node.right)

        balance_factor = height_right - height_left
        print(f"Factor de balanceo del nodo {value}: {balance_factor}")
        return None

    #de este metdodo depende el encontrar el factor de balance de un nodo        
    def search_node(self, root, value):
            if root is None or root.value == value:
                return root

            if root.value < value:
                return self.search_node(root.right, value)

            return self.search_node(root.left, value)

    #metodo para mostrar por pantalla el padre de un nodo
    def find_parent_node(self, root, value):
      if root is None or root.value == value:
        print(f"No se encontró un nodo padre para {value}")
        return None # No hay padre para la raíz o el valor está en la raíz

    # Verificar si el valor está en el subárbol izquierdo
      if root.left and root.left.value == value:
        print(f"El nodo padre de {value} es: {root.value}")
        return  None

    # Verificar si el valor está en el subárbol derecho
      if root.right and root.right.value == value:
        print(f"El nodo padre de {value} es: {root.value}")
        return None

    # Buscar recursivamente en el subárbol izquierdo
      if value < root.value:
        return self.find_parent_node(root.left, value)

    # Buscar recursivamente en el subárbol derecho
      if value > root.value:
        return self.find_parent_node(root.right, value)

    # No se encontró un nodo padre
      print(f"No se encontró un nodo padre para {value}")
      return None


    #metodo de base para la busqueda de abuelo y tio
    def find_parent_node_usage(self, root, value):
      if root is None or root.value == value:
        return None # No hay padre para la raíz o el valor está en la raíz

    # Verificar si el valor está en el subárbol izquierdo
      if root.left and root.left.value == value:
        return  root

    # Verificar si el valor está en el subárbol derecho
      if root.right and root.right.value == value:
        return root

    # Buscar recursivamente en el subárbol izquierdo
      if value < root.value:
        return self.find_parent_node(root.left, value)

    # Buscar recursivamente en el subárbol derecho
      if value > root.value:
        return self.find_parent_node(root.right, value)




    def find_grandparent_node(self, root, value):
      # Primero, encuentra el nodo padre del nodo dado.
        parent = self.find_parent_node_usage(root, value)
        if parent:# Si se encontró un nodo padre, busca el nodo abuelo del nodo padre.
            grandparent = self.find_parent_node_usage(root, parent.value)
            if grandparent: # Si no se encontró un nodo abuelo, imprime un mensaje y devuelve None.
                print(f"El abuelo de {value} es: {grandparent.value}")
                return None
            else: # Si no se encontró un nodo abuelo, imprime un mensaje y devuelve None.
                print(f"No se encontró un abuelo para {value}")
                return None
        else:# Si no se encontró un nodo padre para el valor dado, imprime un mensaje y devuelve None.
            print(f"No se encontró un nodo padre para {value}, no se puede encontrar el abuelo.")
            return None

    def find_uncle_node(self, root, value):
    # Encontrar el nodo padre del nodo dado.
      parent = self.find_parent_node_usage(root, value)

      if parent:
        # Si se encontró un nodo padre, buscar el nodo abuelo del nodo padre.
        grandparent = self.find_parent_node_usage(root, parent.value)

        if grandparent:
            # Si se encontró un nodo abuelo, determinar cuál es el tío del nodo dado.
            if grandparent.left == parent:
                # Si el padre es el hijo izquierdo del abuelo, el tío es el hijo derecho del abuelo.
                uncle = grandparent.right
            else:
                # Si el padre es el hijo derecho del abuelo, el tío es el hijo izquierdo del abuelo.
                uncle = grandparent.left

            if uncle:
                # Si se encontró un tío, imprimir su valor y devolverlo.
                print(f"El tío de {value} es: {uncle.value}")
                return None
            else:
                # Si no se encontró un tío, imprimir un mensaje y devolver None.
                print(f"No se encontró un tío para {value}")
                return None
        else:
            # Si no se encontró un abuelo, imprimir un mensaje y devolver None.
            print(f"No se encontró un abuelo para {value}, no se puede encontrar el tío.")
            return None
      else:
        # Si no se encontró un nodo padre, imprimir un mensaje y devolver None.
        print(f"No se encontró un nodo padre para {value}, no se puede encontrar el tío.")
        return None
    
def obtener_tamano_imagen(image_path):
    try:
        size = os.path.getsize(image_path)
        return size
    except FileNotFoundError:
        print(f"No se encontró la imagen en: {image_path}")
        return None   
    

Tree = AVLTree()
root = None
while True:
    tipo = input("Ingrese el tipo de valor del 1er nodo (Bike, Car, Cat, Dog, Flower, Horse, Human): ")
    if tipo in ['Bike', 'Car', 'Cat', 'Dog', 'Flower', 'Horse', 'Human']:
        break
    else:
        print("\nTipo de nodo inválido. Inténtalo de nuevo.")

valor = input(f"\nIngrese el valor del 1er nodo: ")
root = Tree.insert_node(root, valor)

# Guardar el nodo en el diccionario por tipo
tipo = tipo.lower()
if tipo not in Tree.nodes_by_type:
    Tree.nodes_by_type[tipo] = []
Tree.nodes_by_type[tipo].append(valor)


while True:
    print("\nMenú de Opciones:\n")
    print("1. Agregar Nodo ")
    print("2. Eliminar Nodo por su Nombre ")
    print("3. Buscar Nodo por su Nombre ")
    print("4. Buscar Nodos por su tipo y tamaño" )
    print("5. Recorrido del arbol (recursivos) ")
    print("6. Salir")
    o=int(input( "\nElija una de las opciones: "))

    if (o==1):
        while True:
            agregar_mas = input("\n¿Desea agregar otro nodo? (si/no): ")
            if agregar_mas.lower() == 'si':
                while True:
                    tipo_nodo = input("\nIngrese el tipo del nodo a agregar (Bike, Car, Cat, Dog, Flower, Horse, Human): ")
                    if tipo_nodo in ['Bike', 'Car', 'Cat', 'Dog', 'Flower', 'Horse', 'Human']:
                        break
                    else:
                        print("\nTipo de nodo inválido. Inténtalo de nuevo.")
                valor_nodo = input(f"\nIngrese el valor del nodo a agregar: ")
                root = Tree.insert_node(root, valor_nodo)

                # Guardar el nodo en las listas por tipo
                tipo_nodo = tipo_nodo.lower()
                if tipo_nodo not in Tree.nodes_by_type:
                    Tree.nodes_by_type[tipo_nodo] = []
                Tree.nodes_by_type[tipo_nodo].append(valor_nodo)

                Tree.visualize_binary_tree(root) #Visualizar arbol despues de agregar el nodo
            elif agregar_mas.lower() == 'no':
                break
            else:
                print("\nOpción inválida. Inténtalo de nuevo.")
    elif (o == 2):
        while True:
            eliminar_mas = input("\n¿Desea eliminar un nodo por su nombre? (si/no): ")
            if eliminar_mas.lower() == 'si':
                
                tipo_nodo = input("\nIngrese el tipo del nodo a eliminar (Bike, Car, Cat, Dog, Flower, Horse, Human): ").lower()
                valor_nodo = input("\nIngrese el nombre del nodo a eliminar: ")
                
                if tipo_nodo in Tree.nodes_by_type:
                    if valor_nodo in Tree.nodes_by_type[tipo_nodo]:
                        root = Tree.delete_node(root, valor_nodo)
                        
                        Tree.visualize_binary_tree(root) #Visualizar arbol despues de elimanar el nodo


                        # Eliminar el nombre del nodo de la lista correspondiente
                        Tree.nodes_by_type[tipo_nodo].remove(valor_nodo)
                        print(f"\nEl nodo {valor_nodo} de tipo {tipo_nodo} ha sido eliminado.")
                    else:
                        print(f"\nNo se encontró el nodo {valor_nodo} de tipo {tipo_nodo}.")
                else:
                    print(f"\nNo se encontraron nodos del tipo {tipo_nodo}.")
            elif eliminar_mas.lower() == 'no':
                break
            else:
                print("Opción inválida. Inténtalo de nuevo.")

    elif (o == 3):
        while True:
            buscar_mas = input("\n¿Desea buscar un nodo por su nombre? (si/no): ")
            if buscar_mas.lower() == 'si':
                valor_nodo = input("\nIngrese el valor/nombre del nodo a buscar: ")
                
                # Realizar la búsqueda del nodo en el árbol AVL
                found_node = Tree.search_node(root, valor_nodo)
                if found_node:
                    print(f"\nEl nodo con valor {valor_nodo} se encontró en el árbol.")
                    ver_operaciones = input("\n¿Desea ver las operaciones disponibles para este nodo? (si/no): ")
                    if ver_operaciones.lower() == 'si':
                        while True:
                            print("\nOperaciones disponibles:")
                            print("a. Obtener el nivel del nodo.")
                            print("b. Obtener el factor de balanceo (equilibrio) del nodo.")
                            print("c. Encontrar el padre del nodo.")
                            print("d. Encontrar el abuelo del nodo.")
                            print("e. Encontrar el tío del nodo.")
                            print("f. Volver al menú principal.")
                            operacion = input("Seleccione una operación: ")

                            if operacion == 'a':
                                level = Tree.get_node_level(root, valor_nodo)
                            elif operacion == 'b':
                                balance_factor = Tree.avl_BalanceFactor_node(valor_nodo)
                            elif operacion == 'c':
                                parent = Tree.find_parent_node(root, valor_nodo)
                            elif operacion == 'd':
                                grandparent = Tree.find_grandparent_node(root, valor_nodo)
                            elif operacion == 'e':
                                uncle = Tree.find_uncle_node(root, valor_nodo)
                            elif operacion == 'f':
                                break
                            else:
                                print("\nOperación no válida. Inténtalo de nuevo.")
                else:
                    print(f"\nNo se encontró ningún nodo con valor {valor_nodo} en el árbol.")
                    
            elif buscar_mas.lower() == 'no':
                break
            else:
                print("\nOpción inválida. Inténtalo de nuevo.")

    elif o == 4:
        tipo_buscado = input("\nIngrese el tipo de nodo que desea buscar (Bike, Car, Cat, Dog, Flower, Horse, Human): ").lower()
        if tipo_buscado in Tree.nodes_by_type:
            print(f"\nNodos de tipo {tipo_buscado}:")
            for i, node_name in enumerate(Tree.nodes_by_type[tipo_buscado]):
                print(f"{i+1}. {node_name}")

            # Pedir al usuario que ingrese el rango de tamaño
            min_size = int(input("\nIngrese el tamaño mínimo en bytes: "))
            max_size = int(input("Ingrese el tamaño máximo en bytes: "))

            # Crear una lista para almacenar los nodos que cumplen con el filtro de tamaño
            nodos_filtrados = []

            # Recorrer la lista de nodos del tipo especificado
            for node_name in Tree.nodes_by_type[tipo_buscado]:
                # Obtener la ruta de la imagen para el nodo
                tipo = tipo_buscado.lower()
                if tipo.startswith('bike'):
                    image_path = f'C:/ArchivosLab1/DataEDD2/data/bike/{node_name}.bmp'
                elif tipo.startswith('car'):
                    image_path = f'C:/ArchivosLab1/DataEDD2/data/cars/{node_name}.bmp'
                elif tipo.startswith('cat'):
                    image_path = f'C:/ArchivosLab1/DataEDD2/data/cats/{node_name}.jpg'
                elif tipo.startswith('dog'):
                    image_path = f'C:/ArchivosLab1/DataEDD2/data/dogs/{node_name}.jpg'
                elif tipo.startswith('0'):
                    image_path = f'C:/ArchivosLab1/DataEDD2/data/flowers/{node_name}.png'
                elif tipo.startswith('horse'):
                    image_path = f'C:/ArchivosLab1/DataEDD2/data/horses/{node_name}.jpg'
                elif tipo.startswith('rider'):
                    image_path = f'C:/ArchivosLab1/DataEDD2/data/human/{node_name}.jpg'
                else:
                    print(f"Tipo de nodo no reconocido: {tipo}")
                    continue

                # Obtener el tamaño de la imagen
                size = obtener_tamano_imagen(image_path)
                if size is not None:
                    # Verificar si el tamaño está dentro del rango especificado
                    if min_size <= size <= max_size:
                        nodos_filtrados.append(node_name)

            # Mostrar la lista de nodos que cumplen con el filtro
            print("\nNodos que cumplen con el filtro de tamaño:")
            for i, node_name in enumerate(nodos_filtrados):
                print(f"{i+1}. {node_name}")

            # Permitir al usuario seleccionar un nodo para realizar operaciones adicionales
            seleccion = input("\nSeleccione el número del nodo que desea explorar (o '0' para volver al menú principal): ")
            if seleccion.isdigit():
                seleccion = int(seleccion)
                if seleccion == 0:
                    continue
                elif 1 <= seleccion <= len(nodos_filtrados):
                    valor_nodo = nodos_filtrados[seleccion - 1]
                    print(f"\nHa seleccionado el nodo '{valor_nodo}'.")
                    
                    ver_operaciones = input("\n¿Desea ver las operaciones disponibles para este nodo? (si/no): ")
                    if ver_operaciones.lower() == 'si':
                        while True:
                            print("\nOperaciones disponibles:")
                            print("a. Obtener el nivel del nodo.")
                            print("b. Obtener el factor de balanceo (equilibrio) del nodo.")
                            print("c. Encontrar el padre del nodo.")
                            print("d. Encontrar el abuelo del nodo.")
                            print("e. Encontrar el tío del nodo.")
                            print("f. Volver al menú principal.")
                            operacion = input("Seleccione una operación: ")

                            if operacion == 'a':
                                level = Tree.get_node_level(root, valor_nodo)
                            elif operacion == 'b':
                                balance_factor = Tree.avl_BalanceFactor_node(valor_nodo)
                            elif operacion == 'c':
                                parent = Tree.find_parent_node(root, valor_nodo)
                            elif operacion == 'd':
                                grandparent = Tree.find_grandparent_node(root, valor_nodo)
                            elif operacion == 'e':
                                uncle = Tree.find_uncle_node(root, valor_nodo)
                            elif operacion == 'f':
                                break
                            else:
                                print("\nOperación no válida. Inténtalo de nuevo.")



                else:
                    print("\nNúmero de selección fuera de rango.")
            else:
                print("\nSelección no válida. Debe ingresar un número.")
        else:
            print(f"\nNo se encontraron nodos del tipo {tipo_buscado}.")    
    
    elif o == 5:
        while True:
            print("\nMenú de Recorridos Recursivos:")
            print("a. Preorden")
            print("b. Inorden")
            print("c. Postorden")
            print("d. Por niveles")
            print("e. Volver al menú principal")
            recorrido = input("Seleccione un tipo de recorrido: ")

            if recorrido == 'a':
                print("Recorrido Preorden:")
                Tree.preOrder(root)
            elif recorrido == 'b':
                print("Recorrido Inorden:")
                Tree.inOrder(root)
            elif recorrido == 'c':
                print("Recorrido Postorden:")
                Tree.postOrder(root)
            elif recorrido == 'd':
                print("Recorrido Por niveles:")
                Tree.level_order_recursive(root)
            elif recorrido == 'e':
                break
            else:
                print("\nOpción no válida. Inténtalo de nuevo.")

    elif(o==6):
        print("\nHa salido con exito.")
        break
    else:
        print("\nOpción invalida. Intente de nuevo")



