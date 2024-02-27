from __future__ import annotations
from typing import TypeVar, Iterable, Generic, List, Callable, Set, Deque, Any, Optional
from typing_extensions import Protocol
T = TypeVar('T')

def linear_contains(iterable: Iterable[T], key: T) -> bool:
  for item in iterable:
    if item == key:
      return True
  return False

C = TypeVar("C", bound="Comparable")

class Comparable(Protocol):
  def __eq__(self, other: Any) -> bool:
    ...

  def __lt__(self: C, other: C) -> bool:
    ...

  def __gt__(self: C, other: C) -> bool:
    return (not self < other) and self != other

  def __le__(self: C, other: C) -> bool:
    return self < other or self == other

  def __ge__(self: C, other: C) -> bool:
    return not self < other


class Node(Generic[T]):
  def __init__(self, state: T, parent: Optional[Node], cost: float = 0.0,
  heuristic: float = 0.0) -> None:
    self.state: T = state
    self.parent: Optional[Node] = parent
    self.cost: float = cost
    self.heuristic: float = heuristic
  def __lt__(self, other: Node) -> bool:
    return (self.cost + self.heuristic) < (other.cost + other.heuristic)


class Queue(Generic[T]):
  def __init__(self) -> None:
    self._container: Deque[T] = Deque()

  @property
  def empty(self) -> bool:
    return not self._container # negação é verdadeira para um contêiner vazio
  def push(self, item: T) -> None:
    self._container.append(item)
  def pop(self) -> T:
    return self._container.popleft() # FIFO
  def __repr__(self) -> str:
    return repr(self._container)

def node_to_path(node: Node[T]) -> List[T]:
  path: List[T] = [node.state]
  # trabalha no sentido inverso, do final para o início
  while node.parent is not None:
    node = node.parent
    path.append(node.state)
  path.reverse()
  return path


def bfs(initial: T, goal_test: Callable[[T], bool], successors:
  Callable[[T], List[T]]) -> Optional[Node[T]]:
    # frontier corresponde aos lugares que ainda devemos visitar
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    # explored representa os lugares em que já estivemos
    explored: Set[T] = {initial}
    # continua enquanto houver mais lugares para explorar
    while not frontier.empty:
      current_node: Node[T] = frontier.pop()
      current_state: T = current_node.state
      # se encontrarmos o objetivo, terminamos
      if goal_test(current_state):
       return current_node
      # verifica para onde podemos ir em seguida e que ainda não tenha sido explorado
      for child in successors(current_state):
        #print('antes')
        if child in explored: # ignora os filhos que já tenham sido explorados
          #print("Depois - Oloco meu")
          continue
        explored.add(child)
        frontier.push(Node(child, current_node))
    return None # passamos por todos os lugares e não atingimos o objetivo
