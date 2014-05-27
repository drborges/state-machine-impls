class InvalidTransition(Exception):
  pass

class Transition:
  def __init__(self, from_state='', to_state='', listeners=[]):
    self.from_state = from_state
    self.to_state = to_state
    self._listeners = listeners

  def accepts(self, from_state, to_state):
    return self.from_state == from_state and self.to_state == to_state

  def notify_listeners(self, data):
    for listener in self._listeners:
      listener(data)

class StateMachine:
  def __init__(self, transition_handler=None, transitions=[]):
    self.transitions = transitions
    self.transition_handler = transition_handler

  def transition(self, data):
    def apply(from_state, to_state):
      transition = next((t for t in self.transitions if t.accepts(from_state, to_state)), None)

      if transition:
        if self.transition_handler:
          self.transition_handler(data, transition)

        transition.notify_listeners(data)
        return transition

      raise InvalidTransition('%s -> %s' % (from_state, to_state))

    return apply