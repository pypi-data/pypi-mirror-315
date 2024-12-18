import json
import datetime

from dataclasses import asdict, is_dataclass

from .config import site_resources

ts_retool_rpc = site_resources.retool.rpc.get_client()


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    if isinstance(o, bytes):
        return o.decode("utf-8")
    return str(o)


def as_json_serializable(obj):
    if is_dataclass(obj):
        obj = as_json_serializable(asdict(obj))  # pyright: ignore
    if isinstance(obj, (list, tuple)):
        obj = [as_json_serializable(i) for i in obj]
    if isinstance(obj, dict):
        obj = {k: as_json_serializable(v) for k, v in obj.items()}
    if isinstance(obj, bytes):
        obj = obj.decode("utf-8")
    return json.loads(json.dumps(obj, default=default))


async def count_temporal_workflows(args, context):
    tp = await site_resources.temporal.connect()
    resp = await tp.count_workflows(**args)
    return as_json_serializable(resp)


async def temporal_workflow_status_summary(args, context):
    workflow_type = args.get("workflow_type", None)
    query = "ExecutionStatus = '{status}'"
    if workflow_type:
        query += f" and WorkflowType = '{workflow_type}'"
    statuses = ["Completed", "Failed", "Canceled", "ContinuedAsNew", "TimedOut", "Terminated"]
    data = {}
    for status in statuses:
        data[status] = await count_temporal_workflows(
            {"query": query.format(status=status)}, context
        )
    return data

async def list_temporal_workflows(args, context):
    tp = await site_resources.temporal.connect()
    kwargs = dict(args)
    map_histories = kwargs.pop("map_histories", True)
    kwargs["next_page_token"] = args.get("next_page_token", "").encode("utf-8")

    it = tp.list_workflows(**kwargs)
    await it.fetch_next_page()

    workflows = it.current_page or []

    data = []
    for wf in workflows:
        row = asdict(wf)
        if map_histories:
            hist = await tp.get_workflow_handle(wf.id, run_id=wf.run_id).fetch_history()
            row["history"] = hist.to_json_dict()
        row = as_json_serializable(row)
        data.append(row)

    data = {
        "workflows": data,
        "next_page_token": (
            it.next_page_token.decode("utf-8") if it.next_page_token else None
        ),
    }
    return data


ts_retool_rpc.register(
    {
        "name": "countTemporalWorkflows",
        "arguments": {
            "query": {
                "type": "string",
                "description": "The temporal query filter to apply to the workflows",
                "required": False,
                "array": False,
            },
        },
        "implementation": count_temporal_workflows,
        "permissions": None,
    }
)

ts_retool_rpc.register(
    {
        "name": "temporalWorkflowStatusSummary",
        "arguments": {
            "workflow_type": {
                "type": "string",
                "description": "The workflow type to filter by",
                "required": False,
                "array": False,
            },
        },
        "implementation": temporal_workflow_status_summary,
        "permissions": None,
    }
)

ts_retool_rpc.register(
    {
        "name": "listTemporalWorkflows",
        "arguments": {
            "query": {
                "type": "string",
                "description": "The temporal query filter to apply to the workflows",
                "required": False,
                "array": False,
            },
            "page_size": {
                "type": "number",
                "description": "The maximum number of workflows to return per page",
                "required": False,
                "array": False,
            },
            "next_page_token": {
                "type": "string",
                "description": "The token to get the next page of results",
                "required": False,
                "array": False,
            },
            "map_histories": {
                "type": "boolean",
                "description": "Whether to return the workflow execution histories",
                "required": False,
                "array": False,
            },
        },
        "implementation": list_temporal_workflows,
        "permissions": None,
    }
)


async def start_rpc():
    await ts_retool_rpc.listen()
