import asyncio

from backend.core.llm import create_llm
from backend.graphs.trip_graph import create_trip_graph


async def main() -> None:
    llm = create_llm()
    graph = create_trip_graph(llm)

    user_query = "Plan a 5-day trip to Tokyo from San Francisco in March with a focus on food and culture."

    result = await graph.ainvoke({"query": user_query})
    print("Trip plan result:\n", result.get("result"))


if __name__ == "__main__":
    asyncio.run(main())
