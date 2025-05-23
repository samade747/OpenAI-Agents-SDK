# 3) What is the purpose of the Runner class?
# The Runner orchestrates the agent’s execution loop:

# Builds conversation messages: Prepares system + user inputs.

# Invokes the LLM: Sends messages to OpenAI’s chat completion endpoint.

# Tool dispatch: If the agent chooses a tool action, Runner calls the corresponding function and feeds results back into the loop.

# Termination logic: Knows when the agent has arrived at a final answer (e.g. looking for a special “finish” signal).

# In effect, Runner encapsulates the control flow that turns an agent definition into an interactive process.


# The Runner orchestrates an agent’s execution loop:

# Initialization: Builds the initial message list from agent.instructions plus the user’s input.

# LLM invocation: Sends messages to the model.

# Tool dispatch: If the agent’s response indicates a tool call, it invokes that tool and feeds the result back.

# Handoffs: If the agent delegates to another agent (handoff), Runner restarts the loop with the new agent.

# Termination: Stops when the agent returns a final output matching its output_type, or raises if max_turns is exceeded 