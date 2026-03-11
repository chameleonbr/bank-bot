"""SessionStateToolkit — tools for the agent to manage the pending operation state."""

from agno.tools import Toolkit
from agno.run import RunContext

class SessionStateToolkit(Toolkit):
    def __init__(self):
        super().__init__(name="session_state_toolkit")
        self.register(self.update_pending_operation)
        self.register(self.cancel_pending_operation)
        self.register(self.confirm_pending_operation)
        self.register(self.get_pending_operation)

    def get_pending_operation(self, run_context: RunContext) -> str:
        """
        Retrieves the current pending operation and its data from the session state.
        Use this if you need to check what the user was doing before answering them.
        """
        state = run_context.session_state
        pending = state.get("pending_operation")
        if not pending:
            return "No pending operation."
        return f"Pending operation: {pending}"

    def update_pending_operation(self, run_context: RunContext, op_type: str, data: dict) -> str:
        """
        Updates the current pending financial operation with partial data (e.g. just the amount, or just the key).
        Use this when the user gives you constraints for a transaction piecemeal.
        `op_type` should be 'pix', 'ted', 'pix_schedule', 'ted_schedule', etc.
        `data` is a flat dictionary of the fields gathered so far (e.g. {"amount": 50.0, "pix_key": "123"}).
        Do not use this to execute the transaction; it only stores the state.
        """
        state = run_context.session_state
        pending = state.get("pending_operation")
        
        if pending and pending.get("type") == op_type:
            # Update existing pending operation of same type
            pending.update(data)
            state["pending_operation"] = pending
        else:
            # Create new pending operation
            new_op = {"type": op_type, "status": "pending_data"}
            new_op.update(data)
            state["pending_operation"] = new_op
            
        return f"Pending operation updated: {state['pending_operation']}"

    def cancel_pending_operation(self, run_context: RunContext) -> str:
        """
        Cancels the current pending operation and clears it from the session.
        Use this if the user aborts the transaction.
        """
        run_context.session_state["pending_operation"] = None
        return "Pending operation has been cancelled and cleared."

    def confirm_pending_operation(self, run_context: RunContext) -> str:
        """
        Marks the current pending operation as confirmed.
        Use this ONLY when the user explicitly says 'yes' or confirms the transaction details.
        Once confirmed, you must immediately call the actual execution tool (e.g. pix_transfer, ted_transfer)
        using the data from the session state to execute it.
        """
        state = run_context.session_state
        pending = state.get("pending_operation")
        
        if not pending:
            return "There is no pending operation to confirm."
            
        pending["status"] = "confirmed"
        state["pending_operation"] = pending
        
        op_type = pending.get("type")
        return f"Operation confirmed. You must now invoke the execution tool for '{op_type}' passing the required arguments."
