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

  def test_it_handles_transition_through_callback(self):
    transition_handler = Mock()
    statemachine = StateMachine(transition_handler, transitions=[Transition('A', 'B')])

    data = 'some data'
    transition = statemachine.transition(data)(from_state='A', to_state='B')

    transition_handler.assert_called_with(data, transition)

  def test_it_allows_for_lazy_execution(self):
    transition_a_b = Transition(from_state='A', to_state='B')
    statemachine = StateMachine(transitions=[transition_a_b])

    apply_transition = statemachine.transition({ 'data': 'some data' })
    transition = apply_transition(from_state='A', to_state='B')

    expect(transition).to.be.equal(transition_a_b)

  def test_it_notify_listeners(self):
    listener1 = Mock()
    listener2 = Mock()

    statemachine = StateMachine(transitions=[
      Transition('A', 'B'),
      Transition('A', 'C', [listener1, listener2]),
    ])

    data = { 'data': 'some data' }
    transition = statemachine.transition(data)(from_state='A', to_state='C')

    listener1.assert_called_with(data)
    listener2.assert_called_with(data)

  @raises(InvalidTransition)
  def test_it_raises_exception_when_transition_is_invalid(self):
    StateMachine([Transition('A', 'B')]).transition({})('A', 'C')