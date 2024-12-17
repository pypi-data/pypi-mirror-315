import uuid

import structlog
from langgraph.graph import StateGraph
from mtmaisdk.workflow import WorkflowMeta

LOG = structlog.get_logger()


async def build_graph_flow(graph: StateGraph) -> WorkflowMeta:
    from langchain_core.runnables import RunnableConfig
    from langgraph.checkpoint.memory import MemorySaver
    from langgraph.graph.graph import CompiledGraph
    from mtmaisdk.context.context import Context

    from mtmai.agents.ctx import init_mtmai_context
    from mtmai.agents.graphutils import is_internal_node, is_skip_kind
    from mtmai.core.coreutils import is_in_dev
    from mtmai.workflows.wfapp import wfapp

    memory = MemorySaver()

    @wfapp.workflow(on_events=["agent:call"])
    class AgentCall:
        @wfapp.step(timeout="10m", retries=3)
        async def call_agent(self, hatctx: Context):
            init_mtmai_context(hatctx)
            self.graph = graph
            thread_id = hatctx.input.get("thread_id")
            if not thread_id:
                thread_id = str(uuid.uuid4())
            messages = hatctx.input.get("messages")
            if not messages:
                messages = []
            self.compiled_graph = await self.compile_graph()
            stepId = uuid.UUID(hatctx.stepRunId)
            thread: RunnableConfig = {
                "run_id": stepId,
                "configurable": {
                    "thread_id": thread_id,
                    # 可以从指定检测点运行，以及分支
                    # "checkpoint_id": "xxxxx"
                },
            }
            return await self.run_graph(
                thread=thread,
                inputs=hatctx.input,
            )

        async def compile_graph(self) -> CompiledGraph:
            graph = self.graph.compile(
                checkpointer=memory,
                # checkpointer=await mtmai_context.get_graph_checkpointer(),
                # interrupt_after=["human"],
                interrupt_before=[
                    # HUMEN_INPUT_NODE,
                    # "update_flight_sensitive_tools",
                    # "develop_sensitive_tools",
                    # "book_car_rental_sensitive_tools",
                    # "book_hotel_sensitive_tools",
                    # "book_excursion_sensitive_tools",
                ],
                debug=True,
            )

            if is_in_dev():
                image_data = graph.get_graph(xray=1).draw_mermaid_png()
                save_to = "./.vol/asisant_graph.png"
                with open(save_to, "wb") as f:
                    f.write(image_data)
            return graph

        async def run_graph(self, thread: RunnableConfig, inputs=None):
            async for event in self.compiled_graph.astream_events(
                inputs,
                version="v2",
                config=thread,
                subgraphs=True,
            ):
                kind = event["event"]
                node_name = event["name"]
                data = event["data"]

                if not is_internal_node(node_name):
                    if not is_skip_kind(kind):
                        LOG.info("[event] %s@%s", kind, node_name)
                        # mtmai_context.emit("logs", {"on": kind, "node_name": node_name})

                # if kind == "on_chat_model_stream":
                #     yield data

                if kind == "on_chain_start":
                    LOG.info("on_chain_start %s:", node_name)
                    output = data.get("output")
                    if node_name == "__start__":
                        pass

                if kind == "on_chain_end":
                    LOG.info("on_chain_end %s:", node_name)
                    output = data.get("output")
                    if node_name == "__start__":
                        pass
                    # if node_name in [HUMEN_INPUT_NODE, "articleGen", "entry"]:
                    #     # human_ouput_message = output.get("human_ouput_message")
                    #     # LOG.info("human_ouput_message %s", human_ouput_message)
                    #     pass
                if node_name == "on_chat_start_node":
                    # thread_ui_state = output.get("thread_ui_state")
                    # if thread_ui_state:
                    pass
                    # await context.emitter.emit(
                    #     "ui_state_upate",
                    #     jsonable_encoder(thread_ui_state),
                    # )

                if kind == "on_tool_start":
                    pass

                if kind == "on_tool_end":
                    pass
                    output = data.get("output")

    return AgentCall
