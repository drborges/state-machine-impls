import unittest

from mock import Mock
from sure import expect
from nose.tools import raises, nottest

from statemachine import StateMachine, Transition, InvalidTransition

class TestStateMachine(unittest.TestCase):

  def test_it_accepts_transition_from_state_a_to_state_b(self):
    transition_a_b = Transition(from_state='A', to_state='B')
    statemachine = StateMachine(transitions=[transition_a_b])

    transition = statemachine.transition({ 'data': 'some data' })(from_state='A', to_state='B')

    expect(transition).to.be.equal(transition_a_b)

  def test_it_allows_for_lazy_execution(self):
    transition_a_b = Transition(from_state='A', to_state='B')
    statemachine = StateMachine(transitions=[transition_a_b])

    apply_transition = statemachine.transition({ 'data': 'some data' })
    transition = apply_transition(from_state='A', to_state='B')

    expect(transition).to.be.equal(transition_a_b)

  def test_it_notifies_listeners(self):
    listener1 = Mock()
    listener2 = Mock()

    statemachine = StateMachine(transitions=[
      Transition('A', 'B'),
      Transition('A', 'C', [listener1, listener2]),
    ])

    data = { 'data': 'some data' }
    statemachine.transition(data)(from_state='A', to_state='C')

    listener1.assert_called_with(data)
    listener2.assert_called_with(data)

  def test_it_calls_no_transition_handler_when_transition_is_invalid(self):
    handler = Mock()

    StateMachine(no_transition=handler).transition({})('A', 'C')

    handler.assert_called_with('A', 'C')

  def test_it_returns_none_when_transition_is_invalid(self):
    transition = StateMachine().transition({})('A', 'C')

    expect(transition).to.be.none