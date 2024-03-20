
from typing import Any, List, Optional, Tuple
import matplotlib.pyplot as plt
import networkx as nx
import graphviz
from graphviz import Digraph
from PIL import Image
from IPython.display import display


class avl_Node(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVLTree(object):

    def insert_node(self, root, value):

        if not root:
            return avl_Node(value)
        elif value < root.value:
            root.left = self.insert_node(root.left, value)
        else:
            root.right = self.insert_node(root.right, value)

        root.height = 1 + max(self.avl_Height(root.left),
                              self.avl_Height(root.right))

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

        return root

    def avl_Height(self, root):
        if not root:
            return 0
        return root.height

    def avl_BalanceFactor(self, root):
        if not root:
            return 0
        return self.avl_Height(root.left) - self.avl_Height(root.right)

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

    def leftRotate(self, b):
        a = b.right
        T2 = a.left
        a.left = b
        b.right = T2
        b.height = 1 + max(self.avl_Height(b.left),
                           self.avl_Height(b.right))
        a.height = 1 + max(self.avl_Height(a.left),
                           self.avl_Height(a.right))
        return a

    def rightRotate(self, b):
        a = b.left
        T3 = a.right
        a.right = b
        b.left = T3
        b.height = 1 + max(self.avl_Height(b.left),
                           self.avl_Height(b.right))
        a.height = 1 + max(self.avl_Height(a.left),
                           self.avl_Height(a.right))
        return a

    def to_dot(self, root, dot):
        if root is not None:
            dot.node(str(root.value))
            if root.left is not None:
                dot.edge(str(root.value), str(root.left.value))
                self.to_dot(root.left, dot)
            if root.right is not None:
                dot.edge(str(root.value), str(root.right.value))
                self.to_dot(root.right, dot)

    def plot_tree(self,root):
        dot = graphviz.Digraph(format='png')
        dot.graph_attr['size'] = '15,15'
        dot.node_attr['width'] = '1.5'
        dot.node_attr['height'] = '1.5'
        dot.node_attr['fontsize'] = '16'
        dot.node_attr['fontname'] = 'Helvetica-Bold'
        self.to_dot(root, dot)
        dot.render('avl_tree', format='png', cleanup=True)


        img = Image.open('avl_tree.png')
        display(img)

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
        node = Tree.find_node(root, value)

        if not node:
            print(f"El nodo {value} no existe en el árbol.")
            return None

        height_left = self.avl_Height(node.left)
        height_right = self.avl_Height(node.right)

        balance_factor = height_right - height_left
        print(f"Factor de balanceo del nodo {value}: {balance_factor}")
        return None

    #de este metdodo depende el encontrar el factor de balance de un nodo
    def find_node(self, root, value):
        if root is None:
            return None
        elif root.value == value:
            return root
        elif value < root.value:
            return self.find_node(root.left, value)
        else:
            return self.find_node(root.right, value)


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

#______________________________________________________________________________________________________________________________

Tree = AVLTree()
root = None
root = Tree.insert_node(root, 'bike_001')
root = Tree.insert_node(root, 'bike_071')
root=Tree.insert_node(root,'bike_080')
root=Tree.insert_node(root,'bike_081')
root=Tree.insert_node(root,'bike_082')
root=Tree.insert_node(root,'bike_062')
root=Tree.insert_node(root,'bike_063')
root=Tree.insert_node(root,'bike_085')
root=Tree.insert_node(root,'bike_084')
root=Tree.insert_node(root,'bike_065')
root=Tree.insert_node(root,'bike_066')
root=Tree.insert_node(root,'bike_053')
root=Tree.insert_node(root,'bike_163')
root=Tree.insert_node(root,'bike_092')
root=Tree.insert_node(root,'bike_005')
root=Tree.insert_node(root,'bike_002')
root=Tree.insert_node(root,'bike_003')
root=Tree.insert_node(root,'bike_004')
root=Tree.insert_node(root,'bike_010')
root=Tree.insert_node(root,'bike_013')
root=Tree.insert_node(root,'bike_056')
root=Tree.insert_node(root,'bike_900')
root=Tree.insert_node(root,'bike_146')
root=Tree.insert_node(root,'bike_087')
root=Tree.insert_node(root,'bike_027')
root=Tree.insert_node(root,'bike_041')
root=Tree.insert_node(root,'bike_050')
root=Tree.insert_node(root,'bike_0')






ima=Tree.plot_tree(root)
ima.show()