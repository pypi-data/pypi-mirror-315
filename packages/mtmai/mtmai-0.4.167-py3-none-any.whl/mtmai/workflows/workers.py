from mtmai.agents.base import GraphBuilder


def get_graphs() -> list[GraphBuilder]:
    from mtmai.agents.assisant_graph import MtmAssistantGraph

    return [
        MtmAssistantGraph(),
    ]


async def deploy_mtmai_workers(backend_url: str):
    import asyncio
    from mtmai.workflows.agentcall import AgentCall
    from mtmai.workflows.wfapp import wfapp

    # 获取配置文件
    # response = httpx.get("http://localhost:8383/api/v1/worker/config")
    # hatchet = Hatchet(debug=True)
    # list: WorkflowList = await wfapp.rest.aio.default_api.worker_config()
    worker = wfapp.worker("pyworker")
    if not worker:
        raise ValueError("worker not found")
    # worker.register_workflow(BasicRagWorkflow())
    # worker.register_workflow(FlowMcpClientExample())
    # worker.register_workflow(FlowArticleGen())
    # worker.register_workflow(FlowWriteChapter())
    # worker.register_workflow(BlogGen())
    worker.register_workflow(AgentCall())

    # from mtmai.workflows.graphflowhelper import build_graph_flow

    # for graph in get_graphs():
    #     builded_graph = await graph.build_graph()
    #     graph_flow = await build_graph_flow(builded_graph)
    #     worker.register_workflow(graph_flow())
    await worker.async_start()

    while True:
        await asyncio.sleep(1)
